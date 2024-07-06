import allure
from playwright.sync_api import Page, expect

import cfg
from src.pages.index_page.index_page import IndexPage
from src.pages.order_form.order_form import OrderForm
from src.pages.procedure_page.procedure_page import ProcedurePage


@allure.parent_suite("Bookimed")
@allure.suite("Заповнення форм")
class TestBookimed:
    @allure.title("Открытая форма на главной")
    def test_order_from_homepage(self, page: Page, fake):
        index_page = IndexPage(page)
        order_form = OrderForm(page)

        with allure.step("Переходим на главную"):
            index_page.goto("/")
            page.reload()

        with allure.step("Скролл до блока 'Get a free consultation'"):
            index_page.scroll_to_the_form()

        with allure.step("Вводим контактные данные"):
            index_page.insert_phone(cfg.PHONE)
            index_page.select_contact_messenger()
            index_page.insert_name("teratst")
            index_page.insert_description("test")
            index_page.click_terms_checkbox()
            index_page.click_send_request_btn()

        with allure.step("Проверяем отображение формы ввода смс"):
            expect(order_form.page.locator(order_form.locConfirmPhoneStepTitle)).to_be_visible(
                timeout=cfg.WAIT_PAGE_LOAD_TIMEOUT)
            page.wait_for_timeout(5000)

    @allure.title("Форма 'Request a call' на 435-ю клинику")
    def test_order_for_clinic(self, page: Page, fake):
        index_page = IndexPage(page)
        order_form = OrderForm(page)

        with allure.step("Переходимо за посиланням"):
            index_page.goto("/")

        with allure.step("Кликаем на Request a call"):
            index_page.click_btn(index_page.locRequestCallBtn)

        with allure.step("Заполняем форму"):
            expect(order_form.page.locator(order_form.locChooseSpecialityStepTitle)).to_be_visible()
            order_form.click_on_speciality("Plastic Surgery")
            expect(order_form.page.locator(order_form.locImproveQuestionStepTitle)).to_be_visible()
            order_form.click_on_improve_question("A nose")
            expect(order_form.page.locator(order_form.locLookingQuestionStepTitle)).to_be_visible()
            order_form.click_on_looking_question("Best price")
            expect(order_form.page.locator(order_form.locHavePlasticQuestionStepTitle)).to_be_visible()
            order_form.click_on_have_plastic_btn("No")
            expect(order_form.page.locator(order_form.locPhotoAreaQuestionStepTitle)).to_be_visible()
            order_form.click_on_photo_area_question("No")
            expect(order_form.page.locator(order_form.locTimeQuestionStepTitle)).to_be_visible()
            order_form.click_on_time_answer("As soon as possible")
            expect(order_form.page.locator(order_form.locOfferQuestionStepTitle)).to_be_visible()
            order_form.click_on_offer_answer("Yes")
            expect(order_form.page.locator(order_form.locNameQuestionStepTitle)).to_be_visible()
            order_form.input_first_name("teratst")
            expect(order_form.page.locator(order_form.locNiceToMeetStepTitle.format("teratst"))).to_be_visible()
            expect(order_form.page.locator(order_form.locEmailStepTitle)).to_be_visible()
            order_form.input_email("teratst@gmail.com")
            expect(order_form.page.locator(order_form.locReviewingDataStepTitle)).to_be_visible()
            expect(order_form.page.locator(order_form.locSendingDataStepTitle)).to_be_visible()
            expect(order_form.page.locator(order_form.locChooseCountryStepTitle)).to_be_visible()
            order_form.click_on_country_answer("Ukraine")
            expect(order_form.page.locator(order_form.locRequestCallStepTitle)).to_be_visible()
            order_form.input_phone(cfg.PHONE)
            order_form.page.locator(order_form.locVerifyPhoneBtn).click()

    @allure.title("Форма 'Процедура' + клиника (без фото)")
    def test_order_for_procedure(self, page: Page):
        slug: str = "/clinics/procedure=rhinoplasty-nose-job/"
        procedure_page = ProcedurePage(page)

        with allure.step("Переходим по ссылке на страницу процедуры"):
            procedure_page.goto(slug)

        with allure.step("Проверяем переход на страницу процедурой"):
            expect(procedure_page.get_page()).to_have_url(cfg.BASE_URL + slug)
            assert procedure_page.pageTitle.lower() in procedure_page.get_page_title().lower()
