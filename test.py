import base64
import io

from PIL import Image
from playwright.sync_api import sync_playwright, Page
from smsactivate.api import SMSActivateAPI

import playwright_util
from actions import add_question, do_nothing, add_to_cart, add_to_favorites, remove_from_favorites, remove_from_cart, \
    set_like_to_comment
from config import app_config, database
from repository import proxy_repository


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


def test_set_like(page):
    set_like_to_comment.run(page=page,
                            url="https://www.wildberries.ru/catalog/46174110/detail.aspx?targetUrl=SP",
                            name="Кирилл",
                            text="Вместо 5 дней шло 20.Спасибо.", is_like=False)


def pw_sandbox(page: Page):
    print("debug")
    page.pause()


def load_proxy():
    s = """176.103.82.169:3875:user61433:8421d9
176.103.82.223:3875:user61433:8421d9
212.115.50.44:3875:user61433:8421d9
45.90.44.136:3875:user61433:8421d9
45.8.156.26:3875:user61433:8421d9
46.149.174.30:3875:user61433:8421d9
45.145.3.86:3875:user61433:8421d9"""
    lines = s.splitlines()
    with database.session_local() as session:
        for line in lines:
            xs = line.split(":")
            proxy_repository.save(session, {
                "ip":  xs[0] + ":" + xs[1],
                "username": xs[2],
                "password": xs[3]
            })




if __name__ == '__main__':
    with sync_playwright() as p:
        page = p.chromium.launch(headless=False).new_page()
        # pw_sandbox(page)
        playwright_util.load_cookies(page, "cookies-auth.json")
        # pw_sandbox(page)
        # test_remove_from_cart(page)
        test_set_like(page)
    load_proxy()
