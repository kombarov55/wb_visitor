import time

from playwright.sync_api import Page

from config import app_config


def run(page: Page, url: str):
    page.goto(url)
    time.sleep(3)
    page.wait_for_load_state("networkidle")
    if app_config.mock:
        print("click")
    else:
        page.pause()
        page.get_by_role("button", name="Добавить в корзину").click()
    print("success")
    time.sleep(1)
