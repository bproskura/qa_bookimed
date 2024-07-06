from allure import step
from playwright.sync_api import Page

import cfg


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @step("goto {endpoint}")
    def goto(self, endpoint: str) -> None:
        self.page.goto(cfg.BASE_URL + endpoint)

    @step("click button")
    def click_btn(self, locator: str) -> None:
        self.page.locator(locator).click()

    @step("get page")
    def get_page(self) -> Page:
        return self.page
