from playwright.sync_api import Page


class CompanyPage:

    def __init__(self, page: Page):
        """
        Filter Tab component within the Companies tab.

        :param page: Playwright Page object.
        """
        self.page = page
        self.sidebar_add_ons = page.locator('div.tab__left').filter(has_text="Add-ons")
        self.add_ons_tab = self.AddOns(page)

    class AddOns:
        def __init__(self, page: Page):
            """
            Filter Tab component within the Companies tab.

            :param page: Playwright Page object.
            """
            self.page = page
            self.web_automation_checkbox = page.locator('label span').filter(has_text="Web Automations")
            self.documents_insights_checkbox = page.locator('label span').filter(has_text="Document Insights")
            self.sides_checkbox = page.locator('label span').filter(has_text="SIDES")
            self.datastores_checkbox = page.locator('label span').filter(has_text="Datastores")
            self.forms_checkbox = page.locator('label span').filter(has_text="Forms")
            self.save_button = page.get_by_role("button", name="Save")
            self.popup_save_button = page.locator('div[width = "720"][tabindex = "-1"] button').filter(has_text="Save")


