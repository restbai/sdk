import requests

from PIL import Image


def service(url, endpoint, params):
    if params['image_base64'] is not None:
        params.pop('image_url', None)
        query_params = dict(client_key=params['client_key'])  # client_key should always be passed as a query parameter
        return requests.post(url=url+endpoint, params=query_params, data=params, allow_redirects=False, timeout=60)
    else:
        params.pop('image_base64', None)
        return requests.get(url=url+endpoint, params=params, allow_redirects=True, timeout=30)


def resize_image_path(image_load_path, image_save_path):
    # load image
    img = Image.open(image_load_path)

    # handle resize
    resized_img = resize_image(img)

    # save the image by re-encoding as JPEG
    resized_img.save(fp=image_save_path, format='JPEG', quality=90)


def resize_image(image):
    # calculate new dimensions
    x, y = image.size
    small = min(x, y)
    factor = small / 600 if small > 600 else 1.0
    resize_dimensions = int(x / factor), int(y / factor)

    # resize (using LANCZOS resampling/interpolation)
    image = image.resize(resize_dimensions, resample=Image.LANCZOS)
    return image
