from playwright.sync_api import expect
from datetime import datetime
from data.constants import DOMAIN_STAGE_URL, HOME_PAGE_USER_TITLE, ERROR_TEXT_PASSWORD_LENGTH_MIN, \
    ERROR_TEXT_PASSWORD_DIFFERS, ERROR_TEXT_PASSWORD_SAME_WITH_CURRENT
from pageObjects.loginPage import LoginPage
from pageObjects.updatePasswordPage import UpdatePasswordPage
from utilities.api.api_temp_email import wait_for_email_and_read, delete_emails_in_inbox
from utilities.data_processing import get_create_new_password_link_from_the_email_body, get_key_value_from_file, \
    write_new_password_to_temp_email


def test_send_update_password(context_and_playwright):
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
    # Generate new password
    now = datetime.now()
    timestamp = int(now.timestamp())
    new_password = temp_email_data["password"] + str(timestamp)
    write_new_password_to_temp_email("user_credentials.json", new_password)
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Delete inbox of email if there are letters
    wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the update password form
    page.goto(link)
    on_update_password_page = UpdatePasswordPage(page)
    # Verification
    expect(on_update_password_page.update_button).to_be_disabled()
    on_update_password_page.send_update_password_form(new_password)
    on_update_password_page.back_to_login_button.click()
    # Steps to log in with new password
    on_home_page = on_login_page.login_with_user_credentials(temp_email_data["email"], new_password)
    # Verification
    expect(on_home_page.user_greeting_text).to_have_text(f"{HOME_PAGE_USER_TITLE + temp_email_data["name"]}!")



def test_error_message_is_displayed_when_invalid_value_is_entered_in_the_new_password_input(context_and_playwright):
    """
    This test case verifies that an error message is displayed when invalid value is entered in the New password field

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Fill in all required fields and send the forgot password form
    - Open the email and get the link
    - Open the update password link
    - Enter invalid value in the New password field

    Expected:
    - An error message is displayed under the New Password field

    Post-condition:
    - Delete all received emails
    """
    # Get user data rom the file
    temp_email_data = get_key_value_from_file("user_credentials.json", "temp_email")
    invalid_password_list = get_key_value_from_file("invalid_data.json", "invalid_passwords")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Delete inbox of email if there are letters
    wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the update password form
    page.goto(link)
    on_update_password_page = UpdatePasswordPage(page)
    # Verification
    expect(on_update_password_page.update_button).to_be_disabled()
    for item in invalid_password_list:
        on_update_password_page.new_password_input.fill(item["value"])
        # Verification
        expect(on_update_password_page.error_message).to_have_text(item["error_msg"])
        page.reload()


def test_error_message_is_displayed_when_empty_value_is_entered_in_the_new_password_input(context_and_playwright):
    """
    This test case verifies that an error is displayed when New password input is empty

     Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Fill in all required fields and send the forgot password form
    - Open the email and get the link
    - Open the update password link
    - Enter valid value in the New password field
    - Clear the New password field

    Expected:
    - An error message is displayed under the New Password field

    Post-condition:
    - Delete all received emails
    """
    # Get user data rom the file
    temp_email_data = get_key_value_from_file("user_credentials.json", "temp_email")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Delete inbox of email if there are letters
    wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the update password form
    page.goto(link)
    on_update_password_page = UpdatePasswordPage(page)
    # Verification
    expect(on_update_password_page.update_button).to_be_disabled()
    on_update_password_page.new_password_input.fill("A1@aaaaa")
    on_update_password_page.new_password_input.clear()
    # Verification
    expect(on_update_password_page.error_message).to_have_text(ERROR_TEXT_PASSWORD_LENGTH_MIN)


def test_error_message_is_displayed_when_password_value_are_different(context_and_playwright):
    """
    This test case verifies that the system correctly handles update password attempt with different values in the fields by displaying an appropriate error message.

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Fill in all required fields and send the forgot password form
    - Open the email and get the link
    - Open the update password link
    - Enter valid value in the New password field
    - Enter different valid value in the Confirm new password field

    Expected:
    - An error message is displayed under the Confirm new password field

    Post-condition:
    - Delete all received emails
    """
    # Get user data rom the file
    temp_email_data = get_key_value_from_file("user_credentials.json", "temp_email")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Delete inbox of email if there are letters
    wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the update password form
    page.goto(link)
    on_update_password_page = UpdatePasswordPage(page)
    # Verification
    expect(on_update_password_page.update_button).to_be_disabled()
    on_update_password_page.new_password_input.fill("A1@aaaaa")
    on_update_password_page.confirm_new_password_input.fill("B1@bbbbb")
    # Verification
    expect(on_update_password_page.error_message).to_have_text(ERROR_TEXT_PASSWORD_DIFFERS)


def test_error_message_is_displayed_when_current_password_is_entered(context_and_playwright):
    """
    This test case verifies that the system correctly handles update password attempt with current password in the fields by displaying an appropriate error message.

    Steps:
    - Open the login page
    - Navigate to the Forgot Password page
    - Fill in all required fields and send the forgot password form
    - Open the email and get the link
    - Open the update password link
    - Enter current password in the New password field
    - Enter current password in the Confirm new password field
    - Click the Update button

    Expected:
    - An error message is displayed under the New password field

    Post-condition:
    - Delete all received emails
    """

    # Get user data rom the file
    temp_email_data = get_key_value_from_file("user_credentials.json", "temp_email")
    # Set the browser
    context, playwright = context_and_playwright
    page = context.new_page()
    # Delete inbox of email if there are letters
    wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the forgot password form
    page.goto(DOMAIN_STAGE_URL)
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.send_forgot_password_form(temp_email_data["email"])
    # Verification
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    link = get_create_new_password_link_from_the_email_body(body)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, temp_email_data["inbox_id"], temp_email_data["x_api_key"])
    assert response.ok
    # Steps to send the update password form
    page.goto(link)
    on_update_password_page = UpdatePasswordPage(page)
    # Verification
    expect(on_update_password_page.update_button).to_be_disabled()
    on_update_password_page.new_password_input.fill(temp_email_data["password"])
    on_update_password_page.confirm_new_password_input.fill(temp_email_data["password"])
    with on_update_password_page.page.expect_response("**/api/account-service/auth-user/create-password") as resp_info:
        on_update_password_page.update_button.click()
    response = resp_info.value
    assert response.status == 400
    # Verification
    expect(on_update_password_page.error_message).to_have_text(ERROR_TEXT_PASSWORD_SAME_WITH_CURRENT)
