import time

from playwright.sync_api import Page

import playwright_util


def look_at_article(page: Page, search_str: str, article: str):
    page.goto("https://wb.ru")
    page.wait_for_selector("div.img-plug")
    page.click("input#searchInput")
    page.type("input#searchInput", search_str, delay=150)
    time.sleep(1)
    page.keyboard.press("Enter")
    page.wait_for_selector("div#catalog_sorter")
    card = find_card(page, article)
    if card is not None:
        playwright_util.scroll_to_element(page, card)
        time.sleep(2)
        card.click()
        time.sleep(5)
    else:
        print("ERROR, card not found. search_str={} article={}".format(search_str, article))


def find_card(page: Page, article: str):
    cards = page.locator("div.product-card__wrapper")
    for i in range(0, cards.count()):
        card = cards.nth(i)
        href = card.locator("a.j-card-link").get_attribute("href")
        card_article = href.split("/")[4]
        if card_article == article:
            return card
    return None


def test(page: Page):
    look_at_article(page, "хутер", "28280119")
