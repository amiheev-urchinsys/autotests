from playwright.sync_api import Playwright, expect

from pageObjects.loginPage import LoginPage
from pageObjects.updatePasswordPage import UpdatePasswordPage
from utilities.api.api_temp_email import wait_for_email_and_read, delete_emails_in_inbox
from utilities.data_processing import get_create_new_password_link_from_the_email_body


def test_update_password(playwright: Playwright):
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
    email = "user-7d53eb27-1e37-4b41-a8ee-50b5492a5f2b@mailslurp.biz"
    # Set the browser
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Steps send the forgot password form
    page.goto("https://studio.dev.plextera.com/")
    on_login_page = LoginPage(page)
    on_forgot_password_page = on_login_page.navigate_to_forgot_password_page()
    on_forgot_password_page.email_input.fill(email)
    # Wait until request is finished and then continue
    with page.expect_response(
            f"**/api/account-service/auth-user/forgot-password?email={email}") as resp_info:
        on_forgot_password_page.send_button.click()
    response = resp_info.value
    assert response.ok
    on_forgot_password_page.back_to_login_button.is_visible()
    # Steps to get update password link from email
    body = wait_for_email_and_read(playwright, "7d53eb27-1e37-4b41-a8ee-50b5492a5f2b")
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
    on_home_page = on_login_page.login_with_user_credentials(email,"EM#@YgnHy9")
    expected_text = "Welcome back, testing!"
    expect(on_home_page.user_greeting_text).to_have_text(expected_text)
    # Delete all emails in the inbox
    response = delete_emails_in_inbox(playwright, "7d53eb27-1e37-4b41-a8ee-50b5492a5f2b")
    assert response.ok