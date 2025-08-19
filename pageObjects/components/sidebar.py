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
        self.user_menu_dropdown = page.locator('.bottom-section .name')
        self.user_menu_settings_point = page.locator('span').filter(has_text="Settings")
        self.user_menu_admin_console_point = page.locator('span').filter(has_text="Admin Console")
        self.user_menu_log_out_point = page.locator('span').filter(has_text="Log out")
        self.toggle_button = page.locator('button[aria-label="toggle"]')
        self.logo = page.locator('.logo')
        self.alerts_point = page.locator('li span').filter(has_text="Alerts")

    def logout(self):
        self.sidebar_bottom_section.hover()
        self.user_menu_dropdown.click()
        self.user_menu_log_out_point.click()

    def open_user_menu(self):
        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        self.user_menu_dropdown.click()

    def navigate_to_admin_console_page(self):
        from pageObjects.adminConsolePage import AdminConsolePage

        self.open_user_menu()
        self.user_menu_admin_console_point.click()
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

    def navigate_to_web_automations_page(self):
        from pageObjects.webAutomationsPage import WebAutomationsPage

        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response("**/api/sbb/automation/list?page=0&size=25&sortDirection=DESC&sortBy=createdOn") as resp_info, \
                self.page.expect_response("**/api/sbb/automation/**") as resp2_info:
            self.web_automation_point.click()
        assert resp_info.value.ok
        assert resp2_info.value.ok
        web_automations_page = WebAutomationsPage(self.page)

        return web_automations_page

    def navigate_to_workflows_page(self):
        from pageObjects.workflowsPage import WorkflowsPage

        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response(
                "**/api/studio/workflow/list") as resp_info:
            self.workflows_point.click()
        assert resp_info.value.ok
        workflows_page = WorkflowsPage(self.page)

        return workflows_page

    def navigate_to_sides_page(self):
        from pageObjects.sidesPage import SidesPage

        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response(
                "**/api/sides/schedules") as resp_info:
            self.sides_point.click()
        assert resp_info.value.ok
        sides_page = SidesPage(self.page)

        return sides_page


    def navigate_to_datastores_page(self):
        from pageObjects.datastoresPage import DatastoresPage

        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response(
                "**/api/studio/datasource/configuration?page=0&size=10") as resp_info:
            self.datastores_point.click()
        assert resp_info.value.ok
        datastores_page = DatastoresPage(self.page)

        return datastores_page


    def navigate_to_forms_page(self):
        from pageObjects.formsPage import FormsPage

        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response(
                "**/api/studio/forms?page=0&size=10") as resp_info:
            self.forms_point.click()
        assert resp_info.value.ok
        forms_page = FormsPage(self.page)

        return forms_page


    def navigate_to_alerts_page(self):
        from pageObjects.alertsPage import AlertsPage

        self.sidebar_bottom_section.hover()
        self.toggle_button.click()
        # Wait until request is finished and then continue
        with self.page.expect_response(
                "**/api/issues-service/issues?page=0&size=10&sortBy=severity&sortDirection=DESC&status=OPEN") as resp_info:
            self.alerts_point.click()
        assert resp_info.value.ok
        alerts_page = AlertsPage(self.page)

        return alerts_page