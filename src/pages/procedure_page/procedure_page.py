from allure import step
from playwright.sync_api import Page

import cfg
from src.pages.base_page import BasePage


class ProcedurePage(BasePage):
    pageTitle: str = "Rhinoplasty"
    locGetFreeQuoteBtn: str = "(//*[@class='offer-card__request-btn'])[1]"

    def __init__(self, page):
        super().__init__(page)

    @step("Забираем заголовок страницы")
    def get_page_title(self) -> str:
        return self.get_page().title()

    def click_on_get_free_quote(self):
        self.click_btn(self.locGetFreeQuoteBtn)
