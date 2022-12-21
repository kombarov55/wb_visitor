# This is a sample Python script.
from playwright.sync_api import Page

import scheduler
from config import database
from repository import task_repository, phone_number_repository
from scheduled import task_service, activate_numbers_service
from actions import set_like_to_comment


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def test_set_like(page: Page):
    set_like_to_comment.run(page,
                                   "https://www.wildberries.ru/catalog/43809808/detail.aspx?targetUrl=MI",
                                   "Елена",
                                   "23 ноября 2022, 03:48",
                            True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    database.base.metadata.create_all(bind=database.engine)
    task_repository.set_all_running_to_failed()
    phone_number_repository.set_all_activating_to_just_received()
    scheduler.run()
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     page = browser.new_page()
    #
    #     # look_at_article.test(page)
    #
    #
    #     page.pause()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
