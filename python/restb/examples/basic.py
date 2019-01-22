import base64

from restb.sdk import *
from restb.sdk.api import service


def test_api(client_key):

    # note the module variables as defined in restb/sdk/__init__.py
    params = __PARAMS.copy()

    # 1. Pick which API endpoint to use (US vs. EU)
    url = __URL_US

    # 2. Determine which solution (API and model) to use
    model_id = 're_features_v3'  # from list of keys from __MODELS
    endpoint = __ENDPOINT
    params['model_id'] = model_id

    # 3. Insert in your client_key
    params['client_key'] = client_key

    # 4a. Pick an image_url
    image_url = 'https://demo.restb.ai/images/demo/demo-1.jpg'
    params['image_url'] = image_url

    # # 4b. -OR- add a base64 encoded payload (development only!)
    # file = '/tmp/demo-1.jpg'
    # with open(file, "rb") as image_file:
    #     image_base64 = base64.urlsafe_b64encode(image_file.read())
    #     params['image_base64'] = image_base64

    # 5. Call the API
    return service(url=url, endpoint=endpoint, params=params)


def run(client_key):
    response = test_api(client_key)
    print(response.text)
