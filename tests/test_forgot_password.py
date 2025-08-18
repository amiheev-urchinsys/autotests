from playwright.sync_api import expect

from data.constants import DOMAIN_STAGE_URL, FORGOT_PASSWORD_PAGE_ERROR_EMPTY_EMAIL, \
    FORGOT_PASSWORD_PAGE_ERROR_INVALID_FORMAT, FORGOT_PASSWORD_PAGE_SUCCESS, FORGOT_PASSWORD_PAGE_DESCRIPTION_PART_ONE, \
    FORGOT_PASSWORD_PAGE_DESCRIPTION_PART_TWO, FORGOT_PASSWORD_LETTER_LINK_PART
from pageObjects.loginPage import LoginPage
from utilities.api.api_temp_email import wait_for_email_and_read, delete_emails_in_inbox
from utilities.data_processing import get_create_new_password_link_from_the_email_body, get_key_value_from_file


def test_send_forgot_password_form(context_and_playwright):
    """
    This test verifies that a user can successfully:
    - Send forgot password form
    - Navigate to the Update password page using link from the email letter
    - Send update password form
    - Authenticate with new password

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Fill in all required fields and send the forgot password form
    - Open the email and get the link
    - Open the update password link
    - Fill in all the required fields and send the update password form
    - Navigate to the login page and authenticate with new password

    Expected:
    - The home page is displayed after login.
    - The user greeting message contains the text 'Welcome back, username'.

    Post-condition:
    - Delete all received emails
    """
    # Get user data rom the file
    temp_email_data = get_key_value_from_file("user_credentials.json", "temp_email")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps to send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    expect(on_forgot_password_page.page_title).to_have_text(FORGOT_PASSWORD_PAGE_SUCCESS)
    on_forgot_password_page.back_to_login_button.is_visible()
    expect(on_forgot_password_page.description_text).to_have_text(FORGOT_PASSWORD_PAGE_DESCRIPTION_PART_ONE)
    expect(on_forgot_password_page.resend_reset_email_text).to_have_text(FORGOT_PASSWORD_PAGE_DESCRIPTION_PART_TWO)
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    assert link.startswith(FORGOT_PASSWORD_LETTER_LINK_PART)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
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
    invalid_emails_list = get_key_value_from_file("invalid_data.json", "invalid_emails")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    for item in invalid_emails_list:
        on_forgot_password_page.email_input.fill(item["value"])
        on_forgot_password_page.send_button.click()
        # Verification
        expect(on_forgot_password_page.error_message).to_have_text(FORGOT_PASSWORD_PAGE_ERROR_INVALID_FORMAT)
        page.reload()


def test_navigate_to_the_login_page_from_the_forgot_password_form(context_and_playwright):
    """
    Verify that user can successfully navigate to Login page from Forgot password page

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
    - Navigate to the Forgot Password page
    - Send forgot password request
    - Click the Back to log in button

    Expected:
    - The Login page is displayed

    Post-condition:
    - Delete all received emails
    """
    temp_email_data = get_key_value_from_file("user_credentials.json", "temp_email")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Steps send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    expect(on_forgot_password_page.page_title).to_have_text(FORGOT_PASSWORD_PAGE_SUCCESS)
    # Navigate to Login page
    on_forgot_password_page.back_to_login_button.click()
    # Verification
    expect(on_login_page.page_title).to_be_visible()
    expect(on_login_page.email_input).to_be_visible()
    expect(on_login_page.password_input).to_be_visible()
    expect(on_login_page.login_button).to_be_visible()
    expect(on_login_page.forgot_password_button).to_be_visible()
    # Delete all emails in the inbox
    wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
