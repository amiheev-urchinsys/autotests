from playwright.sync_api import Playwright, expect

from data.constants import DOMAIN_STAGE_URL, SUCCESS_POPUP_TITLE, HOME_PAGE_USER_TITLE
from pageObjects.homePage import HomePage
from pageObjects.registerCompanyOwnerPage import RegisterCompanyOwnerPage
from pageObjects.registerCompanyUserPage import RegisterCompanyUserPage
from utilities.api.api_base import authenticate_with_user
from utilities.api.api_temp_email import wait_for_email_and_read, delete_emails_in_inbox
from utilities.data_processing import get_key_value_from_file, get_register_link_from_the_email_body
import time

from utilities.utils import authenticate_with_user_profile


def test_invite_and_register_new_owner(context_and_playwright):
    """
    Verify that a support user can send invite to register a company owner.
    Verify that a user receives an email and register link is working.
    Verify that a user can successfully fill in and send the register form.
    Verify that a company owner can authenticate after a successful registration.

    Steps:
    - Delete previously created company with this name
    - Get support user token to authenticate
    - Navigate to Home page
    - Open the Companies tab on the Admin Console page
    - Open the Invite new owner user form
    - Fill in all required fields and send the form
    - Open the email and get the link
    - Open the register link
    - Fill in all the required fields and send the form
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Delete all received emails
    """
    # Delete company with name autotest_create_company

    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get user credentials from the json file
    registration_owner_data = get_key_value_from_file(
        "user_credentials.json",
        "registration_owner_data"
    )
    temp_email_data = get_key_value_from_file(
        "user_credentials.json",
        "temp_email"
    )
    # Steps to send invitation to new company owner
    authenticate_with_user_profile(
        playwright,
        context,
        "support"
    )
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_admin_console_page = on_home_page.sidebar.navigate_to_admin_console_page()
    on_admin_console_page.sidebar_companies_tab.click()
    on_admin_console_page.send_invite_new_company_owner_form(registration_owner_data["email"])
    # Verification Success popup is present
    expect(on_admin_console_page.companies_tab.success_popup.title).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to get register link from email
    body = wait_for_email_and_read(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    link = get_register_link_from_the_email_body(body)
    # Steps to register a new owner
    page.goto(link)
    on_register_company_owner_page = RegisterCompanyOwnerPage(page)
    on_register_company_owner_page.send_the_register_new_company_owner_form(
        registration_owner_data["first_name"],
        registration_owner_data["last_name"],
        registration_owner_data["password"],
        registration_owner_data["company_name"]
    )
    # Verification Success popup is present
    expect(on_register_company_owner_page.success_page.title).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to log in with company owner user
    on_login_page = on_register_company_owner_page.success_page.navigate_to_login_page()
    on_login_page.login_with_user_credentials(
        registration_owner_data["email"],
        registration_owner_data["password"]
    )
    # Verification that user is authenticated
    expect(on_home_page.user_greeting_text).to_have_text(HOME_PAGE_USER_TITLE + registration_owner_data["first_name"])
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    assert response.ok


def test_invite_and_register_new_company_administrator(context_and_playwright):
    """
    Verify that a support user can send invite to register a company user.
    Verify that a user receives an email and register link is working.
    Verify that a user can successfully fill in and send the register form.
    Verify that a company user can authenticate after a successful registration.

    Steps:
    - Get support user token to authenticate
    - Navigate to Home page
    - Open the Companies tab on the Admin Console page
    - Open company page
    - Click the Invite
    - Fill in all required fields and send the form
    - Open the email and get the link
    - Open the register link
    - Fill in all the required fields and send the form
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Delete all received emails
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get user credentials from the json file
    registration_company_administrator_data = get_key_value_from_file(
        "user_credentials.json",
        "registration_company_administrator_data"
    )
    temp_email_data = get_key_value_from_file(
        "user_credentials.json",
        "temp_email"
    )
    # Steps to send invitation to new company owner
    authenticate_with_user_profile(
        playwright,
        context,
        "support"
    )
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_admin_console_page = on_home_page.sidebar.navigate_to_admin_console_page()
    on_admin_console_page.open_companies_tab.click()
    on_company_page = on_admin_console_page.companies_tab.navigate_to_company_page("automation_testing")
    on_company_page.invite_company_user_button.click()
    on_company_page.send_invite_company_administrator_form(registration_company_administrator_data["email"])
    # Verification Success popup is present
    expect(on_company_page.popups).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to get register link from email
    body = wait_for_email_and_read(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    link = get_register_link_from_the_email_body(body)
    # Steps to register a new owner
    page.goto(link)
    on_register_company_user_page = RegisterCompanyUserPage(page)
    on_register_company_user_page.send_the_register_new_company_user_form(
        registration_company_administrator_data["first_name"],
        registration_company_administrator_data["last_name"],
        registration_company_administrator_data["password"],
    )
    # Verification Success popup is present
    expect(on_register_company_user_page.success_page.title).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to log in with company owner user
    on_login_page = on_register_company_user_page.success_page.navigate_to_login_page()
    on_login_page.login_with_user_credentials(
        registration_company_administrator_data["email"],
         registration_company_administrator_data["password"]
    )
    # Verification that user is authenticated
    expect(on_home_page.user_greeting_text).to_have_text(HOME_PAGE_USER_TITLE + registration_company_administrator_data["first_name"])
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    assert response.ok


def test_invite_and_register_new_company_user(context_and_playwright):
    """
    Verify that a support user can send invite to register a company user.
    Verify that a user receives an email and register link is working.
    Verify that a user can successfully fill in and send the register form.
    Verify that a company user can authenticate after a successful registration.

    Steps:
    - Get support user token to authenticate
    - Navigate to Home page
    - Open the Companies tab on the Admin Console page
    - Open company page
    - Click the Invite
    - Fill in all required fields and send the form
    - Open the email and get the link
    - Open the register link
    - Fill in all the required fields and send the form
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Delete all received emails
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get user credentials from the json file
    registration_company_user_data = get_key_value_from_file(
        "user_credentials.json",
        "registration_company_user_data"
    )
    temp_email_data = get_key_value_from_file(
        "user_credentials.json",
        "temp_email"
    )
    # Steps to send invitation to new company owner
    authenticate_with_user_profile(
        playwright,
        context,
        "support"
    )
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_admin_console_page = on_home_page.sidebar.navigate_to_admin_console_page()
    on_admin_console_page.open_companies_tab.click()
    on_company_page = on_admin_console_page.companies_tab.navigate_to_company_page("automation_testing")
    on_company_page.invite_company_user_button.click()
    on_company_page.send_invite_company_user_form(registration_company_user_data["email"])
    # Verification Success popup is present
    expect(on_company_page.popups).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to get register link from email
    body = wait_for_email_and_read(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    link = get_register_link_from_the_email_body(body)
    # Steps to register a new owner
    page.goto(link)
    on_register_company_user_page = RegisterCompanyUserPage(page)
    on_register_company_user_page.send_the_register_new_company_user_form(
        registration_company_user_data["first_name"],
        registration_company_user_data["last_name"],
        registration_company_user_data["password"],
    )
    # Verification Success popup is present
    expect(on_register_company_user_page.success_page.title).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to log in with company owner user
    on_login_page = on_register_company_user_page.success_page.navigate_to_login_page()
    on_login_page.login_with_user_credentials(
        registration_company_user_data["email"],
        registration_company_user_data["password"]
    )
    # Verification that user is authenticated
    expect(on_home_page.user_greeting_text).to_have_text(HOME_PAGE_USER_TITLE + registration_company_user_data["first_name"])
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    assert response.ok


def test_invite_and_register_new_support_user(context_and_playwright):
    """
    Verify that a support user can send invite to register a company user.
    Verify that a user receives an email and register link is working.
    Verify that a user can successfully fill in and send the register form.
    Verify that a company user can authenticate after a successful registration.

    Steps:
    - Get support user token to authenticate
    - Navigate to Home page
    - Open the Companies tab on the Admin Console page
    - Open company page
    - Click the Invite
    - Fill in all required fields and send the form
    - Open the email and get the link
    - Open the register link
    - Fill in all the required fields and send the form
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Delete all received emails
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get user credentials from the json file
    registration_support_user_data = get_key_value_from_file(
        "user_credentials.json",
        "registration_support_user_data"
    )
    temp_email_data = get_key_value_from_file(
        "user_credentials.json",
        "temp_email"
    )
    # Steps to send invitation to new company owner
    authenticate_with_user_profile(
        playwright,
        context,
        "support"
    )
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_admin_console_page = on_home_page.sidebar.navigate_to_admin_console_page()
    on_admin_console_page.open_companies_tab.click()
    on_company_page = on_admin_console_page.companies_tab.navigate_to_company_page("automation_testing")
    on_company_page.invite_company_user_button.click()
    on_company_page.send_invite_company_user_form(registration_support_user_data["email"])
    # Verification Success popup is present
    expect(on_company_page.popups).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to get register link from email
    body = wait_for_email_and_read(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    link = get_register_link_from_the_email_body(body)
    # Steps to register a new owner
    page.goto(link)
    on_register_company_user_page = RegisterCompanyUserPage(page)
    on_register_company_user_page.send_the_register_new_company_user_form(
        registration_support_user_data["first_name"],
        registration_support_user_data["last_name"],
        registration_support_user_data["password"],
    )
    # Verification Success popup is present
    expect(on_register_company_user_page.success_page.title).to_have_text(SUCCESS_POPUP_TITLE)
    # Steps to log in with company owner user
    on_login_page = on_register_company_user_page.success_page.navigate_to_login_page()
    on_login_page.login_with_user_credentials(
        registration_support_user_data["email"],
        registration_support_user_data["password"]
    )
    # Verification that user is authenticated
    expect(on_home_page.user_greeting_text).to_have_text(HOME_PAGE_USER_TITLE + registration_support_user_data["first_name"])
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(
        playwright,
        temp_email_data["email_id"],
        temp_email_data["x_api_key"]
    )
    assert response.ok

