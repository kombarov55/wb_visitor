import datetime
from concurrent.futures import ThreadPoolExecutor

from playwright.sync_api import sync_playwright, Page, Playwright

from actions import receive_cookies_for_new_number
from config import database, app_config
from model.exceptions import CannotResolveCaptchaException
from model.phone_number import PhoneNumberStatus, PhoneNumberVO
from repository import phone_number_repository, proxy_repository


def tick(executor: ThreadPoolExecutor):
    with database.session_local() as session:
        xs = phone_number_repository.find_just_received(session)

        running_now = phone_number_repository.count_activating()
        max_running = app_config.max_workers_for_sms
        available_workers = max_running - running_now

        amount = len(xs) \
            if len(xs) < available_workers \
            else available_workers

        if amount != 0:
            print("found {} numbers to activate".format(amount))
            for x in xs[0:amount]:
                x.status = PhoneNumberStatus.activating
                x.status_change_datetime = datetime.datetime.now()
                phone_number_repository.update(session, x)

                executor.submit(execute, x)


def execute(vo: PhoneNumberVO):
    session = database.session_local()

    vo = phone_number_repository.find_by_id(session, vo.id)
    proxy = proxy_repository.get_random_proxy()
    print("got random proxy ip={} uname={} pwd={}".format(proxy.ip, proxy.username, proxy.password))

    try:
        with sync_playwright() as p:
            if app_config.use_proxy:
                browser = p.chromium.launch(
                    headless=app_config.headless,
                    proxy={
                        "server": proxy.ip,
                        "username": proxy.username,
                        "password": proxy.password
                    }
                )
                browser.new_context(proxy={"server": proxy.ip})
            else:
                browser = p.chromium.launch(headless=app_config.headless)

            page = browser.new_page()
            page.goto("https://httpbin.org/ip")
            print("ip check: ")
            print(page.text_content("*"))
            cookies_json = receive_cookies_for_new_number.run_v2(page, ext_id=vo.ext_id, number=vo.number)

        vo.cookies_json = cookies_json
        vo.status = PhoneNumberStatus.activated
        vo.status_change_datetime = datetime.datetime.now()
        phone_number_repository.update(session, vo)
        print("saved cookies for number={}".format(vo.number))
        proxy_repository.update_proxy_after_auth(session, proxy)

        session.commit()
        session.close()
    except CannotResolveCaptchaException as e:
        print("probably blocked proxy ip={}".format(proxy.ip))
        proxy_repository.update_proxy_after_failed_auth(session, proxy)
        phone_number_repository.set_status(session, vo.id, PhoneNumberStatus.just_received)
    except Exception as e:
        print(str(e))
        phone_number_repository.set_status(session, vo.id, PhoneNumberStatus.just_received)
