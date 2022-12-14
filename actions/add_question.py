import time

from playwright.sync_api import Page

import playwright_util
from config import app_config


def run(page: Page, url: str, text: str):
    page.goto(url)

    page.wait_for_selector("li.user-activity__tab")
    time.sleep(1)

    page.click("button.collapsible__toggle")
    time.sleep(2)

    button = page.locator("li.user-activity__tab").nth(1)
    playwright_util.scroll_to_element(page, button)
    button.click()

    page.wait_for_selector("textarea#new-question")
    input_field = page.locator("textarea#new-question")

    time.sleep(3)
    input_field.click()
    input_field.type(text, delay=200)

    time.sleep(2)
    if app_config.mock:
        print("MOCK add question {}".format(text))
    else:
        page.click("button.textarea-block__submit")
        print("success")
        time.sleep(2)
