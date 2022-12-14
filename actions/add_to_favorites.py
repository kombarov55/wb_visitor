import time

from playwright.sync_api import Page

from config import app_config


def run(page: Page, url: str):
    page.goto(url)
    time.sleep(2)
    page.wait_for_load_state("networkidle")

    page.pause()
    if app_config.mock:
        print("Mock click btn-heart-black")
    else:
        page.get_by_role("button", name="Добавить в избранное").click()
    print("Success")
    time.sleep(2)


