import time
from time import sleep

from playwright.sync_api import Playwright, expect

from data.constants import LOGIN_PAGE_TITLE, DOCUMENTS_INSIGHTS_TITLE
from pageObjects.documentsInsightsPage import DocumentsInsightsPage
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.api.api_base import get_user_token
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list


def test_log_out(playwright: Playwright):
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
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
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


def test_navigate_to_documents_insights_page(playwright: Playwright):
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
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
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    # Verification
    expect(on_documents_insights_page.page_title).to_have_text(DOCUMENTS_INSIGHTS_TITLE)
    expect(on_documents_insights_page.hubs_button).to_be_visible()
    expect(on_documents_insights_page.reports_button).to_be_visible()
    expect(on_documents_insights_page.processed_tab).to_be_visible()
    expect(on_documents_insights_page.pending_tab).to_be_visible()
    expect(on_documents_insights_page.queued_tab).to_be_visible()
    expect(on_documents_insights_page.rejected_tab).to_be_visible()

