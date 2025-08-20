from playwright.sync_api import Page
from pageObjects.basePage import BasePage

class AlertsPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the Alers page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.page_title = page.locator('.page-content .header')
        self.filter_button = page.get_by_role("button", name="Filter").filter(has_not_text="Reset Filters")
        self.reset_filters_button = page.get_by_role("button", name="Reset Filters")
        self.table = page.locator(".page-content table")
        self.no_data_available_text = page.locator(".content p")