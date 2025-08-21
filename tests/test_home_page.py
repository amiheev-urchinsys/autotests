from playwright.sync_api import Playwright, expect

from data.constants import LOGIN_PAGE_TITLE, DOCUMENTS_INSIGHTS_TITLE, WORKFLOWS_EMPTY_STATE_TITLE, \
    WORKFLOWS_EMPTY_STATE_DESCRIPTION, DOMAIN_STAGE_URL
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.utils import authenticate_with_user_profile


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
    # Test
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.user_menu_dropdown.click()
    on_home_page.sidebar.user_menu_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


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
    # Test
    authenticate_with_user_profile(playwright, context, "support")
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
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_web_automations_page = on_home_page.sidebar.navigate_to_web_automations_page()
    # Verification
    expect(on_web_automations_page.automations_tab).to_contain_class("active")
    expect(on_web_automations_page.fragments_tab).not_to_contain_class("active")
    expect(on_web_automations_page.credentials_tab).not_to_contain_class("active")
    expect(on_web_automations_page.create_button).to_be_visible()
    expect(on_web_automations_page.import_button).to_be_visible()
    expect(on_web_automations_page.table).to_be_visible()
    expect(on_web_automations_page.no_data_row).to_have_text("No data")


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
    # Test
    authenticate_with_user_profile(playwright, context, "support")
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


def test_navigate_to_sides_page(context_and_playwright):
    """
    This test case verifies that users can successfully navigate to the SIDES page by clicking the corresponding item in the left sidebar.

    Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the SIDES page

    Expected:
    - The SIDES page is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_sides_page = on_home_page.sidebar.navigate_to_sides_page()
    # Verification
    expect(on_sides_page.states_and_exchanges_tab).to_have_attribute("aria-selected", "true")
    expect(on_sides_page.history_tab).to_have_attribute("aria-selected", "false")
    expect(on_sides_page.pull_schedule_button).to_be_visible()
    expect(on_sides_page.table).to_be_visible()
    expect(on_sides_page.test_button).to_be_visible()
    expect(on_sides_page.pull_button).to_be_visible()


def test_navigate_to_the_datastores_page(context_and_playwright):
    """
    This test case verifies that users can successfully navigate to the Datastores page by clicking the corresponding item in the left sidebar.

     Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the Datastores page

    Expected:
    - The Datastores page is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_datastores_page = on_home_page.sidebar.navigate_to_datastores_page()
    # Verification
    expect(on_datastores_page.page_title).to_be_visible()
    expect(on_datastores_page.add_new_button).to_be_visible()
    expect(on_datastores_page.table).to_be_visible()
    expect(on_datastores_page.no_data_available_text).to_be_visible()


def test_navigate_to_the_forms_page(context_and_playwright):
    """
    This test case verifies that users can successfully navigate to the Forms page by clicking the corresponding item in the left sidebar.

     Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the Forms page

    Expected:
    - The Forms page is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_forms_page = on_home_page.sidebar.navigate_to_forms_page()
    # Verification
    expect(on_forms_page.page_title).to_be_visible()
    expect(on_forms_page.create_form_button).to_be_visible()
    expect(on_forms_page.table).to_be_visible()
    expect(on_forms_page.no_data_available_text).to_be_visible()


def test_navigate_to_the_alerts_page(context_and_playwright):
    """
    This test case verifies that users can successfully navigate to the Alerts page by clicking the corresponding item in the left sidebar.

     Steps:
    - Get support user token to authenticate
    - Navigate to the Home page
    - Navigate to the Alerts page

    Expected:
    - The Alerts page is displayed
    """
    # Browser setupr
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_alerts_page = on_home_page.sidebar.navigate_to_alerts_page()
    # Verification
    expect(on_alerts_page.page_title).to_be_visible()
    expect(on_alerts_page.filter_button).to_be_visible()
    expect(on_alerts_page.reset_filters_button).to_be_visible()
    expect(on_alerts_page.table).to_be_visible()
    expect(on_alerts_page.no_data_available_text).to_be_visible()


def test_open_user_menu_of_support_user(context_and_playwright):
    """
    This test case verifies that users can successfully open the personal cabinet menu by clicking the corresponding item in the left sidebar.

    Steps:
    - Get support user token to authenticate
    - Click the user menu

    Expected:
    - The user menu is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "support")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_home_page.sidebar.open_user_menu()
    # Verification
    expect(on_home_page.sidebar.user_menu_dropdown).to_be_visible()
    expect(on_home_page.sidebar.user_menu_settings_point).to_be_visible()
    expect(on_home_page.sidebar.user_menu_admin_console_point).to_be_visible()
    expect(on_home_page.sidebar.user_menu_log_out_point).to_be_visible()


def test_open_user_menu_of_company_owner(context_and_playwright):
    """
    This test case verifies that users can successfully open the personal cabinet menu by clicking the corresponding item in the left sidebar.

    Steps:
    - Get support user token to authenticate
    - Click the user menu

    Expected:
    - The user menu is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "company_owner")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_home_page.sidebar.open_user_menu()
    # Verification
    expect(on_home_page.sidebar.user_menu_dropdown).to_be_visible()
    expect(on_home_page.sidebar.user_menu_settings_point).to_be_visible()
    expect(on_home_page.sidebar.user_menu_admin_console_point).not_to_be_visible()
    expect(on_home_page.sidebar.user_menu_log_out_point).to_be_visible()


def test_open_user_menu_of_company_administrator(context_and_playwright):
    """
    This test case verifies that users can successfully open the personal cabinet menu by clicking the corresponding item in the left sidebar.

    Steps:
    - Get support user token to authenticate
    - Click the user menu

    Expected:
    - The user menu is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "company_administrator")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_home_page.sidebar.open_user_menu()
    # Verification
    expect(on_home_page.sidebar.user_menu_dropdown).to_be_visible()
    expect(on_home_page.sidebar.user_menu_settings_point).to_be_visible()
    expect(on_home_page.sidebar.user_menu_admin_console_point).not_to_be_visible()
    expect(on_home_page.sidebar.user_menu_log_out_point).to_be_visible()


def test_open_user_menu_of_company_user(context_and_playwright):
    """
    This test case verifies that users can successfully open the personal cabinet menu by clicking the corresponding item in the left sidebar.

    Steps:
    - Get support user token to authenticate
    - Click the user menu

    Expected:
    - The user menu is displayed
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Test
    authenticate_with_user_profile(playwright, context, "company_user")
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_home_page.sidebar.open_user_menu()
    # Verification
    expect(on_home_page.sidebar.user_menu_dropdown).to_be_visible()
    expect(on_home_page.sidebar.user_menu_settings_point).to_be_visible()
    expect(on_home_page.sidebar.user_menu_admin_console_point).not_to_be_visible()
    expect(on_home_page.sidebar.user_menu_log_out_point).to_be_visible()