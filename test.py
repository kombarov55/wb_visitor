import base64
import io

from PIL import Image
from playwright.sync_api import sync_playwright
from smsactivate.api import SMSActivateAPI

import playwright_util
from actions import add_question, do_nothing, add_to_cart, add_to_favorites, remove_from_favorites, remove_from_cart
from config import app_config


def test_question(page):
    add_question.run(page, url="https://www.wildberries.ru/catalog/12489184/detail.aspx", text="Сколько стоит?")


def test_do_nothing(page):
    do_nothing.run(page)


def test_add_to_cart(page):
    add_to_cart.run(page, "https://www.wildberries.ru/catalog/123110851/detail.aspx?targetUrl=XS")


def test_add_to_favorites(page):
    add_to_favorites.run(page, "https://www.wildberries.ru/catalog/123110851/detail.aspx?targetUrl=XS")


def test_remove_from_favorites(page):
    remove_from_favorites.run(page, "98919124")


def test_remove_from_cart(page):
    remove_from_cart.run(page, "40193383")


if __name__ == '__main__':
    with sync_playwright() as p:
        page = p.chromium.launch(headless=False).new_page()
        playwright_util.load_cookies(page, "cookies-auth.json")
        test_remove_from_cart(page)
