import time

from playwright.sync_api import Page

from datetime import datetime


from config import app_config


def run(page: Page, url: str, task_id: str):
    def log(s: str):
        line = "{} add to favorites url={} {}".format(str(datetime.now()), url, s)
        print(line)
        with open("{}/{}.log".format(app_config.static_dir_path, str(task_id)), "a") as file:
            file.write(line + "\n")

    page.goto(url)
    log("goto url")

    time.sleep(2)
    log("sleep 2")

    page.wait_for_load_state("networkidle")
    log("networkidle now")

    if app_config.mock:
        print("Mock click btn-heart-black")
    else:
        page.get_by_role("button", name="Добавить в избранное").click()
    log("Success")
    time.sleep(2)
