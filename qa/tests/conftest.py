import pytest
from playwright.sync_api import sync_playwright
from qa.utilities.logging_utils import logger_utility

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )

@pytest.fixture(scope="function")
def page_instance(request):
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("--headless")

    with sync_playwright() as p:
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)

        context = browser.new_context()

        page = context.new_page()

        page.goto('https://cmelski.github.io/online-portfolio/')
        logger_utility().info('Launching UI...')

        try:
            yield page
        finally:
            context.close()
            browser.close()