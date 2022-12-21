import io

import requests
from PIL import Image
from playwright.sync_api import sync_playwright
from twocaptcha import TwoCaptcha


def download_img(src):
    content = requests.get(src).content
    image_file = io.BytesIO(content)
    image = Image.open(image_file)
    with open("captcha.png", "wb") as f:
        image.save(f, "png")


def request_solving(path: str):
    solver = TwoCaptcha("665080ecc6111b94809f7d4fbba65b29")
    result = solver.normal(path)
    print("received result: {}".format(result))
    return result["code"]


def scratch_run():
    with sync_playwright() as p:
        page = p.chromium.launch(headless=False).new_page()
        page.goto("https://eda.yandex.ru/showcaptcha?cc=1&mt=8352A9C8F47CF4647FC70ACC32EC3D3B2548F41F091E639C13DE59A3A59837A09A06&retpath=aHR0cHM6Ly9lZGEueWFuZGV4LnJ1L21vc2Nvdz9zaGlwcGluZ1R5cGU9ZGVsaXZlcnk%2C_fd0593559cbccee517013bb08a73d4e7&t=2/1669868919/f5b63d6a67e361320af8c8093a8742c8&u=2cf4f937-a709f913-38f2a278-638bb4ab&s=467c90359f6bf2ce0bfa743ddfebff82")


if __name__ == "__main__":
    scratch_run()
