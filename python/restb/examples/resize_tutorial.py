import requests

from io import BytesIO
from PIL import Image

from restb.sdk.api import resize_image


def resize():
    # 1. first download and load image
    response = requests.get(url='https://demo.restb.ai/images/demo/demo-2.jpg')
    image = Image.open(BytesIO(response.content))
    print("Original image dimensions: {}".format(image.size))

    # 2. then invoke the SDK resize function
    resized_image = resize_image(image)
    print("New resized dimensions: {}".format(resized_image.size))


def run():
    resize()


if __name__ == '__main__':
    run()
