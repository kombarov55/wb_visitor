import time

from playwright.sync_api import Page


def run(page: Page, article: str):
    page.goto("https://wildberries.ru")
    time.sleep(4)
    page.wait_for_load_state("networkidle")

    page.click("span.navbar-pc__icon--profile")

    time.sleep(3)
    page.wait_for_load_state("networkidle")

    page.click("a.lk-item--favorites")

    time.sleep(3)
    page.wait_for_load_state("networkidle")

    item = find(page, article)
    if item is None:
        print("article {} is not in favorites".format(article))
    else:
        item.hover()
        item.locator("span.achtung-icon-white").click()
        print("success")
        time.sleep(2)


def find(page: Page, article: str):
    items = page.locator("div.goods-card__container")

    for i in range(0, items.count()):
        item = items.nth(i)
        href = item.locator("a.j-product-popup").get_attribute("href")
        item_article = href.split("/")[2]
        if item_article == article:
            return item
    return None
