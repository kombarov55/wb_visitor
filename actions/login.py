from playwright.sync_api import Page


def login(page: Page):
    page.goto("https://wb.ru")
    page.wait_for_load_state("networkidle")
    page.click("a.j-main-login")


def test():
    pass
