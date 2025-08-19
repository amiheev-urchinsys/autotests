from playwright.sync_api import Page
from pageObjects.basePage import BasePage


class DatastoresPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the Datastores page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.page_title = page.locator('.page-content .header')
        self.add_new_button = page.get_by_role("button", name="Add New")
        self.table = page.locator(".table-wrapper table")
        self.no_data_available_text = page.locator(".table-wrapper .content")


