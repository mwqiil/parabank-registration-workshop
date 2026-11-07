import json
import os
from uuid import uuid4

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from diagnostics import record_browser_events


DEFAULT_URL = "https://parabank.parasoft.com/parabank"
CALL_FAILED = pytest.StashKey[bool]()


def pytest_addoption(parser):
    options = parser.getgroup("parabank")
    options.addoption("--browser", choices=("both", "chrome", "firefox"), default="both")
    options.addoption("--base-url", default=os.environ.get("PARABANK_URL", DEFAULT_URL))
    options.addoption("--headed", action="store_true", help="Открыть браузер с интерфейсом")


def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        selected = metafunc.config.getoption("--browser")
        browsers = ("chrome", "firefox") if selected == "both" else (selected,)
        metafunc.parametrize("driver", browsers, indirect=True)


@pytest.fixture(scope="session")
@allure.title("Адрес приложения ParaBank")
def base_url(pytestconfig):
    return pytestconfig.getoption("--base-url").rstrip("/")


@pytest.fixture
@allure.title("Синтетические регистрационные данные")
def registration_data():
    password = "Sample2026!"
    return {
        "customer.firstName": "Alex",
        "customer.lastName": "Sample",
        "customer.address.street": "100 Test Lane",
        "customer.address.city": "Oakland",
        "customer.address.state": "CA",
        "customer.address.zipCode": "94607",
        "customer.phoneNumber": "2025550140",
        "customer.ssn": "900-00-0000",
        "customer.username": f"wb_{uuid4().hex[:14]}",
        "customer.password": password,
        "repeatedPassword": password,
    }


@pytest.fixture
@allure.title("Запуск и закрытие браузера")
def driver(request):
    headed = request.config.getoption("--headed")
    if request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", "en-US")
        if not headed:
            options.add_argument("-headless")
        browser_type = webdriver.Firefox
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=en-US")
        if not headed:
            options.add_argument("--headless=new")
        browser_type = webdriver.Chrome

    options.enable_bidi = True
    browser = browser_type(options=options)
    try:
        browser.implicitly_wait(0)
        browser.set_page_load_timeout(25)
        browser.set_window_size(1280, 900)
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    if report.when == "call":
        item.stash[CALL_FAILED] = report.failed
    return report


@pytest.fixture(autouse=True)
@allure.title("Диагностика при падении теста")
def failure_artifacts(driver, request):
    console, network = record_browser_events(driver)
    yield
    if not request.node.stash.get(CALL_FAILED, False):
        return

    try:
        allure.attach(driver.get_screenshot_as_png(), "screenshot", allure.attachment_type.PNG)
    except WebDriverException as error:
        allure.attach(str(error), "screenshot-error", allure.attachment_type.TEXT)
    allure.attach(json.dumps(list(console), ensure_ascii=False, indent=2),
                  "browser-console", allure.attachment_type.JSON)
    allure.attach(json.dumps(list(network), ensure_ascii=False, indent=2),
                  "network-requests", allure.attachment_type.JSON)
