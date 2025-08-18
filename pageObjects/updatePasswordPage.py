from playwright.sync_api import Page


class UpdatePasswordPage:
    def __init__(self, page: Page):
        """
        Initializes the Home page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.page_title = page.locator('div[class="update"] h1')
        self.page_description = page.locator('div[class="update"] p[class="update__text"]')
        self.new_password_input = page.locator('#password')
        self.confirm_new_password_input = page.locator('#passwordConfirmation')
        self.update_button = page.get_by_role("button", name="Update")
        self.back_to_login_button = page.get_by_role("button", name="Back to log in")
        self.error_message = page.locator('[type="ERROR"]')


    def navigate_to_login_page(self):
        from pageObjects.loginPage import LoginPage
        self.back_to_login_button.click()

        login_page = LoginPage(self.page)
        return login_page

    def send_update_password_form(self, new_password):
        self.new_password_input.fill(new_password)
        self.confirm_new_password_input.fill(new_password)
        # Wait until request is finished and then continue
        with self.page.expect_response("**/api/account-service/auth-user/create-password") as resp_info:
            self.update_button.click()
        response = resp_info.value
        assert response.ok