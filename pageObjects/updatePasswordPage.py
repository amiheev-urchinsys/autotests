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


    def navigate_to_login_page(self):
        from pageObjects.loginPage import LoginPage
        self.back_to_login_button.click()

        login_page = LoginPage(self.page)
        return login_page
