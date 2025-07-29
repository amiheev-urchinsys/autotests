from playwright.sync_api import Playwright, expect

from data.constants import DOMAIN_STAGE_URL, FORGOT_PASSWORD_PAGE_ERROR_EMPTY_EMAIL, \
    FORGOT_PASSWORD_PAGE_ERROR_INVALID_FORMAT, FORGOT_PASSWORD_PAGE_SUCCESS
from pageObjects.loginPage import LoginPage
from pageObjects.updatePasswordPage import UpdatePasswordPage
from utilities.api.api_temp_email import wait_for_email_and_read, delete_emails_in_inbox
from utilities.data_processing import get_create_new_password_link_from_the_email_body, get_list_from_file, \
    get_value_by_key_from_list


def test_update_password(context_and_playwright):
    """
    Verify that a support user can send invite to register a company owner.
    Verify that a user receives an email and register link is working.
    Verify that a user can successfully fill in and send the register form.
    Verify that a company owner can authenticate after a successful registration.

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Fill in all required fields and send the form
    - Open the email and get the link
    - Open the update password link
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
    users_list = get_list_from_file("user_credentials.json", "users")
    temp_email_data = get_value_by_key_from_list(users_list, "temp_email")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.email_input.fill(temp_email_data["email"])
    # Wait until request is finished and then continue
    with page.expect_response(
            f"**/api/account-service/auth-user/forgot-password?email={temp_email_data["email"]}") as resp_info:
        on_forgot_password_page.send_button.click()
    response = resp_info.value
    assert response.ok
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["email_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    # Steps to change password and send the form
    page.goto(link)
    on_update_password_page = UpdatePasswordPage(page)
    on_update_password_page.new_password_input.fill("EM#@YgnHy9")
    on_update_password_page.confirm_new_password_input.fill("EM#@YgnHy9")
    # Wait until request is finished and then continue
    with page.expect_response("**/api/account-service/auth-user/create-password") as resp_info:
        on_update_password_page.update_button.click()
    response = resp_info.value
    assert response.ok
    on_update_password_page.back_to_login_button.click()
    # Steps to log in with new password
    on_home_page = on_login_page.login_with_user_credentials(temp_email_data["email"],"EM#@YgnHy9")
    expected_text = "Welcome back, testing!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["email_id"], temp_email_data["x_api_key"])
    assert response.ok


def test_error_message_is_displayed_when_the_email_address_field_is_empty(context_and_playwright):
    """
    Verify that error message is displayed when trying to send form with empty email address input on the Forgot Password page

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Send the form

    Expected:
    - Error message is displayed
    """
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_button.click()
    # Verification
    expect(on_forgot_password_page.error_message).to_have_text(FORGOT_PASSWORD_PAGE_ERROR_EMPTY_EMAIL)


def test_error_message_is_displayed_when_invalid_value_is_entered_in_the_email_address_field(context_and_playwright):
    """
    Verify that error message is displayed when trying to send form with invalid value in the email address input on the Forgot Password page

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Enter invalid value in the Email address input
    - Send the form

    Expected:
    - Error message is displayed
    """
    # Get data from file
    invalid_data = get_list_from_file("invalid_data.json", "invali_data")
    invalid_emails_list = get_value_by_key_from_list(invalid_data, "invalid_emails")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    for email in invalid_emails_list:
        on_forgot_password_page.email_input.fill(get_value_by_key_from_list(email, "value"))
        on_forgot_password_page.send_button.click()
        # Verification
        expect(on_forgot_password_page.error_message).to_have_text(FORGOT_PASSWORD_PAGE_ERROR_INVALID_FORMAT)
        page.reload()


def test_navigate_to_the_login_page_from_the_forgot_password_form(context_and_playwright):
    """
    Verify that user can successfully navigate to Login page from Forgot page

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Click the Back to Log in button

    Expected:
    - The Login page is displayed
    """
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.back_to_login_button.click()
    # Verification
    expect(on_login_page.page_title).to_be_visible()
    expect(on_login_page.email_input).to_be_visible()
    expect(on_login_page.password_input).to_be_visible()
    expect(on_login_page.login_button).to_be_visible()
    expect(on_login_page.forgot_password_button).to_be_visible()


def test_navigate_to_the_login_page_successful_message_section(context_and_playwright):
    """
    Verify that user can successfully navigate to the Login page after successfully sending the forgot password request

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page\
    - Send forgot password request
    - Click the Back to log in button

    Expected:
    - The Login page is displayed
    """
    users_list = get_list_from_file("user_credentials.json", "users")
    temp_email_data = get_value_by_key_from_list(users_list, "invalid_password")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.email_input.fill(temp_email_data["email"])
    # Wait until request is finished and then continue
    with page.expect_response(
            f"**/api/account-service/auth-user/forgot-password?email={temp_email_data["email"]}") as resp_info:
        on_forgot_password_page.send_button.click()
    response = resp_info.value
    assert response.ok
    # Verification
    expect(on_forgot_password_page.page_title).to_have_text(FORGOT_PASSWORD_PAGE_SUCCESS)
    on_forgot_password_page.back_to_login_button.click()
    # Verification
    expect(on_login_page.page_title).to_be_visible()
    expect(on_login_page.email_input).to_be_visible()
    expect(on_login_page.password_input).to_be_visible()
    expect(on_login_page.login_button).to_be_visible()
    expect(on_login_page.forgot_password_button).to_be_visible()