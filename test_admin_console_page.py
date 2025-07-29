from playwright.sync_api import Playwright, expect

from data.constants import DOMAIN_STAGE_URL
from pageObjects.homePage import HomePage
from pageObjects.registerCompanyOwnerPage import RegisterCompanyOwnerPage
from utilities.api.api_base import get_user_token
from utilities.api.api_temp_email import wait_for_email_and_read, delete_emails_in_inbox
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list, \
    get_register_link_from_the_email_body


def test_invite_new_owner(playwright: Playwright):
    """
    Verify that a support user can send invite to register a company owner.
    Verify that a user receives an email and register link is working.
    Verify that a user can successfully fill in and send the register form.
    Verify that a company owner can authenticate after a successful registration.

    Steps:
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
    - Log out user
    - Delete all received emails
    """
    # Get authentication payload
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    # Get user credentials from the json file
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    temp_email_data = get_value_by_key_from_list(users_list, "temp_email")
    # Fill in payload with valid values
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
    # Steps to send invitation to new company owner
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_admin_console_page = on_home_page.sidebar.navigate_to_admin_console_page()
    on_admin_console_page.sidebar_companies_tab.click()
    on_admin_console_page.send_invite_new_company_owner_form(temp_email_data["email"])
    # Verification Success popup is present
    expected_text = "Success!"
    expect(on_admin_console_page.companies_tab.success_popup.title).to_have_text(expected_text)
    # Steps to get register link from email
    body = wait_for_email_and_read(playwright, temp_email_data["email_id"], temp_email_data["x_api_key"])
    link = get_register_link_from_the_email_body(body)
    # Steps to register a new owner
    page.goto(link)
    on_register_company_owner_page = RegisterCompanyOwnerPage(page)
    on_register_company_owner_page.send_the_register_new_company_owner_form("autotestFirstName",
                                                                 "autotestLastName",
                                                                 "EM#@YgnHy8",
                                                                 "autotest_create_company")
    # Verification Success popup is present
    expected_text = "Success!"
    expect(on_register_company_owner_page.success_page.title).to_have_text(expected_text)
    # Steps to log in with company owner user
    on_login_page = on_register_company_owner_page.success_page.navigate_to_login_page()
    on_login_page.login_with_user_credentials(temp_email_data["email"], "EM#@YgnHy8")
    # Verification that user is authenticated
    expected_text = "Welcome back, autotestFirstName!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["email_id"], temp_email_data["x_api_key"])
    assert response.ok
