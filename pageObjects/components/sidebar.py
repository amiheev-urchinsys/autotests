from playwright.sync_api import Page


class Sidebar:
    def __init__(self, page: Page):
        self.page = page
        self.company_selector = page.locator('.organization')
        self.home_point = page.locator('li span').filter(has_text="Home")
        self.workflows_point = page.locator('li span').filter(has_text="Workflows")
        self.web_automation_point = page.locator('li span').filter(has_text="Web Automations")
        self.document_insights_point = page.locator('li span').filter(has_text="Document Insights")
        self.sides_point = page.locator('li span').filter(has_text="SIDES")
        self.datastores_point = page.locator('li span').filter(has_text="Datastores")
        self.forms_point = page.locator('li span').filter(has_text="Forms")
        self.sidebar_bottom_section = page.locator('.bottom-section')
        self.personal_cabinet_dropdown_menu = page.locator('.bottom-section .name')
        self.personal_cabinet_settings_point = page.locator('span').filter(has_text="Settings")
        self.personal_cabinet_admin_console_point = page.locator('span').filter(has_text="Admin Console")
        self.personal_cabinet_log_out_point = page.locator('span').filter(has_text="Log out")
        self.toggle_button = page.locator('button[aria-label="toggle"]')
        self.logo = page.locator('.logo')

    def logout(self):
        self.sidebar_bottom_section.hover()
        self.personal_cabinet_dropdown_menu.click()
        self.personal_cabinet_log_out_point.click()

    def open_personal_cabinet_menu(self):
        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        self.personal_cabinet_dropdown_menu.click()

    def navigate_to_admin_console_page(self):
        from pageObjects.adminConsolePage import AdminConsolePage

        self.open_personal_cabinet_menu()
        self.personal_cabinet_admin_console_point.click()
        admin_console_page = AdminConsolePage(self.page)

        return admin_console_page

    def navigate_to_documents_insights_page(self):
        from pageObjects.documentsInsightsPage import DocumentsInsightsPage
        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response("**/api/ocr/history?status=done&size=10&searchBy=NAME") as resp_info:
            self.document_insights_point.click()
        response = resp_info.value
        assert response.ok
        documents_insights_page = DocumentsInsightsPage(self.page)
        return documents_insights_page
