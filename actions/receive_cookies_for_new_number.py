import os
import time
import uuid
from datetime import datetime

from playwright.sync_api import Page

import playwright_util
from model.exceptions import CannotResolveCaptchaException
from service import sms_activate, solve_captcha


def run(page: Page, id: str, number: str):
    print("receive new cookies: id={} number={}".format(id, number))
    page.goto("https://wildberries.ru")
    page.context.clear_cookies()
    page.wait_for_selector("a.j-main-login")
    page.click("a.j-main-login")

    page.wait_for_selector("input.input-item")
    page.type("input.input-item", number[1:len(number)], delay=123)

    page.click("button#requestCode")

    filename = "{}.jpeg".format(str(uuid.uuid4()))

    resolve_captcha(page, filename)

    code = sms_activate.receive_code(id)
    if code is None:
        page.pause()
        resolve_captcha(page, filename)
        code = sms_activate.receive_code(id)

    page.type("input.j-input-confirm-code", code, delay=400)

    time.sleep(5)
    playwright_util.copy_cookies(page, "activated_cookies.json")
    cookies = playwright_util.get_cookies_json(page)

    try:
        print("remove captcha file {}".format(filename))
        os.remove(filename)
    except Exception as e:
        print(e)
        print("файл не могу удалить, ну и хуй с ним")

    return cookies


def resolve_captcha(page: Page, filename: str):
    while True:
        time.sleep(2)
        src = page.locator("img.form-block__captcha-img").get_attribute("src")

        playwright_util.download_img_base64(src, filename)
        captcha_text = solve_captcha.request_solving(filename)

        page.type("input#smsCaptchaCode", captcha_text, delay=250)
        page.click("button.login__btn")
        print("submit captcha.")
        time.sleep(1)

        if page.get_by_text("Введите код").is_visible(timeout=3000):
            print("successfully submitted captcha")
            break

        if page.get_by_text("Вы исчерпали все попытки запроса кода. Попробуйте позже").is_visible():
            raise CannotResolveCaptchaException
        if not page.get_by_text("Код указан неверно").is_visible():
            print("Код указан неверно")
            break

