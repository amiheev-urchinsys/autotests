import pytest
from playwright.sync_api import expect
from pageObjects.loginPage import LoginPage
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.role_support
def test_authenticate_user_with_email_and_password_role_support(page):
    """
    Verify that a user with a 'support user' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Log out user
    """
    # Get user credentials from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    support_user = get_value_by_key_from_list(user_credentials_list, "support")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(support_user["email"], support_user["password"])
    # Verification
    expected_text = f"Welcome back, {support_user['name']}!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Post-conditions
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()
    expect(on_login_page.page_title).to_contain_text("Welcome to Plextera")


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.company_owner
def test_authenticate_user_with_email_and_password_role_owner(page):
    """
    Verify that a user with a 'company owner' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Log out user
    """
    # Get user credentials from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    company_owner = get_value_by_key_from_list(user_credentials_list, "company_owner")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(company_owner["email"], company_owner["password"])
    # Verification
    expected_text = f"Welcome back, {company_owner['name']}!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Post-conditions
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()
    expect(on_login_page.page_title).to_contain_text("Welcome to Plextera")


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.company_administrator
def test_authenticate_user_with_email_and_password_role_administrator(page):
    """
    Verify that a user with a 'company administrator' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Log out user
    """
    # Get user credentials from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    company_administrator = get_value_by_key_from_list(user_credentials_list, "company_administrator")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(company_administrator["email"],
                                                             company_administrator["password"])
    # Verification
    expected_text = f"Welcome back, {company_administrator['name']}!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Post-conditions
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()
    expect(on_login_page.page_title).to_contain_text("Welcome to Plextera")


@pytest.mark.login
@pytest.mark.positive
@pytest.mark.company_user
def test_authenticate_user_with_email_and_password_role_company_user(page):
    """
    Verify that a user with a 'company user' role can successfully log in using valid email and password.

    Steps:
    - Load user credentials from the JSON file.
    - Navigate to the login page.
    - Enter valid credentials and submit the login form.

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Log out user
    """
    # Get user credentials from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    company_user = get_value_by_key_from_list(user_credentials_list, "company_administrator")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_home_page = on_login_page.login_with_user_credentials(company_user["email"], company_user["password"])
    # Verification
    expected_text = f"Welcome back, {company_user['name']}!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Post-conditions
    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()
    expect(on_login_page.page_title).to_contain_text("Welcome to Plextera")


@pytest.mark.login
@pytest.mark.forgot_password
def test_navigate_to_forgot_password_page(page):
    """
    Verify that the 'Forgot password' page can be accessed from the login page.

    Steps:
    - Navigate to the login page.
    - Click on the 'Forgot password' link.

    Expected:
    - The page title should contain the text 'Forgot password'.
    """
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    # Verification
    expect(on_forgot_password_page.page_title).to_contain_text("Forgot password")


@pytest.mark.login
@pytest.mark.negative
def test_error_message_is_displayed_with_invalid_email(page):
    """
    Verify that an appropriate error message is displayed when logging in with invalid credentials invalid email.

    Steps:
    - Navigate to the login page.
    - Attempt login using an invalid email

    Expected:
    - The application should display 'Invalid credentials' for each failed login attempt.
    """
    # Get user credentials list from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    invalid_credential = get_value_by_key_from_list(user_credentials_list, "invalid_email")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_login_page.login_with_user_credentials(invalid_credential["email"], invalid_credential["password"])
    # Verification
    expect(on_login_page.error_message).to_contain_text("Invalid credentials")


@pytest.mark.login
@pytest.mark.negative
def test_error_message_is_displayed_with_invalid_password(page):
    """
    Verify that an appropriate error message is displayed when logging in with invalid credentials invalid password.

    Steps:
    - Navigate to the login page.
    - Attempt login using an invalid password

    Expected:
    - The application should display 'Invalid credentials' for each failed login attempt.
    """
    # Get user credentials list from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    invalid_credential = get_value_by_key_from_list(user_credentials_list, "invalid_password")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_login_page.login_with_user_credentials(invalid_credential["email"], invalid_credential["password"])
    # Verification
    expect(on_login_page.error_message).to_contain_text("Invalid credentials")


@pytest.mark.login
@pytest.mark.negative
def test_error_message_is_displayed_with_invalid_credentials(page):
    """
    Verify that an appropriate error message is displayed when logging in with invalid credentials.

    Steps:
    - Navigate to the login page.
    - Attempt login using an invalid email and password

    Expected:
    - The application should display 'Invalid credentials' for each failed login attempt.
    """
    # Get user credentials list from the json file
    user_credentials_list = get_list_from_file("user_credentials.json", "users")
    invalid_credential = get_value_by_key_from_list(user_credentials_list, "invalid_credentials")
    # Steps
    page.goto("https://studio.dev.plextera.com/login")
    on_login_page = LoginPage(page)
    on_login_page.login_with_user_credentials(invalid_credential["email"], invalid_credential["password"])
    # Verification
    expect(on_login_page.error_message).to_contain_text("Invalid credentials")