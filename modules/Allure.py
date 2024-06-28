import json
from datetime import datetime
from os import path, makedirs

import allure
from bs4 import BeautifulSoup


def add_description_html(item):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    copy_icon = '<span style="margin: 9px 4px 9px 0; cursor: pointer" class="fa fa-files-o" data-copy="{data}"></span>'
    href_tpl = copy_icon + '<a href="{link}" target="_blank">{text}</a>'
    text = f"""<h4 style="margin: -10px 0 5px;">{copy_icon.format(data=item.name)}{item.name}</h4>
    Collected at <span class="label label_status_passed">{date_now}</span><br><br>"""

    try:
        for line in item.function.__doc__.split('\n'):
            line = line.strip()
            match line:
                case line if line.startswith('http'):
                    kwargs = {'data': line.split()[0], 'link': line.split()[0], 'text': line}
                    text += f'{href_tpl.format(**kwargs)}<br>'
                case line if line != '':
                    text += f'{line}<br>'
    except Exception:  # noqa
        pass
    item.add_marker(allure.description_html(text))


def add_allure_environment_properties(alluredir: str = None, properties: dict = None) -> None:
    if alluredir and properties:
        makedirs(alluredir, exist_ok=True)
        allure_env_path = path.join(alluredir, "environment.properties")
        with open(allure_env_path, 'w') as f:
            f.write('\n'.join([f'{variable}={value}' for variable, value in properties.items()]))


def log_location(url: str) -> None:
    allure.attach(url,
                  name="Location",
                  attachment_type=allure.attachment_type.URI_LIST)


def log_screenshot(screenshot, name: str = "Screenshot") -> None:
    allure.attach(screenshot,
                  name=name,
                  attachment_type=allure.attachment_type.PNG)


def log_html_to_allure(content: str, name: str) -> None:
    allure.attach(content,
                  name=f"{name}_content",
                  attachment_type=allure.attachment_type.HTML)


def log_text_to_allure(text, name: str = 'value') -> None:
    allure.attach(str(text),
                  name=name,
                  attachment_type=allure.attachment_type.TEXT)


def take_log_file_to_allure(file_path: str) -> None:
    with open(file_path) as f:
        allure.attach(
            f.read(),
            name='LogFile',
            attachment_type=allure.attachment_type.TEXT
        )


def log_response_to_allure(resp) -> None:
    try:
        allure.attach(_html_format(resp),
                      name=f"{resp.status_code} {resp.request.method} {resp.url}",
                      attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass


def log_console_entire_to_allure(entire) -> None:
    entire_time = datetime.fromtimestamp(entire['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    allure.attach(__dict_to_html(entire),
                  name=f"Console entire ({entire['level']}) - {entire_time}",
                  attachment_type=allure.attachment_type.HTML)


def log_json_allure_to_allure(entire) -> None:
    res = [{
        **item,
        'timestamp': datetime.fromtimestamp(item['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    } for item in entire]

    allure.attach(json.dumps(res, indent=4), 'Console Errors', allure.attachment_type.JSON)


def _html_format(resp) -> str:
    if isinstance(resp.request.body, bytes):
        request_body = resp.request.body.decode('utf-8')
    else:
        request_body = resp.request.body
    _html = f"""
    <div style="border:solid;border-color:#41444e;border-radius:10px;background-color:#EBF3FB;padding:10px;white-space:normal">
        <div>
            {__h1_to_html(f"{resp.request.method} Request")}
            <div style="width:96%;padding:15px;border-radius:10px;background:#41444e;color:#fff;">{resp.request.url}</div>
            {__h2_to_html("Request headers")}
            {__dict_to_html(resp.request.headers)}
            {__h2_to_html("Request cookies")}
            {__dict_to_html(resp.request._cookies.get_dict())}
            {__h2_to_html("Request body")}
            {__dict_to_html(request_body)}
        </div>
        <hr>
        <div>
            {__h1_to_html("Response")}
            {__status_code_to_html(resp.status_code)}
            {__h2_to_html(f"{resp.elapsed.total_seconds()} total seconds")}
            {__h2_to_html("Response headers")}
            {__dict_to_html(resp.headers)}
            {__h2_to_html("Response cookies")}
            {__dict_to_html(resp.cookies.get_dict())}
            {__h2_to_html("Response body")}
            {__data_to_html(resp)}
        </div>
    </div>
    """
    return _html


def __h1_to_html(text) -> str:
    _style = "line-height:0;font-size:20px;margin:1%;font-weight:600;padding-bottom:10px;"
    return f"""<div style="{_style}">{text}</div>"""


def __h2_to_html(text) -> str:
    _style = "line-height:0;font-size:14px;margin:1%;font-weight:600;padding-bottom:10px;"
    return f"""<div style="{_style}">{text}</div>"""


def __status_code_to_html(status_code) -> str:
    if str(status_code).startswith('4') or str(status_code).startswith('5'):
        _color = "#880202"
    else:
        _color = "#008640"
    _html = f"""<div style="color:{_color};font-size:20px;margin:1%;font-weight:600;">{status_code}</div>"""
    return _html


def __dict_to_html(_dict) -> str:
    if _dict is None:
        _rows_content = ""
    else:
        try:
            _dict = dict(_dict)
            _rows_content = json.dumps(_dict, indent=2)
            _rows_content = _rows_content.replace("\n", "<br />")
            _rows_content = _rows_content.replace("  ", "&emsp;")
        except Exception:
            _rows_content = str(_dict)

    _style = "width:92%;padding:15px;margin-left:4%;margin-bottom:8px;border-radius:10px;background:#41444e;color:#fff;font-size:12px;"  # noqa
    _html = f"""<div style="{_style}">{_rows_content}</div>"""
    return _html


def __data_to_html(resp) -> str:
    def remove_style_from_html(error_html):
        soup = BeautifulSoup(error_html, "html.parser")
        for style in soup(["style"]):
            style.extract()
        return str(soup)

    resp_text = resp.text
    if "content-type" in resp.headers.keys():
        if "application/json" in resp.headers['content-type']:
            _html = __dict_to_html(resp.text)
            return _html
        else:
            resp_text = remove_style_from_html(resp_text)
            _style = "border:solid;border-color:#41444e;border-radius:10px;width:92%;padding:15px;margin-left:4%;"
            _html = f"""<div style="{_style}">{resp_text}</div>"""
            return _html
