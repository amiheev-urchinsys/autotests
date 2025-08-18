from playwright.sync_api import Page
from pageObjects.basePage import BasePage


class SidesPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the Web Automations page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.states_and_exchanges_tab = page.locator('#simple-tab-0')
        self.history_tab = page.locator('#simple-tab-1')
        self.pull_schedule_button = page.get_by_role("button", name="Pull schedule")
        self.test_button = page.get_by_role("button", name="Test")
        self.pull_button = page.get_by_role("button", name="Pull").filter(has_not_text="Pull schedule")
        self.table = page.locator(".MuiTable-root")

