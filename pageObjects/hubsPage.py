from playwright.sync_api import Page
from pageObjects.basePage import BasePage


class HubsPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the Hubs page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.page = page
        self.page_title = page.locator('div[class="page-content"] span[class="name"]')
        self.create_a_hub_button = page.get_by_role("button", name="Create A Hub")
        self.outline_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(1)')
        self.create_a_hub_next_button = page.get_by_role("button", name="Next")

