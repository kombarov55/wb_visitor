import io

import requests
from PIL import Image
from twocaptcha import TwoCaptcha


def download_img_base64mg(src):
    content = requests.get(src).content
    image_file = io.BytesIO(content)
    image = Image.open(image_file)
    with open("captcha.png", "wb") as f:
        image.save(f, "png")


def request_solving(path: str):
    solver = TwoCaptcha("665080ecc6111b94809f7d4fbba65b29")
    print("initialized twocaptcha client")

    print("sending captcha request")
    result = solver.normal(path)
    print("received result: {}".format(result))

    return result["code"]
