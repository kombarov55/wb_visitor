from concurrent.futures import ThreadPoolExecutor

from playwright.sync_api import sync_playwright

from actions import receive_cookies_for_new_number
from config import database, app_config
from model.phone_number import PhoneNumberStatus, PhoneNumberVO
from repository import phone_number_repository


def tick(executor: ThreadPoolExecutor):
    with database.session_local() as session:
        xs = phone_number_repository.find_just_received(session)

        if len(xs) != 0:
            print("found {} numbers to activate".format(len(xs)))
            executor.submit(wrap_execute, xs)


def wrap_execute(xs):
    for x in xs:
        with database.session_local() as session:
            x.status = PhoneNumberStatus.activating
            phone_number_repository.update(session, x)

    for vo in xs:
        try:
            execute(vo)
        except Exception as e:
            print(str(e))


def execute(vo: PhoneNumberVO):
    session = database.session_local()

    with sync_playwright() as p:
        page = p.chromium.launch(headless=app_config.headless).new_page()
        cookies_json = receive_cookies_for_new_number.run(page, id=vo.ext_id, number=vo.number)

    vo.cookies_json = cookies_json
    vo.status = PhoneNumberStatus.activated
    phone_number_repository.update(session, vo)
    session.close()

