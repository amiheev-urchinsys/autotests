from playwright.sync_api import Page


class ForgotPasswordPage:
    def __init__(self, page: Page):
        """
        Initializes the Home page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.email_input = page.locator('div[class="forgot"] input[name="email"]')
        self.send_button = page.get_by_role("button", name="Send")
        self.back_to_login_button = page.get_by_role("button", name="Back to log in")
        self.page_title = page.locator('div.forgot__head h1')
        self.error_message = page.locator('[type="ERROR"]')
        self.description_text = page.locator('div.forgot__text p:nth-child(1)')
        self.resend_reset_email_text = page.locator('div.forgot__text p:nth-child(2)')


    def navigate_to_login_page(self):
        from pageObjects.loginPage import LoginPage
        self.back_to_login_button.click()

        login_page = LoginPage(self.page)
        return login_page

    def send_forgot_password_form(self, user_email):
        self.email_input.fill(user_email)
        # Wait until request is finished and then continue
        with self.page.expect_response(
                f"**/api/account-service/auth-user/forgot-password?email={user_email}") as resp_info:
            self.send_button.click()
        response = resp_info.value
        assert response.ok