from playwright.sync_api import Page
from pageObjects.basePage import BasePage

class FormsPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the FORMS page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.page_title = page.locator('.page-content .header h1')
        self.create_form_button = page.get_by_role("button", name="Create Form")
        self.table = page.locator(".page-content table")
        self.no_data_available_text = page.locator(".content p")