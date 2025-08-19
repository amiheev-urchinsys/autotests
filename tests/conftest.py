import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def shared_data():
    return {}


@pytest.fixture
def context_and_playwright():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        yield context, playwright
        context.close()
        browser.close()