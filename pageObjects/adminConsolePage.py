from playwright.sync_api import Page




class AdminConsolePage:

    def __init__(self, page: Page):
        """
        Initializes the Admin Console object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        self.sidebar_internal_users_tab = page.locator('div.tab__left').filter(has_text="Internal Users")
        self.sidebar_companies_tab = page.locator('div.tab__left').filter(has_text="Companies")
        self.companies_tab = self.CompaniesTab(page)

    class CompaniesTab:

        def __init__(self, page: Page):
            """
            Companies tab component within the Admin Console page.

            :param page: Playwright Page object.
            """
            self.page = page
            self.invite_new_owner_button = page.get_by_role("button", name="Invite new owner")
            self.filter_button = page.get_by_role("button", name="Filter")
            self.filter_tab = AdminConsolePage.CompaniesTab.FilterTab(page)
            self.invite_new_owner_user_popup = AdminConsolePage.CompaniesTab.InviteNewOwnerUserPopUp(page)
            self.table_row = page.locator('tbody tr')
            self.company_row = page.locator('tbody div').filter(has_text="testingCompany")
            self.success_popup = AdminConsolePage.CompaniesTab.SuccessPopUp(page)

        def navigate_to_company_page(self):
            from pageObjects.companyPage import CompanyPage
            self.company_row.click()

            company_page = CompanyPage(self.page)
            return company_page

        class FilterTab:

            def __init__(self, page: Page):
                """
                Filter Tab component within the Companies tab.

                :param page: Playwright Page object.
                """
                self.page = page
                self.company_input = page.locator('input[name="organizationName"]')
                self.apply_button = page.get_by_role("button", name="Apply")

        class InviteNewOwnerUserPopUp:

            def __init__(self, page: Page):
                """
                Popup Invite New Owner User component within the Companies tab.

                :param page: Playwright Page object.
                """
                self.page = page
                self.email_input = page.get_by_role("textbox", name="Email address")
                self.invite_button = page.get_by_role("button", name="Invite")

        class SuccessPopUp:

            def __init__(self, page: Page):
                """
                Popup Invite New Owner User component within the Companies tab.

                :param page: Playwright Page object.
                """
                self.page = page
                self.title = page.locator('div[role="presentation"] h3')
