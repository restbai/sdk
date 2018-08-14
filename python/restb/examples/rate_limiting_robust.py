import json
import time
import multiprocessing.dummy as mp

from restb.sdk import *
from restb.sdk.api import service


# set allotted number of requests per second
# this is defined here as it could be retrieved through some external mechanism
__requests_per_second = 4
__waiting_threads = 10


# lambda helper for getting current time in millis
now_millis = lambda: int(round(time.time() * 1000))


def test_api(client_key):

    # 1. create test image data and both processing and result queues
    urls = ['https://demo.restb.ai/images/demo/demo-1.jpg',
            'https://demo.restb.ai/images/demo/demo-2.jpg',
            'https://demo.restb.ai/images/demo/demo-3.jpg',
            'https://demo.restb.ai/images/demo/demo-4.jpg',
            'https://demo.restb.ai/images/demo/demo-5.jpg',
            'https://demo.restb.ai/images/demo/demo-6.jpg']
    queue = mp.Queue()
    image_id = 1
    for url in urls:
        for model in __MODELS.keys():
            queue.put(dict(id=image_id, url=url, model=model))
        image_id += 1
    results = mp.Queue()

    # 2. Pick which API endpoint to use (US vs. EU)
    url = __URL_US

    # 3. Define concurrency specific objects
    # stats objects
    lock_stats = mp.Lock()
    counter = mp.Value('i', 0)
    avg_req_time = mp.Value('f', 0)
    time_start = mp.Value('f', 999999999999999)
    time_end = mp.Value('f', 0)
    # concurrency control objects
    lock_bucket = mp.Lock()
    bucket = mp.Queue()
    # pre-seed bucket
    for i in range(__requests_per_second):
        bucket.put('token')

    # 4. Spawn processes/threads to process the images in the queue
    #   first start bucket refill thread
    refill_thread = mp.Process(target=bucket_refill_thread, args=(lock_bucket, bucket))
    refill_thread.start()
    pool = []
    for i in range(__requests_per_second * __waiting_threads):  # waiting threads to keep the pipeline full
        # pass in necessary parameters to thread, including client key, etc.
        p = mp.Process(target=image_process_thread,
                       args=(url, client_key, queue, results,
                             lock_stats, counter, avg_req_time, time_start, time_end,
                             lock_bucket, bucket))
        pool.append(p)
        p.start()

    # 5. clean-up after queue has been processed with "poison pill"
    while not queue.empty():
        # wait for queue to be processed
        time.sleep(1)
    for i in pool:
        # seed shutdown messages / poison pills
        queue.put(dict(id=-1, url='shutdown', model='shutdown'))
    for p in pool:
        # enforce clean shutdown of threads
        p.join()
    # stop bucket refill thread
    bucket.put('shutdown')
    refill_thread.join()

    # 6. finally, return accumulated results
    total = time_end.value - time_start.value
    print('[{requests}] requests processed in [{seconds}] seconds with average time [{time}] ms, total throughput: [{throughput}] rps'.format(
        requests=counter.value,
        seconds=str(round(total / 1000.0, 1)),
        time=str(round(avg_req_time.value / counter.value, 0)),
        throughput=str(round(counter.value / (total / 1000.0), 2))
    ))
    return results


def bucket_refill_thread(lock_bucket, bucket):
    while True:
        # (re-)establish parameters
        interval = float(1.0)
        tokens = __requests_per_second

        # sleep for interval
        #   the blow section breaks intervals apart into smaller chunks in order to smooth out bursting
        #   for example, 8 rps can be broken down into: 2 requests / 250 ms
        if __requests_per_second > 1:
            for i in range(__requests_per_second-1, 1):
                if __requests_per_second % i == 0:
                    interval = 1 / float(i)
                    tokens = __requests_per_second / i
                    break
        time.sleep(interval)

        # check for poison pill
        lock_bucket.acquire()
        size = bucket.qsize()
        shutdown = False
        for i in range(size):
            try:
                token = bucket.get(block=False)
                if 'shutdown' == token:
                    shutdown = True
                    break
                else:
                    bucket.put(token)
            except:
                pass
        if shutdown:
            break

        # don't let the bucket exceed token capacity
        while bucket.qsize() < min(size + tokens, __requests_per_second):
            bucket.put('token')
        lock_bucket.release()


def image_process_thread(url, client_key, queue, results,
                         lock_stats, counter, avg_req_time, time_start, time_end,
                         lock_bucket, bucket):
    while True:
        # acquire token in order to process
        lock_bucket.acquire()
        token = None
        try:
            token = bucket.get(block=False)  # don't do anything with the token, just remove it, as it acts as our "access rights"
        except:
            pass
        # first release lock
        lock_bucket.release()
        # then proceed or sleep
        if not token:
            time.sleep(1 / float(__requests_per_second))
            continue

        # get image URL entry to process
        entry = None
        try:
            entry = queue.get(block=False)
        except:
            pass
        if entry:
            image_id = entry['id']
            img_url = entry['url']
            model_id = entry['model']
            if img_url == 'shutdown':
                print('thread shutting down')
                break
            params = __PARAMS.copy()  # note the module variables as defined in restb/sdk/__init__.py
            params['client_key'] = client_key
            params['image_url'] = img_url
            params['model_id'] = model_id
            endpoint = __MODELS[model_id]
            start_time = now_millis()
            resp = service(url=url, endpoint=endpoint, params=params)
            end_time = now_millis()
            msg = '[{http}] <{limit}> thread [{thread}] {msg}'
            if resp.status_code == 200:
                vals = json.loads(resp.text)
                results.put(dict(id=image_id, model=model_id, result=vals['response']))
                total = end_time - start_time
                print(msg.format(
                    http=resp.status_code,
                    limit=resp.headers['X-RateLimit-Remaining-second'],
                    thread=mp.current_process().name,
                    msg='processed request in [' + str(total) + '] ms')
                )
                # increment counter
                lock_stats.acquire()
                counter.value += 1
                avg_req_time.value += total
                if start_time < time_start.value:
                    time_start.value = start_time
                if end_time > time_end.value:
                    time_end.value = end_time
                lock_stats.release()
            elif resp.status_code == 429:
                # handle over-rate limit retrying
                print(msg.format(
                    http=resp.status_code,
                    limit=resp.headers['X-RateLimit-Remaining-second'],
                    thread=mp.current_process().name,
                    msg='surpassed rate limit, trying again')
                )
                # re-queue entry and try again
                queue.put(entry)


def run(client_key):
    output = test_api(client_key)
    print('\n\nFinal results queue:')
    results = {}
    while not output.empty():
        # accumulate differing solution results for an image ID together
        result = output.get()
        if result['id'] not in results:
            results[result['id']] = {result['model']: result['result']}
        else:
            results[result['id']][result['model']] = result['result']
    for i in range(len(results.keys())):
        for k, v in sorted(results[i+1].items()):
            print('[{id}] [{model}] {res}'.format(id=i+1, model=k, res=v))
