import base64
import io
import json
import time
import urllib

from PIL import Image
from playwright.sync_api import Page, Locator


def scroll_to_y(page: Page, dest_y: int, delta: int = 500, interval_between_scrolls: float = 0.1):
    current_height = 0

    while True:
        page.evaluate("() => window.scrollTo(0, {});".format(current_height + delta))
        current_height += delta
        time.sleep(interval_between_scrolls)
        if current_height > dest_y:
            break


def scroll_slowly_to_bottom(page: Page):
    scroll_to_y(page, page.evaluate("() => document.body.scrollHeight;"), 500, 0.1)


def get_cookies_json(page: Page):
    cookies = page.context.cookies()
    return json.dumps(cookies)


def copy_cookies(page: Page, path: str):
    cookies = page.context.cookies()
    with open(path, "w") as file:
        file.write(json.dumps(cookies))


def load_cookies(page: Page, path: str):
    with open(path) as file:
        s = file.read()
        cookies = json.loads(s)
        page.context.clear_cookies()
        page.context.add_cookies(cookies)


def scroll_to_element(page: Page, locator: Locator):
    y = locator.bounding_box()["y"]
    scroll_to_y(page=page, dest_y=y, delta=15, interval_between_scrolls=0.01)


def get_query_param(url, param):
    q = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(q.query)[param][0]


def download_img_base64(src: str, path: str):
    src = src[23:len(src)]
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(src, "utf-8"))))
    img.save(path)
    print("saved captcha to {}".format(path))

