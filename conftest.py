from typing import Generator

import pytest

from playwright.sync_api import BrowserContext, Page, Playwright

import cfg

from modules.Allure import (
    add_allure_environment_properties,
    add_description_html,
    log_location,
    log_screenshot,
)

pytest_plugins = ()


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(items):
    """
    Pytest mark implementation for:
     - add/change allure info for report description in html format
    """
    for item in items:
        add_description_html(item)
    yield


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default=cfg.BROWSER)
    parser.addoption("--headless", action="store", default=cfg.HEADLESS)
    parser.addoption("--browser_width", action="store", default=cfg.SCREEN_WIDTH)
    parser.addoption("--browser_height", action="store", default=cfg.SCREEN_HEIGHT)
    parser.addoption("--locale", action="store", default=cfg.DEFAULT_LOCALE)
    parser.addoption("--timezone", action="store", default=cfg.DEFAULT_TIMEZONE)
    parser.addoption("--full_screenshot", action="store", default="False")
    parser.addoption("--mobile_device", action="store", default=cfg.MOBILE_DEVICE)


@pytest.fixture
def context(playwright: Playwright, pytestconfig) -> Generator[BrowserContext, None, None]:
    context = playwright.chromium.launch_persistent_context(
        "",
        headless=eval(pytestconfig.getoption("--headless")),
        locale=pytestconfig.getoption("--locale"),
        timezone_id=pytestconfig.getoption("--timezone"),
        viewport={"width": int(pytestconfig.getoption("--browser_width")),
                  "height": int(pytestconfig.getoption("--browser_height"))},
        timeout=cfg.WAIT_MAX_PAGE_LOAD_TIMEOUT,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--wm-window-animations-disabled",
            "--disable-notifications",
            "--mute-audio",
            "--accept-lang=UK",
            "--browser-test",
        ],
    )
    yield context
    context.close()


@pytest.fixture
def mobile(playwright: Playwright, pytestconfig) -> Generator[BrowserContext, None, None]:
    device = playwright.devices[pytestconfig.getoption("--mobile_device")]
    browser = playwright.chromium.launch(headless=eval(pytestconfig.getoption("--headless")))
    context = browser.new_context(**device)

    yield context
    context.close()


@pytest.fixture(scope="class")
def fake():
    from modules.Faker import Fake
    return Fake()


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    # config.addinivalue_line("markers", "on_env(name): mark test to run only on named environment")
    # config.addinivalue_line("markers", "skip_env(name): mark test to skip only on named environment")
    # config.addinivalue_line("markers", "on_browser(name): mark test to run only on named browser")
    """ add env properties to allure report """
    alluredir = config.getoption("--alluredir")
    browser_name = config.getoption("--browser_name")
    env_properties = {
        "DESCRIPTION": "Bookimed QA Tests",
        "BASE_URL": cfg.BASE_URL,
        "BROWSER": browser_name,
    }
    add_allure_environment_properties(alluredir, env_properties)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """ This fixture make actions when test failed """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.outcome == "failed":
        fixtures_register: set = {"context", "page"}
        try:
            intersection_fixture = list(fixtures_register & set(item.fixturenames))[0]
            page: Page = item.funcargs[intersection_fixture]
            page = page.pages[-1] if getattr(page, "pages", False) else page

            log_location(page.url)
            log_screenshot(page.screenshot(type="png",
                                           full_page=eval(item.config.getoption("--full_screenshot"))))

        except Exception as error:
            print(str(error), rep.head_line)
