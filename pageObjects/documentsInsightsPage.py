from playwright.sync_api import Page

from data.constants import DOCUMENTS_INSIGHTS_PROCESSED_TAB_TITLE, DOCUMENTS_INSIGHTS_PENDING_TAB_TITLE, \
    DOCUMENTS_INSIGHTS_QUEUED_TAB_TITLE, DOCUMENTS_INSIGHTS_REJECTED_TITLE
from pageObjects.basePage import BasePage


class DocumentsInsightsPage(BasePage):

    def __init__(self, page: Page):
        """
        Initializes the Hubs page object with web element locators.

        :param page: Playwright Page object representing the browser tab or frame.
        """
        super().__init__(page)
        self.hubs_button = page.get_by_role("button", name="Hubs")
        self.page_title = page.locator('.header__content h1')
        self.reports_button = page.get_by_role("button", name="Reports")
        self.processed_tab = page.get_by_text(DOCUMENTS_INSIGHTS_PROCESSED_TAB_TITLE).first
        self.pending_tab = page.get_by_text(DOCUMENTS_INSIGHTS_PENDING_TAB_TITLE)
        self.queued_tab = page.get_by_text(DOCUMENTS_INSIGHTS_QUEUED_TAB_TITLE)
        self.rejected_tab = page.get_by_text(DOCUMENTS_INSIGHTS_REJECTED_TITLE)
        self.hubs_page = self.HubsPage(page)

    class HubsPage(BasePage):

        def __init__(self, page: Page):
            """
            Initializes the Hubs page object with web element locators.

            :param page: Playwright Page object representing the browser tab or frame.
            """
            super().__init__(page)
            self.page_title = page.locator('div[class="page-content"] span[class="name"]')
            self.create_a_hub_button = page.get_by_role("button", name="Create A Hub")
            self.outline_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(1)')
            self.next_button = page.get_by_role("button", name="Next")
            self.loading_popup_title = page.locator('.loading')
            self.loading_popup_description = page.locator('.text')
            self.hub_page = DocumentsInsightsPage.HubsPage.HubPage(page)
            self.value_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(2)')


        def create_outline_based_hub(self):
            self.create_a_hub_button.click()
            self.outline_based_type_card.click()
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/default-name") as resp_info:
                self.next_button.click()
            response = resp_info.value
            assert response.ok
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/create") as create_resp_info, \
                    self.page.expect_response("**/api/hubs/**?include=short_outline,channels") as data_resp:
                self.next_button.click()
            create_response = create_resp_info.value
            data_response = data_resp.value
            assert create_response.ok
            assert data_response.ok

        def create_value_based_hub(self):
            self.create_a_hub_button.click()
            self.value_based_type_card.click()
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/default-name") as resp_info:
                self.next_button.click()
            response = resp_info.value
            assert response.ok
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/create") as create_resp_info, \
                    self.page.expect_response("**/api/hubs/**?include=short_outline,channels") as data_resp, \
                    self.page.expect_response("**/api/classification-classes/**") as smth_resp:
                self.next_button.click()
            create_response = create_resp_info.value
            data_response = data_resp.value
            smth = smth_resp.value
            assert create_response.ok
            assert data_response.ok
            assert smth.ok

        class HubPage(BasePage):

            def __init__(self, page: Page):
                """
                Initializes the Hubs page object with web element locators.

                :param page: Playwright Page object representing the browser tab or frame.
                """
                super().__init__(page)
                # General elements
                self.gear_button = page.locator('.tab-header span[kind="greyOutlined"]')
                self.edit_hub_name = page.locator('.page__header-left span[kind="greyOutlined"]')
                self.save_button = page.get_by_role("button", name="Save")
                self.single_radiobutton = page.locator(".radio-button-label .text").filter(has_text="Single")
                self.group_radiobutton = page.locator(".radio-button-label .text").filter(has_text="Group")
                self.list_radiobutton = page.locator(".radio-button-label .text").filter(has_text="List")

                # Outline based hub
                self.add_new_field_button = page.get_by_role("button", name="+ Add new field")
                self.drag_and_drop_files_button = page.locator(".direct-upload-dropzone")
                self.browse_files_button = page.locator(".open-upload")
                self.single_field_label_title = page.locator(".name_box")
                self.list_group_field_label_title = page.locator('ul[role="tree"]')
                self.nested_add_new_field = page.locator('//*[@id="scroll"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/ul/div/li/div/div[2]/div/div[2]/span[3]')
                self.arrow_button = page.locator('.chevron.undefined')
                self.nested_group_label = page.locator(".MuiTreeItem-group.MuiCollapse-entered")

                # Value based hub
                self.upload_documents_button = page.get_by_role("button", name="Upload Documents")
                self.add_data_points_button = page.get_by_role("button", name="ADD DATA POINTS")
                self.import_data_points_in_json_format_button = page.get_by_role("button", name="import data points in json format")
                self.data_points_tab = page.locator("[id*='hubs_data-points-tab']")
                self.dictionary_tab = page.locator("[id*='hubs_synonyms-tab']")
                self.classification_tab = page.locator("[id*='hubs_classificatio-tab']")
                self.field_name_input = page.locator('input[placeholder="Add field name"]')
                self.searchable_checkbox = page.locator('span[class="type"]').filter(has_text="Searchable")