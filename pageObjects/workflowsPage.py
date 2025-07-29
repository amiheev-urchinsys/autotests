from playwright.sync_api import Page


class WorkflowsPage:
    def __init__(self, page: Page):
        """
                Initializes the Home page object with web element locators.

                :param page: Playwright Page object representing the browser tab or frame.
                """
        self.page = page
        self.workflows_tab = page.get_by_role("button", name="Workflows")
        self.runs_tab = page.get_by_role("button", name="Runs")
        self.page_title = page.locator(".content h1")
        self.page_description = page.locator(".content p")
        self.add_new_workflow_button = page.get_by_role("button", name="Add new workflow")