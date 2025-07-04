import time
from time import sleep

from playwright.sync_api import Playwright, expect

from pageObjects.documentsInsightsPage import DocumentsInsightsPage
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.api.api_base import get_user_token


def test_log_out(playwright: Playwright):
    # Get user token to set the cookies
    response = get_user_token(playwright)
    user_token = response.json()["accessToken"]
    # Set the browser
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    page = context.new_page()
    # Test
    page.goto("https://studio.dev.plextera.com")
    on_home_page = HomePage(page)
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text("Welcome to Plextera")


def test_navigate_to_documents_insights_page(playwright: Playwright):
    # Get user token to set the cookies
    response = get_user_token(playwright)
    user_token = response.json()["accessToken"]
    # Set the browser
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    page = context.new_page()
    # Test
    page.goto("https://studio.dev.plextera.com")
    on_home_page = HomePage(page)
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.document_insights_point.click()
    on_documents_insights_page = DocumentsInsightsPage(page)
    on_hubs_page = on_documents_insights_page.navigate_to_hubs_page()
    on_hubs_page.create_a_hub_button.click()
    on_hubs_page.outline_based_type_card.click()
    time.sleep(5)
