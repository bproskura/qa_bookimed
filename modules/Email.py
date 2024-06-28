import email
import imaplib
import time

from datetime import datetime, timedelta
from email.header import decode_header, make_header
from email.message import Message

from allure import step

from modules import HtmlParser
from modules.Allure import log_html_to_allure


# noinspection PyBroadException
class Email:

    def __init__(self, auth: dict, smtp_server: str = "imap.gmail.com", wait=5):
        self.wait = wait
        time.sleep(self.wait)
        self.email = auth["email"]
        self.password = auth["password"]
        self.smtp_server = smtp_server

    def get_messages(self, method: str, *args, timedelta_minutes: int, timeout_seconds: int) -> list:
        """
        Retrieves email messages based on a specified method and arguments, within a certain time frame.

        Args:
            method (str): The name of the method to be used for retrieving messages.
            *args: The arguments to be passed to the method.
            timedelta_minutes (int): The time frame in minutes within which to retrieve messages.
            timeout_seconds (int, optional): The maximum time in seconds to wait for messages. Defaults to 20.

        Returns:
            list: A list of retrieved email messages.

        Raises:
            TimeoutError: If no messages are found within the specified timeout.
        """
        from_time = (datetime.today() - timedelta(minutes=timedelta_minutes)).strftime("%d.%m.%Y %H:%M:%S")
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout_seconds)
        with EmailLib(self.email, self.password, self.smtp_server) as mail:
            while datetime.now() < end_time:
                messages = getattr(mail, method)(*args, from_time)
                if messages:
                    return messages
                time.sleep(self.wait)
                continue
        raise TimeoutError(f"\nMessages not found during {timeout_seconds} seconds"
                           f"\nFrom {start_time.strftime('%H:%M:%S')} to {end_time.strftime('%H:%M:%S')}")

    @step("get_messages_by_addresses")
    def get_msgs_by_addresses(self, to_addr: str = "",
                              from_addr: str = "test@slotoking.com",
                              timedelta_minutes: int = 2,
                              timeout_seconds=20,
                              ) -> list:
        return self.get_messages("get_msgs_with_addresses",
                                 from_addr, to_addr,
                                 timedelta_minutes=timedelta_minutes,
                                 timeout_seconds=timeout_seconds)

    @step("get_messages_by_subject")
    def get_messages_by_subject(self, subject: str,
                                timedelta_minutes: int, timeout_seconds=20,
                                ) -> list:
        return self.get_messages("get_messages_with_subject",
                                 subject,
                                 timedelta_minutes=timedelta_minutes,
                                 timeout_seconds=timeout_seconds)

    @step("get_message_content")
    def get_message_content(self, msg: Message):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get("Content-Disposition"))
                # skip any text/plain (txt) attachments
                if ctype == "text/plain" and "attachment" not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
        else:
            body = msg.get_payload(decode=True)
        content = body.decode("utf-8")
        log_html_to_allure(content, name="message")
        return content

    @step("get_text_by_xpath")
    def get_text_by_xpath(self, msg: Message, xpath: str) -> str:
        """ Обязательно нужен xpath элемента с текстом, а НЕ элемент содержащий нужный элемент с текстом """
        html = self.get_message_content(msg)
        return HtmlParser.return_text_from_html(html, xpath)

    @step("get_href_by_xpath")
    def get_href_by_xpath(self, msg: Message, xpath: str) -> str:
        """ Обязательно нужен xpath элемента с href, а НЕ элемент содержащий нужный элемент с href """
        html = self.get_message_content(msg)
        return HtmlParser.return_href_from_html(html, xpath)

    @step("get_all_links_list_by_xpath")
    def get_all_links_by_xpath(self, msg: Message, xpath: str = "//a") -> list:
        html = self.get_message_content(msg)
        return HtmlParser.return_hrefs_from_html(html, xpath)


class EmailLib:

    def __init__(self, login: str, password: str, smtp_server: str):
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.mail = None

    def __enter__(self):
        self.mail = imaplib.IMAP4_SSL(self.smtp_server)
        self.authentication()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mail.logout()
        self.mail = None

    def authentication(self):
        try:
            self.mail.login(self.login, self.password)
        except Exception as e:
            raise Exception(f"Authentication failed: {repr(e)}")

    def get_mail_by_id(self, msg_id: str) -> Message:
        status, content = self.mail.fetch(msg_id, "(RFC822)")
        if status == "OK":
            return email.message_from_bytes(content[0][1])

    def get_msgs_from_time(self, ids: list, from_time: str) -> list:
        from dateutil.parser import (parse, parserinfo)  # noqa
        result_msgs = []
        for msg_id in ids:
            msg = self.get_mail_by_id(msg_id)
            msg_time = _get_message_date(msg)
            if parse(msg_time, parserinfo(True, False)) >= parse(from_time, parserinfo(True, False)):
                result_msgs.append(msg)
            else:
                break
        return result_msgs

    def get_msgs_with_addresses(self, from_addr: str, to_addr: str, from_time: str) -> list:
        self.mail.select("inbox")
        status, content = self.mail.search(None, "ALL")  # noqa: F841
        messages_ids = content[0].split()
        messages_ids.reverse()
        result_msgs = []
        for msg in self.get_msgs_from_time(messages_ids, from_time):
            if from_addr in msg["from"] and to_addr in msg["to"]:
                result_msgs.append(msg)
        return result_msgs

    def get_messages_with_subject(self, subject: str, from_time: str) -> list:
        self.mail.select("inbox")
        status, content = self.mail.search(None, "ALL")  # noqa: F841
        messages_ids = content[0].split()
        messages_ids.reverse()
        result_msgs = []
        for msg in self.get_msgs_from_time(messages_ids, from_time):
            # print("__________________________________")
            # print('Msg')
            # print('message date: ' + _get_message_date(msg))
            # print('message subject: ' + _get_message_subject(msg))
            # print('message from: ' + __decode_content__(msg['from']))
            # print('message to: ' + msg['to'])
            # print("__________________________________")
            if subject in _get_message_subject(msg):
                result_msgs.append(msg)
        return result_msgs


def __decode_content__(content: str) -> str:
    return str(make_header(decode_header(content)))


def _get_message_subject(msg: Message) -> str:
    _msg_subject = str(msg["subject"])
    msg_subject = __decode_content__(_msg_subject)
    return msg_subject


def _get_message_date(msg: Message) -> str:
    date_tuple = email.utils.parsedate_tz(msg['date'])  # noqa
    date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))  # noqa
    return "{:%d.%m.%Y %H:%M:%S}".format(date)
