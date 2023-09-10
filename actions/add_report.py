import time

from playwright.sync_api import Page

from playwright_util import scroll_slowly_to_bottom, scroll_until_predicate

from datetime import datetime

from config import app_config


def run(page: Page, task_id, product_url: str, comment_text: str):
    def log(s: str):
        line = "{} add report to comment ({}) {}".format(str(datetime.now()), comment_text, s)
        print(line)
        with open("{}/{}.log".format(app_config.static_dir_path, str(task_id)), "a") as file:
            file.write(line + "\n")

    page.goto(product_url)
    page.wait_for_load_state("networkidle")
    log("page loaded")

    log("scrolling until button")
    scroll_slowly_to_bottom(page)
    log("button found. clicking")

    page.get_by_text("Смотреть все отзывы").click()
    log("clicked at Смотреть все отзывы")

    time.sleep(2)
    page.wait_for_selector("div.product-feedbacks__main")
    log("feedback page loaded")

    log("start scrolling to comment")
    found = scroll_until_predicate(
        page, lambda paige: is_comment_loaded(paige, comment_text))
    log("end scrolling to bottom. comment found? {}".format(found))

    log("attempt to find comment")
    comment = find_comment(page, comment_text)
    if comment is not None:
        log("comment found.")

        comment.locator("button.feedback__menu").click()
        log("clicked at 3dots")

        time.sleep(2)

        page.get_by_role("button", name="Пожаловаться на отзыв").click()
        log("clicked at Пожаловаться на отзыв")
        time.sleep(2)

        page.get_by_text("Заказной, фиктивный").click()
        log("clicked at Заказной, фиктивный")
        
        time.sleep(2)

        page.get_by_role("button", name="Сообщить").click()
        log("clicked at сообщить")
        log("added report successfully")

    else:
        log("did not find comment")


def is_comment_loaded(page: Page, comment_text: str):
    return page.get_by_text(comment_text).count() == 1


def find_comment(page: Page, text: str):
    comments = page.locator("li.comments__item")
    for i in range(0, comments.count()):

        comment = comments.nth(i)
        comment_text = comment.locator("p.feedback__text").inner_text()
        if text == comment_text:
            return comment
