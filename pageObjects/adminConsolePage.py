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
            self.filter_button = page.get_by_role("button", name="Filter")
            self.filter_tab = AdminConsolePage.CompaniesTab.FilterTab(page)
            self.table_row = page.locator('tbody tr')
            self.company_row = page.locator('tbody div').filter(has_text="testingCompany")

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
