from playwright.sync_api import Page

import playwright_util
from playwright_util import scroll_slowly_to_bottom


def set_like(page: Page, url: str, name: str, date: str, is_like: bool):
    playwright_util.load_cookies(page, "./cookies-auth.json")
    page.goto(url)
    page.wait_for_load_state("networkidle")
    scroll_slowly_to_bottom(page)
    page.click("li.user-activity__tab")
    page.wait_for_selector("div.comment-card")
    comments = page.locator("div.comment-card")
    success = False
    for i in range(0, comments.count()):
        comment = comments.nth(i)
        comment_name = comment.locator(".comment-card__name").inner_text()
        comment_date = comment.locator(".comment-card__date").inner_text()

        if comment_name == name and comment_date == date:
            if is_like:
                comment.locator("button.j-vote-up").click()
            else:
                comment.locator("button.j-vote-down").click()
            success = True
            break
    print("success: {}".format(success))
