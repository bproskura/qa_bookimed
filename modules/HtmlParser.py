from lxml import html


def return_text_from_html(content, xpath):
    tree = html.fromstring(content)
    try:
        elem_list = tree.xpath(xpath)
        text = elem_list[0].text
        return text
    except Exception:  # noqa
        return f"content does not have this xpath:{xpath}"


def return_href_from_html(content, xpath):
    tree = html.fromstring(content)
    try:
        elem_list = tree.xpath(xpath)
        href = elem_list[0].get("href")
        return href
    except Exception:  # noqa
        return f"content does not have this xpath:{xpath}"


def return_hrefs_from_html(content, xpath: str) -> list:
    tree = html.fromstring(content)
    try:
        elem_list = tree.xpath(xpath)
        return [i.get("href") for i in elem_list if i.get("href") is not None]
    except Exception:  # noqa
        return [f"content does not have this xpath:{xpath}"]
