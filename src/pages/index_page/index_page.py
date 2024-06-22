from src.pages.base_page import BasePage


class IndexPage(BasePage):
    locRequestCallBtn: str = "//a[contains(text(), 'Request a call')]"
    locOrderForm: str = "//*[@class='order-form']"

    def __init__(self, page):
        super().__init__(page)