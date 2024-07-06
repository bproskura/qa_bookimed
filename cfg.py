import os
from dotenv import load_dotenv

load_dotenv(override=False)

# Slack webhook URL
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

# Other configuration settings
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
BASE_URL = os.getenv("BASE_URL")
LANDINGS_SET_COOKIE = "__gmbrV2"
WAIT_PAGE_LOAD_TIMEOUT = 10000
WAIT_MAX_PAGE_LOAD_TIMEOUT = 15000
BROWSER = os.getenv("BROWSER", default="chrome")
HEADLESS = os.getenv("HEADLESS", default="False")
SCREEN_WIDTH = os.getenv("SCREEN_WIDTH", "1440")
SCREEN_HEIGHT = os.getenv("SCREEN_HEIGHT", "768")
DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", default="uk-UA")
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", default="Europe/Kiev")
UA_EXISTING_EMAIL = os.getenv("SKG_EXISTING_EMAIL")
UA_EXISTING_PHONE = os.getenv("SKG_EXISTING_PHONE")
EXISTING_PASSWORD = os.getenv("SKG_PASSWORD")
MOBILE_DEVICE = os.getenv("MOBILE_DEVICE", default="iPhone 11")
PHONE = os.getenv("PHONE")
SMS_CODE = os.getenv("SMS_CODE")


class Email:
    def __init__(self, email: str, password: str, gmail_pwd: str):
        self.AUTH = {"email": email, "password": password}
        self.GMAIL_PWD = gmail_pwd
        self.EMAIL_NAME = email.split("@")[0]
        self.EMAIL_DOMAIN = email.split("@")[1]


EMAIL_QA = Email(
    email="autotests@cleack.com",
    password=os.getenv("APP_GMAIL_PASSWORD"),
    gmail_pwd=os.getenv("GMAIL_PASSWORD")
)
