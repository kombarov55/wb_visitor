from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    page = p.chromium.launch(headless=False).new_page()
    page.pause()
