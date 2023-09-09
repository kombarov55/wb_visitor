from actions import add_report
from playwright.sync_api import sync_playwright

with sync_playwright() as p: 
    page = p.chromium.launch(headless=False).new_page()
    add_report.run(page, "https://www.wildberries.ru/catalog/2695363/detail.aspx", "Товар пришел хорошо упакован, спасибо.")
