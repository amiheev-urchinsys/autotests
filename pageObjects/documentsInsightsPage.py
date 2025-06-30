from playwright.sync_api import Page




class DocumentsInsightsPage:
    def __init__(self, page: Page):
        """
        Initializes the Documents Insights page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.hubs_button = page.get_by_role("button", name="Hubs")

    def navigate_to_hubs_page(self):
        from pageObjects.hubsPage import HubsPage

        self.hubs_button.click()
        hubs_page = HubsPage(self.page)
        return hubs_page
