import pytest
from playwright.sync_api import expect

from data.constants import HOME_PAGE_USER_TITLE, FORGOT_PASSWORD_PAGE_TITLE, \
    ERROR_TEXT_INVALID_CREDENTIALS, LOGIN_PAGE_URL, DOMAIN_STAGE_URL, HOME_PAGE_MAIN_TITLE, HOME_PAGE_DESCRIPTION
from pageObjects.loginPage import LoginPage
from utilities.data_processing import get_key_value_from_file


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.role_support
def test_authenticate_user_with_email_and_password_role_support(context_and_playwright):
    """
    Verify that a user with a 'support user' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed
    - The user greeting message contains the text 'Welcome back, username'.
    """
    # Get user credentials from the json file
    support_user = get_key_value_from_file("user_credentials.json", "support")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(support_user["email"], support_user["password"])
    # Verification
    expect(on_home_page.user_greeting_text).to_have_text(f"{HOME_PAGE_USER_TITLE}{support_user['name']}!")
    expect(on_home_page.main_greeting_text).to_have_text(HOME_PAGE_MAIN_TITLE)
    expect(on_home_page.description_text).to_have_text(HOME_PAGE_DESCRIPTION)

@pytest.mark.login
@pytest.mark.positive
@pytest.mark.company_owner
def test_authenticate_user_with_email_and_password_role_owner(context_and_playwright):
    """
    Verify that a user with a 'company owner' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.
    """
    # Get user credentials from the json file
    company_owner = get_key_value_from_file("user_credentials.json", "company_owner")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(company_owner["email"], company_owner["password"])
    # Verification
    expect(on_home_page.user_greeting_text).to_have_text(f"{HOME_PAGE_USER_TITLE}{company_owner['name']}!")
    expect(on_home_page.main_greeting_text).to_have_text(HOME_PAGE_MAIN_TITLE)
    expect(on_home_page.description_text).to_have_text(HOME_PAGE_DESCRIPTION)


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.company_administrator
def test_authenticate_user_with_email_and_password_role_administrator(context_and_playwright):
    """
    Verify that a user with a 'company administrator' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.
    """
    # Get user credentials from the json file
    company_administrator = get_key_value_from_file("user_credentials.json", "company_administrator")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(company_administrator["email"],
                                                             company_administrator["password"])
    # Verification
    expect(on_home_page.user_greeting_text).to_have_text(f"{HOME_PAGE_USER_TITLE}{company_administrator['name']}!")
    expect(on_home_page.main_greeting_text).to_have_text(HOME_PAGE_MAIN_TITLE)
    expect(on_home_page.description_text).to_have_text(HOME_PAGE_DESCRIPTION)

@pytest.mark.login
@pytest.mark.positive
@pytest.mark.company_user
def test_authenticate_user_with_email_and_password_role_company_user(context_and_playwright):
    """
    Verify that a user with a 'company user' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.
    """
    # Get user credentials from the json file
    company_user = get_key_value_from_file("user_credentials.json", "company_user")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(company_user["email"], company_user["password"])
    # Verification
    expect(on_home_page.user_greeting_text).to_have_text(f"{HOME_PAGE_USER_TITLE}{company_user['name']}!")
    expect(on_home_page.main_greeting_text).to_have_text(HOME_PAGE_MAIN_TITLE)
    expect(on_home_page.description_text).to_have_text(HOME_PAGE_DESCRIPTION)


@pytest.mark.login
@pytest.mark.forgot_password
def test_navigate_to_forgot_password_page(context_and_playwright):
    """
    Verify that the 'Forgot password' page can be accessed from the login page.

    Steps:
    - Navigate to the login page.
    - Click on the 'Forgot password' link.

    Expected:
    - The page title should contain the text 'Forgot password'.
    """
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    # Verification
    expect(on_forgot_password_page.page_title).to_have_text(FORGOT_PASSWORD_PAGE_TITLE)


@pytest.mark.login
@pytest.mark.negative
def test_error_message_is_displayed_with_invalid_email(context_and_playwright):
    """
    Verify that an appropriate error message is displayed when logging in with invalid credentials invalid email.

    Steps:
    - Navigate to the login page.
    - Attempt login using an invalid email

    Expected:
    - The application should display 'Invalid credentials' for each failed login attempt.
    """
    # Get user credentials list from the json file
    invalid_credential = get_key_value_from_file("user_credentials.json", "invalid_email")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_login_page.login_with_user_credentials(invalid_credential["email"], invalid_credential["password"])
    # Verification
    expect(on_login_page.error_message).to_have_text(ERROR_TEXT_INVALID_CREDENTIALS)


@pytest.mark.login
@pytest.mark.negative
def test_error_message_is_displayed_with_invalid_password(context_and_playwright):
    """
    Verify that an appropriate error message is displayed when logging in with invalid credentials invalid password.

    Steps:
    - Navigate to the login page.
    - Attempt login using an invalid password

    Expected:
    - The application should display 'Invalid credentials' for each failed login attempt.
    """
    # Get user credentials list from the json file
    invalid_credential = get_key_value_from_file("user_credentials.json", "invalid_password")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_login_page.login_with_user_credentials(invalid_credential["email"], invalid_credential["password"])
    # Verification
    expect(on_login_page.error_message).to_have_text(ERROR_TEXT_INVALID_CREDENTIALS)


@pytest.mark.login
@pytest.mark.negative
def test_error_message_is_displayed_with_invalid_credentials(context_and_playwright):
    """
    Verify that an appropriate error message is displayed when logging in with invalid credentials.

    Steps:
    - Navigate to the login page.
    - Attempt login using an invalid email and password

    Expected:
    - The application should display 'Invalid credentials' for each failed login attempt.
    """
    # Get user credentials list from the json file
    invalid_credential = get_key_value_from_file("user_credentials.json", "invalid_credentials")
    # Browser setup
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps
    page.goto(DOMAIN_STAGE_URL + LOGIN_PAGE_URL)
    on_login_page = LoginPage(page)
    on_login_page.login_with_user_credentials(invalid_credential["email"], invalid_credential["password"])
    # Verification
    expect(on_login_page.error_message).to_have_text(ERROR_TEXT_INVALID_CREDENTIALS)