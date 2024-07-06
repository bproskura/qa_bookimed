from allure import step
from playwright.sync_api import Page

import cfg
from src.pages.base_page import BasePage


class ProcedurePage(BasePage):
    pageTitle: str = "Rhinoplasty"

    def __init__(self, page):
        super().__init__(page)

    @step("Забираем заголовок страницы")
    def get_page_title(self) -> str:
        return self.get_page().title()
