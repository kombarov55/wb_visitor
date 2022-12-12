import time

from playwright.sync_api import sync_playwright, Browser
from sqlalchemy.orm import Session

from actions import receive_cookies_for_new_number
from config import database, app_config
from model.phone_number import PhoneNumberStatus, PhoneNumberVO
from repository import phone_number_repository


def run():
    session = database.session_local()
    while True:
        xs = phone_number_repository.find_just_received(session)
        if len(xs) != 0:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=app_config.headless)
                for vo in xs:
                    try:
                        execute_task(session, browser, vo)
                    except Exception as e:
                        print(str(e))

        time.sleep(3)


def execute_task(session: Session, browser: Browser, vo: PhoneNumberVO):
    # vo.status = PhoneNumberStatus.activating
    # phone_number_repository.update(session, vo)

    page = browser.new_page()

    cookies_json = receive_cookies_for_new_number.run(page, id=vo.ext_id, number=vo.number)

    vo.cookies_json = cookies_json
    vo.status = PhoneNumberStatus.activated

    phone_number_repository.update(session, vo)

    page.close()

