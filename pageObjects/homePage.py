from playwright.sync_api import Page
from pageObjects.basePage import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the HomePage object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.user_greeting_text = page.locator('.page-content .greeting').first
        self.main_greeting_text = page.locator('.content .greeting')
        self.description_text = page.locator('.content .info')


