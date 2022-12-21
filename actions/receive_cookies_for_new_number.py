import os
import time
import uuid

from playwright.sync_api import Page

import playwright_util
from model.exceptions import CannotResolveCaptchaException
from service import sms_activate, captcha_service


def run_v2(page: Page, ext_id: str, number: str):
    prepare_and_click_login(page)
    filename = "{}.jpeg".format(str(uuid.uuid4()))

    while True:
        time.sleep(3)
        step = determine_auth_step(page)
        print("current auth step: {}".format(step))
        if step == "ENTER_PHONE":
            on_enter_phone(page, number)
        elif step == "CAPTCHA":
            on_captcha(page, filename)
        elif step == "SMS":
            on_sms(page, ext_id)
        elif step == "SUCCESS":
            print("auth success")
            break

    playwright_util.copy_cookies(page, "activated_cookies.json")
    cookies = playwright_util.get_cookies_json(page)

    try:
        print("remove captcha file {}".format(filename))
        os.remove(filename)
    except Exception as e:
        print(e)
        print("файл не могу удалить, ну и хуй с ним")

    return cookies


def prepare_and_click_login(page: Page):
    page.goto("https://wildberries.ru")
    page.context.clear_cookies()
    page.wait_for_selector("a.j-main-login")
    page.click("a.j-main-login")


def determine_auth_step(page: Page):
    if page.get_by_text("Контактный телефон").is_visible():
        return "ENTER_PHONE"
    if page.get_by_text("Вы исчерпали все попытки запроса кода. Попробуйте позже").is_visible():
        raise CannotResolveCaptchaException()
    if page.get_by_text("Введите код с картинки").is_visible():
        return "CAPTCHA"
    if page.get_by_text("Код выслан на номер").is_visible():
        return "SMS"
    else:
        return "SUCCESS"


def on_enter_phone(page: Page, number: str):
    page.wait_for_selector("input.input-item")
    page.type("input.input-item", number[1:len(number)], delay=123)
    page.click("button#requestCode")
    print("enter phone success")


def on_captcha(page: Page, filename: str):
    src = page.locator("img.form-block__captcha-img").get_attribute("src")

    playwright_util.download_img_base64(src, filename)
    captcha_text = captcha_service.request_solving(filename)

    page.type("input#smsCaptchaCode", captcha_text, delay=250)
    page.click("button.login__btn")
    print("submit captcha success")


def on_sms(page: Page, ext_id: str):
    code = sms_activate.receive_code(ext_id, page)
    if code is None and page.get_by_text("Запросить код повторно").count() == 1:
        page.get_by_text("Запросить код повторно").nth(0).click()
        print("timeout on receive sms")
    else:
        page.type("input.j-input-confirm-code", code, delay=400)
        print("receive sms success")
