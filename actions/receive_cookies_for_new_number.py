import time

from playwright.sync_api import Page

import playwright_util
from service import sms_activate, solve_captcha


def run(page: Page, id: str, number: str):
    print("receive new cookies: id={} number={}".format(id, number))
    page.goto("https://wildberries.ru")
    page.wait_for_selector("a.j-main-login")
    page.click("a.j-main-login")

    page.wait_for_selector("input.input-item")
    page.type("input.input-item", number[1:len(number)], delay=200)

    page.click("button#requestCode")

    time.sleep(2)
    src = page.locator("img.form-block__captcha-img").get_attribute("src")
    playwright_util.download_img_base64(src, "captcha.jpeg")
    captcha_text = solve_captcha.request_solving("captcha.jpeg")

    page.type("input#smsCaptchaCode", captcha_text, delay=800)
    page.click("button.login__btn")

    code = sms_activate.receive_code(id)
    page.type("input.j-input-confirm-code", code, delay=600)

    time.sleep(5)
    playwright_util.copy_cookies(page, "activated_cookies.json")
    cookies = playwright_util.get_cookies_json(page)
    return cookies

