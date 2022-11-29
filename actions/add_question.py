from playwright.sync_api import Page

import playwright_util
from config import app_config


def run(page: Page, url: str, text: str):
    page.goto(url)
    page.wait_for_selector("li.user-activity__tab")
    button = page.locator("li.user-activity__tab").nth(1)
    button.click()
    page.wait_for_selector("textarea#new-question")
    input_field = page.locator("textarea#new-question")
    input_field.click()
    input_field.type(text, delay=10)
    if app_config.mock:
        print("MOCK add question {}".format(text))
    else:
        page.click("button.textarea-block__submit")


def test(page: Page):
    playwright_util.load_cookies(page, "./cookies-auth.json")
    run(page,
                 "https://www.wildberries.ru/catalog/39769256/detail.aspx?targetUrl=XS",
                 "Сколько МП камера?")