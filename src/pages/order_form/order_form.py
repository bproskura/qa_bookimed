from allure import step

from src.pages.base_page import BasePage


class OrderForm(BasePage):
    locConfirmPhoneStepTitle: str = "//*[text()='Please verify your phone number']"
    locChooseSpecialityStepTitle: str = "//div//*[contains(text(),'Choose specialty')]"
    locImproveQuestionStepTitle: str = "//*[text()='What would you like to improve?']"
    locImproveQuestionBtn: str = "//button[text()='{}']"
    locSpecialtyBtn: str = "//li//span[text()='{}']"
    locLookingQuestionStepTitle: str = "//*[contains(text(),'What are you looking for now?')]"
    locLookingQuestionBtn: str = "//{0}[contains(text(),'{1}')]"
    locHavePlasticQuestionStepTitle: str = "//*[contains(text(),'Have you already had plastic surgery?')]"
    locHavePlasticQuestionBtn: str = "//button[text()='{}']"
    locPhotoAreaQuestionStepTitle: str = \
        "//*[text()='Do you have a photo of the area you plan to improve with the procedure?']"
    locPhotoUploadQuestionStepTitle: str = \
        "//*[text()='Would you like to upload a photo of the area you plan to improve?']"
    locPhotoAreaQuestionBtn: str = "//{0}[text()='{1}']"
    locTimeQuestionStepTitle: str = "//div[contains(text(),'Do you consider any particular time for the procedure?')]"
    locTimeQuestionBtn: str = "//span[contains(text(), '{}')]"
    locContinueFormBtn: str = "//button[contains(text(), 'Continue')]|//div[contains(text(), 'Continue')]"
    locOfferQuestionStepTitle: str = \
        "//div[contains(text(), 'Would you like to receive offers from relevant clinics?')]"
    locOfferQuestionBtn: str = "//{0}[contains(text(),'{1}')]"
    locNameQuestionStepTitle: str = "//div[contains(text(),'What’s your first name?')]"
    locFirstNameInput: str = "//*[@name='name']"
    locConfirmFormBtn: str = "//div[contains(text(), 'Confirm')]|//button[contains(text(), 'Confirm')]"
    locNiceToMeetStepTitle: str = "//*[contains(text(),'Nice to meet you, {}!')]"
    locEmailStepTitle: str = "//div[contains(text(), 'Enter your email')]"
    locEmailInput: str = "//input[@type='email']"
    locReviewingDataStepTitle: str = "//p[contains(text(),'Reviewing & saving your data')]"
    locSendingDataStepTitle: str = "//p[contains(text(),'Sending request for getting Best price')]"
    locChooseCountryStepTitle: str = \
        "//div[contains(text(),'Choose your preferred country to find clinics for the procedure:')]"
    locCountryQuestionBtn: str = "//div[contains(text(),'{}')]"
    locRequestCallStepTitle: str = "//div[contains(text(), 'Your request is almost ready!')]"
    locPhoneInput: str = "//input[@name='phone']"
    locVerifyPhoneBtn: str = "//button[contains(@class,'phone__button phone')]"
    locVerifyViaSmsBtn: str = "//div[contains(@class,'order-sticky__button')]"
    locVerifyPhoneStepTitle: str = "//div[text()='Please verify your phone number']"
    locSmsCodeInput: str = "//input[@type='tel']"
    locVerifyThxStepTitle: str = \
        "//div[contains(text(), 'Choose the best way to manage and get updates on your requests')]"
    locPhoneSelector: str = "//*[@aria-label='Country Code Selector']"
    locSelectorCountry: str = "//strong[contains(text(), '{}')]"
    locRhinoplastyStepTitle: str = "//*[contains(text(),'Are you interested in rhinoplasty')]"
    locRhinoplastyBtn: str = "//span[contains(text(),'{}')]"
    locRhinoplastyReasonStepTitle: str = \
        "//div[contains(text(),'What is your personal reason for considering a rhinoplasty?')]"
    locRhinoplastyReasonBtn: str = "//span[contains(text(),'{}')]"
    locNotAloneStepTitle: str = "//div[contains(text(),'You’re not alone')]"
    locDiscomfortStepTitle: str = "//div[contains(text(),'Does your nose cause you discomfort or dissatisfaction?')]"
    locDiscomfortBrn: str = "//span[contains(text(),'{}')]"
    locTreatmentStepTitle: str = "//div[contains(text(),'found best treatment with Bookimed')]"
    locTransferStepTitle: str = "//div[contains(text(),'important to you during medical trip?')]"
    locEmojiBtn: str = "(//button[@class='order-button order-button--emojii'])[{}]"
    locMedicalTripStepTitle: str = "//div[contains(text(),'accommodation included for your medical trip')]"

    def __init__(self, page):
        super().__init__(page)

    @step("Выбираем специальность {speciality}")
    def click_on_speciality(self, speciality):
        self.page.locator(self.locSpecialtyBtn.format(speciality)).click()

    @step("Выбираем улучшение {improve}")
    def click_on_improve_question(self, improve):
        self.page.locator(self.locImproveQuestionBtn.format(improve)).click()

    @step("Выбираем {looking}")
    def click_on_looking_question(self, element_type, looking):
        self.page.locator(self.locLookingQuestionBtn.format(element_type, looking)).click()

    @step("Выбираем {answer}")
    def click_on_have_plastic_btn(self, answer):
        self.page.locator(self.locHavePlasticQuestionBtn.format(answer)).click()

    @step("Выбираем {answer}")
    def click_on_photo_area_question(self, element_type, answer):
        self.page.locator(self.locPhotoAreaQuestionBtn.format(element_type, answer)).click()

    @step("Выбираем {answer}")
    def click_on_time_answer(self, answer):
        self.page.locator(self.locTimeQuestionBtn.format(answer)).click()

    @step("Выбираем {answer}")
    def click_on_offer_answer(self, element_type, answer):
        self.page.locator(self.locOfferQuestionBtn.format(element_type, answer)).click()

    @step("Вводим имя {name} и нажимаем Confirm")
    def input_first_name(self, name):
        self.page.locator(self.locFirstNameInput).fill(name)

    @step("Нажимаем Confirm")
    def click_on_confirm_button(self):
        self.click_btn(self.locConfirmFormBtn)

    @step("Вводим почту {email} и нажимаем Confirm")
    def input_email(self, email):
        self.page.locator(self.locEmailInput).fill(email)
        self.click_btn(self.locConfirmFormBtn)

    @step("Выбираем страну {answer} и нажимаем 'Continue'")
    def click_on_country_answer(self, answer):
        self.click_btn(self.locCountryQuestionBtn.format(answer))
        self.click_btn(self.locContinueFormBtn)

    def input_phone(self, phone):
        self.page.locator(self.locPhoneInput).fill(phone)

    @step("Выбираем телефонный код страны")
    def select_country_code(self, country):
        self.page.locator(self.locPhoneSelector).click()
        self.page.locator(self.locSelectorCountry.format(country)).click()

    @step("Вводим смс код")
    def input_sms_code(self, sms_code):
        self.page.locator(self.locSmsCodeInput).fill(sms_code)
        self.page.locator(self.locConfirmFormBtn).click()

    @step("Выбираем {answer}")
    def click_on_rhinoplasty_answer(self, answer):
        self.click_btn(self.locRhinoplastyBtn.format(answer))

    @step("Выбираем {answer}")
    def click_on_rhinoplasty_reason_answer(self, answer):
        self.click_btn(self.locRhinoplastyReasonBtn.format(answer))

    @step("Нажимаем Continue")
    def click_on_continue(self):
        self.click_btn(self.locContinueFormBtn)

    @step("Выбираем {answer}")
    def click_on_discomfort_answer(self, answer):
        self.click_btn(self.locRhinoplastyReasonBtn.format(answer))

    @step("Нажимаем на emojii")
    def click_on_emoji(self, emoji_num):
        self.click_btn(self.locEmojiBtn.format(emoji_num))
