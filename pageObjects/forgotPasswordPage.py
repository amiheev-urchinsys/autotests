from playwright.sync_api import Page


class ForgotPasswordPage:
    def __init__(self, page: Page):
        """
        Initializes the Home page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.email_input = page.locator('input[name="email"]')
        self.send_button = page.get_by_role("button", name="Send")
        self.back_to_login_button = page.get_by_role("button", name="Back to log in")
        self.page_title = page.locator('.forgot__head h1')

    def return_to_login_page(self):
        from pageObjects.loginPage import LoginPage
        self.back_to_login_button.click()

        login_page = LoginPage(self.page)
        return login_page