import time

from playwright.sync_api import Page


def run(page: Page, article: str):
    page.goto("https://wildberries.ru")
    time.sleep(2)
    page.wait_for_load_state("networkidle")

    page.click("span.navbar-pc__icon--basket")

    time.sleep(2)
    page.wait_for_load_state("networkidle")

    good = find(page, article)

    if good is None:
        print("article {} is not in cart".format(article))
    else:
        good.locator("span.good-info__good-name").hover()
        page.pause()
        page.get_by_role("button", name="Удалить").first.click()
        print("success")
    time.sleep(2)


def find(page: Page, article: str):
    goods = page.locator("div.list-item__good")
    for i in range(0, goods.count()):
        good = goods.nth(i)
        href = good.locator("a.good-info__title").get_attribute("href")
        good_article = href.split("/")[2]
        if good_article == article:
            return good
    return None
