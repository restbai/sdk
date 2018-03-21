import requests


def service(url, endpoint, params):
    if params['image_base64'] is not None:
        params.pop('image_url', None)
        return requests.post(url=url+endpoint, data=params, allow_redirects=False, timeout=60)
    else:
        params.pop('image_base64', None)
        return requests.get(url=url+endpoint, params=params, allow_redirects=True, timeout=30)
