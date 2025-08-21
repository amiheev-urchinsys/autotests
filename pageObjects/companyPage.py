from playwright.sync_api import Page

from pageObjects.basePage import BasePage


class CompanyPage(BasePage):

    def __init__(self, page: Page):
        """
        Filter Tab component within the Companies tab.

        :param page: Playwright Page object.
        """
        super().__init__(page)
        self.sidebar_add_ons = page.locator('div.tab__left').filter(has_text="Add-ons")
        self.add_ons_tab = self.AddOns(page)
        self.invite_company_user_button = page.locator(".tab__content-header .link")

    def send_invite_company_user_form(self, user_email):
        self.popups.invite_company_user_email_address_input.fill(user_email)
        self.popups.invite_company_user_role_selector.click()
        self.popups.invite_company_user_role_selector_list_user_point.click()
        with self.page.expect_response("**/api/account-service/admin-console/organizations/**/invite/organization-user") as resp_info:
            self.popups.invite_button.click()
        response = resp_info.value
        assert response.ok

    def send_invite_company_administrator_form(self, user_email):
        self.popups.invite_company_user_email_address_input.fill(user_email)
        self.popups.invite_company_user_role_selector.click()
        self.popups.invite_company_user_role_selector_list_administrator_point.click()
        with self.page.expect_response("**/api/account-service/admin-console/organizations/**/invite/organization-user") as resp_info:
            self.popups.invite_button.click()
        response = resp_info.value
        assert response.ok


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


