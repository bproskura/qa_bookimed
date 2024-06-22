import os

from dotenv import load_dotenv

load_dotenv(override=False)

# ### SECURITY TOKENS ###
TG_BOT_TOKEN: str = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
BASE_URL: str = "https://us-uk.bookimed.com"

LANDINGS_SET_COOKIE = "__gmbrV2"
WAIT_PAGE_LOAD_TIMEOUT = 10000
WAIT_MAX_PAGE_LOAD_TIMEOUT = 15000
BROWSER: str = os.getenv("BROWSER", default="chrome")
HEADLESS: str = os.getenv("HEADLESS", default="False")
SCREEN_WIDTH, SCREEN_HEIGHT = os.getenv("SCREEN_WIDTH", "1440"), os.getenv("SCREEN_HEIGHT", "768")
DEFAULT_LOCALE: str = os.getenv("DEFAULT_LOCALE", default="uk-UA")
DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", default="Europe/Kiev")
UA_EXISTING_EMAIL: str = os.getenv("SKG_EXISTING_EMAIL")
UA_EXISTING_PHONE: str = os.getenv("SKG_EXISTING_PHONE")
EXISTING_PASSWORD: str = os.getenv("SKG_PASSWORD")
MOBILE_DEVICE: str = os.getenv("MOBILE_DEVICE", default="iPhone 11")


class Email:
    def __init__(self, email: str, password: str, gmail_pwd: str):
        self.AUTH = dict({"email": email, "password": password})
        self.GMAIL_PWD = gmail_pwd
        self.EMAIL_NAME = (email.split("@"))[0]
        self.EMAIL_DOMAIN = (email.split("@"))[1]


EMAIL_QA = Email(email="autotests@cleack.com",
                 password=os.getenv("APP_GMAIL_PASSWORD"),
                 gmail_pwd=os.getenv("GMAIL_PASSWORD"))
