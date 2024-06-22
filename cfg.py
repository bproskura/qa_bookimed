import os

from dotenv import load_dotenv

load_dotenv(override=False)

# ### SECURITY TOKENS ###
TG_BOT_TOKEN: str = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
KING_URL = "https://slotoking.ua"
SEVENS_URL = "https://777.ua"
FUNRIZE_URL = "https://funrize.com"
KING_LANDINGS_URL = {
    "kg-best": "https://kg-best-spin.lets-fun.top",
    "kg-bonus": "https://kg-bonus.fun-spin.top",
    "kg-fortune": "https://kg-fortune-boxes.fun-spin.top",
    "kg-lucky-bonus": "https://kg-lucky-bonus.lets-fun.top",
    "kg-lucky-wheel": "https://kg-lucky-wheel.fun-spin.top",
    "kg-welcome": "https://kg-welcome.lets-fun.top",
    "kg-prize": "https://kg-prize.lets-fun.top",
    "kg-slot": "https://kg-slot.lets-fun.top/",
}

SEVENS_LANDINGS_URL = {
    "lady-wheel": "https://777-lady-wheel.lets-fun.top",
    "adventure-wheel": "https://777-adventure-wheel.lets-fun.top",
    "welcome-lets": "https://777-welcome.lets-up.fun",
    "welcome-bonus": "https://777_welcome_bonus_pack.lets-fun.top",
}

FUNRIZE_LANDINGS_URL = {
    "funrize_lp_one": "https://promo.funrize.com/lp1",
    "funrize_lp_two": "https://promo.funrize.com/lp2",
    "funrize_lp_three": "https://promo.funrize.com/lp3",
    "funrize_lp_four": "https://promo.funrize.com/lp4",
}

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
