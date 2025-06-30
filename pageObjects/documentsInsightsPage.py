from playwright.sync_api import Page


class DocumentsInsightsPage:
    def __init__(self, page: Page):
        """
        Initializes the Documents Insights page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.hubs_button = page.locator('.header__content button')

