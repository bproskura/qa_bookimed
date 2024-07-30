import os
import allure
import pytest
import time
from playwright.sync_api import Page, expect

import cfg
from data import order_id_manager
from src.pages.index_page.index_page import IndexPage
from src.pages.order_form.order_form import OrderForm
from src.pages.procedure_page.procedure_page import ProcedurePage


@pytest.fixture(scope="function", autouse=True)
def delay_between_tests():
    yield
    time.sleep(130)


order_ids_file = os.path.join('results', 'order_ids.xml')
order_id_manager = order_id_manager.OrderIDManager(order_ids_file)


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    # Создаем папку, если она не существует
    if not os.path.exists('results'):
        os.makedirs('results')
    yield


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
            order_form.page.wait_for_timeout(3000)
            order_form.select_country_code("Ukraine")
            order_form.page.wait_for_timeout(3000)
            index_page.insert_phone(cfg.PHONE)
            order_form.page.wait_for_timeout(3000)
            index_page.select_contact_messenger()
            order_form.page.wait_for_timeout(3000)
            index_page.insert_name("teratst")
            order_form.page.wait_for_timeout(3000)
            index_page.insert_description("test")
            order_form.page.wait_for_timeout(3000)
            index_page.click_terms_checkbox()
            order_form.page.wait_for_timeout(3000)
            index_page.click_send_request_btn()

            with allure.step("Проверяем отображение формы ввода смс"):
                expect(order_form.page.locator(order_form.locConfirmPhoneStepTitle)).to_be_visible(
                    timeout=cfg.WAIT_PAGE_LOAD_TIMEOUT)
            with allure.step("Извлекаем order_id из URL и проверяем диапазон"):
                current_url = page.url
                page.wait_for_timeout(5000)
                assert order_id_manager.validate_order_id(
                    current_url, "test_order_from_homepage") is True, "Order id in fake range"
                # order_form.page.wait_for_timeout(5000)
                # order_form.input_sms_code(cfg.SMS_CODE)
                # expect(order_form.page.locator(order_form.locVerifyThxStepTitle)).to_be_visible()

    @allure.title("Форма 'Request a call' на 435-ю клинику")
    def test_order_for_clinic(self, page: Page, fake):
        index_page = IndexPage(page)
        order_form = OrderForm(page)

        with allure.step("Переходимо за посиланням"):
            index_page.goto("/")

        with allure.step("Кликаем на Request a call"):
            index_page.click_btn(index_page.locRequestCallBtn)

        with allure.step("Заполняем форму"):
            expect(order_form.page
                   .locator(order_form.locChooseSpecialityStepTitle)).to_be_visible(timeout=cfg.WAIT_PAGE_LOAD_TIMEOUT)
            order_form.click_on_speciality("Plastic Surgery")
            expect(order_form.page.locator(order_form.locImproveQuestionStepTitle)).to_be_visible()
            order_form.click_on_improve_question("A nose")
            expect(order_form.page.locator(order_form.locLookingQuestionStepTitle)).to_be_visible()
            order_form.click_on_looking_question("button", "Best price")
            expect(order_form.page.locator(order_form.locHavePlasticQuestionStepTitle)).to_be_visible()
            order_form.click_on_have_plastic_btn("No")
            expect(order_form.page.locator(order_form.locPhotoAreaQuestionStepTitle)).to_be_visible()
            order_form.click_on_photo_area_question("button", "No")
            expect(order_form.page.locator(order_form.locTimeQuestionStepTitle)).to_be_visible()
            order_form.click_on_time_answer("As soon as possible")
            order_form.click_on_continue()
            expect(order_form.page.locator(order_form.locOfferQuestionStepTitle)).to_be_visible()
            order_form.click_on_offer_answer("div", "Yes")
            expect(order_form.page.locator(order_form.locNameQuestionStepTitle)).to_be_visible()
            order_form.input_first_name("teratst")
            order_form.click_on_confirm_button()
            expect(order_form.page.locator(order_form.locNiceToMeetStepTitle.format("teratst"))).to_be_visible()
            expect(order_form.page.locator(order_form.locEmailStepTitle)).to_be_visible()
            order_form.input_email("teratst@gmail.com")
            expect(order_form.page.locator(order_form.locReviewingDataStepTitle)).to_be_visible()
            expect(order_form.page.locator(order_form.locSendingDataStepTitle)).to_be_visible()
            expect(order_form.page.locator(order_form.locChooseCountryStepTitle)).to_be_visible()
            order_form.click_on_country_answer("Turkey")
            expect(order_form.page.locator(order_form.locRequestCallStepTitle)).to_be_visible()
            order_form.page.wait_for_timeout(3000)
            order_form.select_country_code("Ukraine")
            order_form.input_phone(cfg.PHONE)
            order_form.page.locator(order_form.locVerifyPhoneBtn).click()
            expect(order_form.page
                   .locator(order_form.locVerifyPhoneStepTitle)).to_be_visible(timeout=cfg.WAIT_PAGE_LOAD_TIMEOUT)
            with allure.step("Извлекаем order_id из URL и проверяем диапазон"):
                current_url = page.url
                page.wait_for_timeout(5000)
                assert order_id_manager.validate_order_id(
                    current_url, "test_order_for_clinic") is True, "Order id in fake range"

            # order_form.input_sms_code(cfg.SMS_CODE)
            # expect(order_form.page.locator(order_form.locVerifyThxStepTitle)).to_be_visible()

    @allure.title("Форма 'Процедура' + клиника (без фото)")
    def test_order_for_procedure(self, page: Page):
        slug: str = "/clinics/procedure=rhinoplasty-nose-job/"
        procedure_page = ProcedurePage(page)
        order_form = OrderForm(page)

        with allure.step("Переходим по ссылке на страницу процедуры"):
            procedure_page.goto(slug)

        with allure.step("Проверяем переход на страницу с процедурой"):
            expect(procedure_page.get_page()).to_have_url(cfg.BASE_URL + slug)
            assert procedure_page.pageTitle.lower() in procedure_page.get_page_title().lower()

        with allure.step("Кликаем на первой карточке клиники 'Get free quote'"):
            procedure_page.click_on_get_free_quote()

        with (allure.step("Заполняем форму")):
            expect(order_form.page.locator(order_form.locRhinoplastyStepTitle)).to_be_visible()
            order_form.click_on_rhinoplasty_answer("Yes")
            expect(order_form.page.locator(order_form.locRhinoplastyReasonStepTitle)).to_be_visible()
            order_form.click_on_rhinoplasty_reason_answer("Improve breathing")
            expect(order_form.page.locator(order_form.locNotAloneStepTitle)).to_be_visible()
            order_form.click_on_continue()
            expect(order_form.page.locator(order_form.locDiscomfortStepTitle)).to_be_visible()
            order_form.click_on_discomfort_answer("Yes")
            expect(order_form.page.locator(order_form.locTreatmentStepTitle))
            order_form.click_on_continue()
            expect(order_form.page.locator(order_form.locLookingQuestionStepTitle)).to_be_visible()
            order_form.click_on_looking_question("span", "Best Surgeon")
            expect(order_form.page.locator(order_form.locTransferStepTitle)).to_be_visible()
            order_form.click_on_emoji("4")
            order_form.click_on_continue()
            expect(order_form.page.locator(order_form.locMedicalTripStepTitle)).to_be_visible()
            order_form.click_on_emoji("4")
            order_form.click_on_continue()
            expect(order_form.page.locator(order_form.locTimeQuestionStepTitle)).to_be_visible()
            order_form.click_on_time_answer("As soon as possible")
            expect(order_form.page.locator(order_form.locOfferQuestionStepTitle)).to_be_visible()
            order_form.click_on_offer_answer("span", "Yes")
            expect(order_form.page.locator(order_form.locNameQuestionStepTitle)).to_be_visible()
            order_form.input_first_name("teratst")
            order_form.click_on_continue()
            expect(order_form.page.locator(order_form.locNiceToMeetStepTitle.format("teratst"))).to_be_visible()
            expect(order_form.page.locator(order_form.locPhotoUploadQuestionStepTitle)).to_be_visible()
            order_form.click_on_photo_area_question("span", "No, I will do it later")
            expect(order_form.page.locator(order_form.locEmailStepTitle)).to_be_visible()
            order_form.input_email("teratst@gmail.com")
            expect(order_form.page
                   .locator(order_form.locRequestCallStepTitle)).to_be_visible(timeout=cfg.WAIT_MAX_PAGE_LOAD_TIMEOUT)
            order_form.page.wait_for_timeout(3000)
            order_form.select_country_code("Ukraine")
            order_form.input_phone(cfg.PHONE)
            order_form.page.locator(order_form.locVerifyViaSmsBtn).click()
            expect(order_form.page
                   .locator(order_form.locVerifyPhoneStepTitle)).to_be_visible(timeout=cfg.WAIT_PAGE_LOAD_TIMEOUT)

            with allure.step("Извлекаем order_id из URL и проверяем диапазон"):
                current_url = page.url
                page.wait_for_timeout(5000)
                assert order_id_manager.validate_order_id(
                    current_url, "test_order_for_procedure") is True, "Order id in fake range"
