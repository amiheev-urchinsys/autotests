from playwright.sync_api import Playwright, expect

from data.constants import LOGIN_PAGE_TITLE, DOCUMENTS_INSIGHTS_TITLE, WORKFLOWS_EMPTY_STATE_TITLE, \
    WORKFLOWS_EMPTY_STATE_DESCRIPTION, DOMAIN_STAGE_URL
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.api.api_base import get_user_token
from utilities.data_processing import get_key_value_from_file


def test_log_out(context_and_playwright):
    """
    This test verifies that a user can successfully log out from the system

    Steps:
    - Get support user token to authenticate
    - Navigate to Home page
    - Oper user menu and select Log out

    Expected:
    - The Login page is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get data from the json file
    authentication_payload = get_key_value_from_file("payloads.json", "authentication_payload")
    support_data = get_key_value_from_file("user_credentials.json", "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
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
    # Test
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


def test_navigate_to_documents_insights_page(context_and_playwright):
    """
    This test verifies that a user can successfully navigate to the Documents Insights page using sidebar on the Home page

    Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the Documents Insights page

    Expected:
    - The Documents Insights page is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get data from the json file
    authentication_payload = get_key_value_from_file("payloads.json", "authentication_payload")
    support_data = get_key_value_from_file("user_credentials.json", "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
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
    # Test
    page.goto(DOMAIN_STAGE_URL)
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


def test_navigate_to_workflows_page(context_and_playwright):
    """
    This test verifies that a user can successfully navigate to the Workflows page

    Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the Workflows page

    Expected:
    - The Workflows page is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get data
    authentication_payload = get_key_value_from_file("payloads.json", "authentication_payload")
    support_data = get_key_value_from_file("user_credentials.json", "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
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
    # Test
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_workflows_page = on_home_page.sidebar.navigate_to_workflows_page()
    # Verification
    expect(on_workflows_page.page_title).to_have_text(WORKFLOWS_EMPTY_STATE_TITLE)
    expect(on_workflows_page.page_description).to_have_text(WORKFLOWS_EMPTY_STATE_DESCRIPTION)
    expect(on_workflows_page.add_new_workflow_button).to_be_visible()


def test_navigate_to_web_automations_page(context_and_playwright):
    """
    This test verifies that a user can successfully navigate to the Web Automations page

    Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the Web Automations page

    Expected:
    - The Web Automations page is displayed
    """
    # Browser setupr
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get data
    authentication_payload = get_key_value_from_file("payloads.json", "authentication_payload")
    support_data = get_key_value_from_file("user_credentials.json", "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
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
    # Test
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_web_automations_page = on_home_page.sidebar.navigate_to_web_automations_page()
    # Verification
    expect(on_web_automations_page.page_title).to_have_text(WORKFLOWS_EMPTY_STATE_TITLE)
    expect(on_web_automations_page.page_description).to_have_text(WORKFLOWS_EMPTY_STATE_DESCRIPTION)
    expect(on_web_automations_page.add_new_workflow_button).to_be_visible()

