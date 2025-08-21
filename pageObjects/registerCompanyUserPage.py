from playwright.sync_api import Page


class RegisterCompanyUserPage:
    def __init__(self, page: Page):
        """
        Initializes the Register Company User page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.first_name_input = page.locator('div[class="register"] input[name="firstName"]')
        self.last_name_input = page.locator('div[class="register"] input[name="lastName"]')
        self.password_input = page.locator('div[class="register"] input[name="password"]')
        self.confirm_password_input = page.locator('div[class="register"] input[name="passwordConfirmation"]')
        self.privacy_policy_checkbox = page.locator('div[class="register"] input[name="privacy"]')
        self.terms_of_use_checkbox = page.locator('div[class="register"] input[name="terms"]')
        self.register_button = page.get_by_role("button", name="Register")
        self.success_page = RegisterCompanyUserPage.SuccessPage(page)

    def send_the_register_new_company_user_form(self, first_name, last_name, password):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.password_input.fill(password)
        self.confirm_password_input.fill(password)
        # Wait until request is finished and then continue
        with self.page.expect_response("**/api/account-service/auth-user/register-invite") as resp_info:
            self.register_button.click()
        response = resp_info.value
        assert response.ok


    class SuccessPage:

        def __init__(self, page: Page):
            """
            Initializes the Success page object with web element locators.

            :param page: Playwright Page object representing the browser tab or frame.
            """
            self.page = page
            self.title = page.locator('div[class="register"] h1')
            self.description = page.locator('div[class="register"] div[class="register__text"] p')
            self.go_to_log_in_button = page.get_by_role("button", name="Go to log in")

        def navigate_to_login_page(self):
            from pageObjects.loginPage import LoginPage
            self.go_to_log_in_button.click()
            login_page = LoginPage(self.page)
            return login_page