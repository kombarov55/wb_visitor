from playwright.sync_api import sync_playwright
from repository import phone_number_repository
import playwright_util
import time

with sync_playwright() as p:
    page = p.chromium.launch(headless=False).new_page()
    page.goto("https://wb.ru")
    phone_number = phone_number_repository.get_number_for_task("")
    print("cookies={}".format(phone_number.cookies_json))
    playwright_util.set_cookies(page, phone_number.cookies_json)
    time.sleep(1)
    page.reload()

    page.pause()
