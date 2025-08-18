from playwright.sync_api import Page
from pageObjects.basePage import BasePage


class WebAutomationsPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the Web Automations page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.create_button = page.get_by_role("button", name="Create").filter(has_not_text="Created")
        self.import_button = page.get_by_role("button", name="Import")
        self.web_automation_page = self.WebAutomationPage(page)
        self.file_input = page.locator("input[type='file']")
        self.table = page.locator('[tablename="automations"]')
        self.automations_tab = page.locator(".nav-item.ng-star-inserted a").filter(has_text="Automations")
        self.fragments_tab = page.locator(".nav-item.ng-star-inserted a").filter(has_text="Fragments")
        self.credentials_tab = page.locator(".nav-item.ng-star-inserted a").filter(has_text="Credentials")
        self.no_data_row = page.locator('.mat-cell')


    def upload_file(self, document):
        """
        Uploads a web automation file to create a web automation

        :param document: Document name with its type, example 'name.json'
        """
        self.file_input.set_input_files("data/" + document + "")

    class WebAutomationPage(BasePage):
        def __init__(self, page: Page):
            """
            Initializes the Web Automation page object with web element locators.

            :param page: Playwright Page object representing the browser tab or frame.
            """
            super().__init__(page)
            self.save_button = page.get_by_role("button", name="Save")
