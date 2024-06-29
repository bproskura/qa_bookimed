from time import sleep

import allure
from playwright.sync_api import Page, expect

from src.pages.index_page.index_page import IndexPage


@allure.parent_suite("Bookimed")
@allure.suite("Заповнення форм")
class TestBookimed:
    @allure.title("Перевірка запиту на дзвінок")
    def test_request_call(self, page: Page):
        index_page = IndexPage(page)

        with allure.step("Переходимо за посиланням"):
            index_page.goto("/")

        with allure.step("Клілкаємо на кнопку Request a call"):
            index_page.click_btn(index_page.locRequestCallBtn)

        with allure.step("Перевіряємо відкриття форми"):
            expect(page.locator(index_page.locOrderForm)).to_be_visible()
            sleep(10)

    @allure.title("Failed test")
    def test_failed(self, page:Page):
        index_page = IndexPage(page)
        with allure.step("Переходимо за посиланням"):
            index_page.goto("/")
        assert 2 == 3

    @allure.title("Pass test")
    def test_pass(self, page:Page):
        index_page = IndexPage(page)
        with allure.step("Переходимо за посиланням"):
            index_page.goto("/")
        assert 2 == 2

    @allure.title("Second failed test")
    def test_request_call_from_home_page(self, page:Page):
        index_page = IndexPage(page)
        with allure.step("Переходимо за посиланням"):
            index_page.goto("/")
        assert 2 == 5

