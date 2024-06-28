import datetime
import random
import time

from allure import step
from faker import Faker  # https://faker.readthedocs.io/en/stable/

import cfg


class Fake:

    def __init__(self, locale="uk_UA"):
        self.fake = Faker(locale=locale)

    @property
    @step("get_fake_password")
    def password(self):
        return self.fake.password(length=6, special_chars=False)

    @property
    @step("get_real_email")
    def get_real_email(self):
        return f"{cfg.EMAIL_QA.EMAIL_NAME}+{int(time.time())}@{cfg.EMAIL_QA.EMAIL_DOMAIN}"

    @property
    @step("get_fake_email")
    def email(self) -> str:
        return self.fake.email(safe=True)

    @property
    @step("Random phone")
    def random_phone(self) -> str:
        return f"{self.fake.country_calling_code()}{self.fake.random_number(digits=9)}"

    @step("Generate Random UA phone")
    def random_ua_phone(self, safe: bool = False) -> str:
        if safe:
            operator_code = (44,)
        else:
            operator_code = (68, 67, 63, 98, 50, 44, 99, 93)
        num = str(time.time()).replace(".", "")[-7:]
        return f"{random.choice(operator_code)}{num}"

    @property
    @step("Get first name")
    def first_name(self) -> str:
        return self.fake.first_name()

    @property
    @step("Get last name")
    def last_name(self) -> str:
        return self.fake.last_name()

    @step("Get random date of birth")
    def random_date_of_birth(self, minimum_age: int = 21, maximum_age: int = 50) -> str:
        return str(self.fake.date_of_birth(minimum_age=minimum_age, maximum_age=maximum_age))

    @property
    @step("Generate Postal code")
    def random_postalcode(self) -> str:
        return self.fake.postcode()

    @property
    @step("Generate address")
    def random_address(self) -> str:
        """
        :return: Ex: '398 Wallace Ranch Suite 593\nIvanburgh, AZ 80818'
        """
        return self.fake.address()

    @property
    @step("Generate street address")
    def random_street_address(self) -> str:
        """
        :return: Ex: '778 Brown Plaza' '60975 Jessica Squares'
        """
        return self.fake.street_address()

    @property
    @step("Random region")
    def get_region(self) -> str:
        return self.fake.region()

    @property
    @step("Random city name")
    def get_city_name(self) -> str:
        return self.fake.city_name()

    @property
    @step("Random street name")
    def get_street_name(self) -> str:
        return self.fake.street_name()

    @step("Get Card num")
    def get_bank_card_num(self, provider="visa"):
        # providers 'amex', 'diners', 'discover', 'jcb', 'jcb15', 'jcb16',
        # 'maestro', 'mastercard', 'visa', 'visa13', 'visa16', 'visa19'.
        return self.fake.credit_card_number(card_type=provider)

    @step("get_fake_string")
    def string(self, charts: int = 10) -> str:
        letters_list = self.fake.random_letters(length=charts)
        string = "".join([i for i in letters_list])
        return string

    @step("get_fake_sentence")
    def sentence(self, words: int = 10) -> str:
        return self.fake.sentence(nb_words=words)

    @property
    @step("Get random word")
    def random_word(self) -> str:
        return self.fake.word()

    @step("get_fake_number")
    def number(self, digits: int = 10) -> int:
        return self.fake.random_number(digits=digits, fix_len=True)

    @step("get_random_number_in_range")
    def get_random_number_in_range(self, start: int, end: int) -> int:
        return random.randint(start, end)

    @property
    @step("get_today")
    def get_today(self):
        return datetime.date.today()

    @step("random_number_in_range")
    def random_number_in_range(self, min_num: int = 0, max_num: int = 9999) -> int:
        return self.fake.pyint(min_num, max_num)

    @step("random_float")
    def random_float(self, a: float, b: float, float_format=2) -> float:
        value = "{:." + str(float_format) + "f}"
        return float(value.format(random.uniform(a, b)))

    @property
    @step("Get random url")
    def random_url(self) -> str:
        return self.fake.url()

    @step("Get random image url")
    def random_img_url(self, width: int = None, height: int = None) -> str:
        return self.fake.image_url(width, height)

    @step("Create random image")
    def create_image(self, size: tuple = (2880, 1920), img_format: str = "png"):
        color_list = ["monochrome", "red", "orange", "yellow", "green", "blue", "purple", "pink"]
        color = random.choice(color_list)
        return self.fake.image(size=size, hue=color, luminosity="bright", image_format=img_format)

    @property
    @step("Generate uuid4")
    def random_uuid4(self) -> str:
        return self.fake.uuid4()


if __name__ == "__main__":
    f = Fake()
    print(f.get_city_name)
