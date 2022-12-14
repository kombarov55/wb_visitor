import time

from playwright.sync_api import Page

import playwright_util
from config import app_config
from playwright_util import scroll_slowly_to_bottom


def run(page: Page, url: str, name: str, date: str, is_like: bool):
    page.goto(url)
    page.wait_for_load_state("networkidle")
    scroll_slowly_to_bottom(page)
    page.click("li.user-activity__tab")
    time.sleep(2)
    page.wait_for_selector("div.comment-card")
    comments = page.locator("div.comment-card")
    success = False
    for i in range(0, comments.count()):
        comment = comments.nth(i)
        comment_name = comment.locator(".comment-card__name").inner_text()
        comment_date = comment.locator(".comment-card__date").inner_text()

        if comment_name == name and comment_date == date:
            if app_config.mock:
                print("MOCK: set like to {} {}".format(comment_name, comment_date))
            else:
                if is_like:
                    comment.locator("button.j-vote-up").click()
                else:
                    comment.locator("button.j-vote-down").click()
            time.sleep(4)
            success = True
            break
    print("success: {}".format(success))
