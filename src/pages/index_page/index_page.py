from allure import step

import cfg
from src.pages.base_page import BasePage


class IndexPage(BasePage):
    locRequestCallBtn: str = "//a[contains(text(), 'Request a call')]"
    locOrderForm: str = "//*[@class='order-form']"
    locGetConsultationForm: str = "//*[@class='simple-order__form']"
    locPhoneInput: str = "//*[@name='phone']//input"
    locContactWayDropdown: str = "//*[@class='simple-order__select simple-order__item']"
    locWhatsAppListItem: str = "//li[contains(text(),'WhatsApp')]"
    locNameInput: str = "//*[@id='name']"
    locTermsCheckbox: str = "//*[@id='checkbox']"
    locSendRequestBtn: str = "//*[contains(@class, 'send-button')]"
    locDescriptionTextArea: str = "//*[@name='question']"

    def __init__(self, page):
        super().__init__(page)


    @step("Скролл до блока 'Get a free consultation'")
    def scroll_to_the_form(self, timeout=cfg.WAIT_PAGE_LOAD_TIMEOUT):
        self.page.locator(self.locGetConsultationForm).scroll_into_view_if_needed(timeout=timeout)

    @step("Вводим номер телефона")
    def insert_phone(self, phone: str):
        self.page.locator(self.locPhoneInput).click()
        self.page.locator(self.locPhoneInput).fill(phone)

    @step("Выбираем мессенджер WhatsApp")
    def select_contact_messenger(self):
        self.page.locator(self.locContactWayDropdown).click()
        self.page.locator(self.locWhatsAppListItem).click()

    @step("Вводим имя в поле")
    def insert_name(self, name: str):
        self.page.locator(self.locNameInput).click()
        self.page.locator(self.locNameInput).fill(name)

    @step("Активируем чекбокс с Terms&Conditions")
    def click_terms_checkbox(self):
        self.page.locator(self.locTermsCheckbox).click()

    @step("Нажимаем на 'Send Request'")
    def click_send_request_btn(self):
        self.page.locator(self.locSendRequestBtn).click()

    @step("Вводим описание в поле")
    def insert_description(self, description):
        self.page.locator(self.locDescriptionTextArea).click()
        self.page.locator(self.locDescriptionTextArea).fill(description)
