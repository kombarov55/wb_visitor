import time

from playwright.sync_api import Page

from playwright_util import scroll_slowly_to_bottom, scroll_until_predicate


def run(page: Page, url: str, name: str, text: str, is_like: bool):

    def log(s: str):
        print("set_like_to_comment({} {}) {}".format(name, text, s))

    page.goto(url)
    page.wait_for_load_state("networkidle")
    log("page loaded")

    log("start scrolling to bottom")
    scroll_slowly_to_bottom(page)
    log("end scrolling to bottom")

    page.click("li.user-activity__tab")
    log("clicked at Вопросы")

    page.get_by_text("Смотреть все отзывы").click()
    log("clicked at Cмотреть все отзывы")

    time.sleep(2)
    page.wait_for_selector("div.product-feedbacks__main")
    log("feedback page loaded")

    log("start scrolling to comment")
    found = scroll_until_predicate(
        page, lambda paige: is_comment_loaded(paige, text))
    log("end scrolling to bottom. comment found? {}".format(found))

    log("attempt to find comment")
    comment = find_comment(page, name, text)
    if comment is not None:
        log("comment found")
        button = comment.locator("button.j-vote-up") \
            if is_like \
            else comment.locator("button.j-vote-down")
        button.click()

        log("{} set".format("like" if is_like else "dislike"))
    else:
        log("did not find comment")


def is_comment_loaded(page: Page, text: str):
    return page.get_by_text(text).count() == 1


def find_comment(page: Page, name: str, text: str):
    comments = page.locator("li.comments__item")
    for i in range(0, comments.count()):

        comment = comments.nth(i)
        comment_name = comment.locator("p.feedback__header").inner_text()
        comment_text = comment.locator("p.feedback__text").inner_text()
        if name == comment_name and text == comment_text:
            return comment
