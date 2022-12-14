import random
import time

from playwright.sync_api import Page

import playwright_util

queries = [
    "брелок для ауди",
    "бершка",
    "краска светящаяся",
    "кисточка",
    "дерево",
    "bosch",
    "картина",
    "носки",
    "ipone",
    "клетка"
]


def run(page: Page):
    page.goto("https://wb.ru")
    time.sleep(3)

    amount = random.randint(0, 3)
    print("do nothing for {} queries".format(amount))

    for i in range(0, amount):
        page.click("input#searchInput")
        time.sleep(2.5)

        query = random.choice(queries)
        page.type("input#searchInput", query, delay=380)
        time.sleep(2)
        page.keyboard.press("Enter")
        time.sleep(6)
        page.wait_for_selector("div#catalog_sorter")

        playwright_util.scroll_to_y(page, dest_y=600, delay_every_y=500)
        time.sleep(3)
        playwright_util.scroll_to_y(page, dest_y=0, delta=100, interval_between_scrolls=0.2)
        time.sleep(4)
        page.locator("input#searchInput").fill("")
