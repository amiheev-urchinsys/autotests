import time

from playwright.sync_api import Page

from data.constants import DOCUMENTS_INSIGHTS_PROCESSED_TAB_TITLE, DOCUMENTS_INSIGHTS_PENDING_TAB_TITLE, \
    DOCUMENTS_INSIGHTS_QUEUED_TAB_TITLE, DOCUMENTS_INSIGHTS_REJECTED_TITLE, HUB_PAGE_VALUE_SINGLE_FIELD_NAME, \
    HUB_PAGE_VALUE_GROUP_FIELD_NAME, HUB_PAGE_VALUE_LIST_FIELD_NAME, HUB_PAGE_VALUE_NESTED_FIELD_NAME
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
            self.loading_popup_title = page.locator('.loading')
            self.loading_popup_description = page.locator('.text')
            self.hub_page = DocumentsInsightsPage.HubsPage.HubPage(page)
            self.empty_state_text = page.locator("#scroll div:nth-child(2) span")
            self.hub_card = page.locator("//div[contains(@class, 'hub-item')]")
            self.hub_card_meatball_menu = page.locator("//div[contains(@class, 'open-hub-actions')]")
            self.hub_card_meatball_menu_delete_point = page.locator("//div[contains(@class, 'remove-hub')]")
            self.hub_card_switch = page.locator("//div[contains(@class, 'toggle-enable')]")
            self.hub_card_meatball_menu_view_details_point = page.locator("//div[contains(@id, 'hubs_menu-view-details')]")
            self.hub_card_meatball_menu_rename_point = page.locator("//div[contains(@class, 'rename-hub')]")
            self.hub_card_title = page.locator("(//div[contains(@class, 'hub-item')] //span[@title])[2]")
            self.hub_card_meatball_menu_tags_point = page.locator("//div[contains(@id, 'hubs_menu-tags')]")
            self.hub_card_description = page.locator('//div[contains(@id,"clamped-content-description-for-")]')

        def create_outline_based_hub(self, all_field_populated: bool = False):
            """
            Creates an outline based hub and returns hub id and name
            If received value is 'true', then all fields will be populated, else only required fields will be populated.

            :param all_field_populated: Can be True or False. Default value is False
            :return: hub ID and hub name
            """
            self.create_a_hub_button.click()
            self.popups.create_hub_outline_based_type_card.click()
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/default-name") as resp_info:
                self.popups.next_button.click()
            response = resp_info.value
            assert response.ok
            if all_field_populated:
                self.popups.create_hub_description_input.fill("description")
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/create") as create_resp_info, \
                    self.page.expect_response("**/api/hubs/**?include=short_outline,channels") as data_resp:
                self.popups.next_button.click()
            assert create_resp_info.value.ok
            assert data_resp.value.ok
            outline_hub_id = create_resp_info.value.json()["id"]
            outline_hub_name = create_resp_info.value.json()["name"]
            return outline_hub_id, outline_hub_name

        def create_value_based_hub(self, all_field_populated: bool = False, extractor_type: bool = False):
            """
            Creates a value based hub and returns hub id and name
            If received value is 'true', then all fields will be populated, else only required fields will be populated.

            :param all_field_populated: Can be True or False. Default value is False
            :return: hub ID and hub name
            """
            self.create_a_hub_button.click()
            self.popups.create_hub_value_based_type_card.click()
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/default-name") as resp_info:
                self.popups.next_button.click()
            response = resp_info.value
            assert response.ok
            if all_field_populated:
                self.popups.create_hub_description_input.fill("description")
                self.popups.create_hub_additional_options_checkbox.click()
                if extractor_type:
                    self.popups.create_hub_label_based_extractor_radiobutton.click()
            # Wait until after the click on the Next button the '/api/hubs/default-name' request will be finished successfully
            with self.page.expect_response("**/api/hubs/create") as create_resp_info, \
                    self.page.expect_response("**/api/hubs/**?include=short_outline,channels") as data_resp, \
                    self.page.expect_response("**/api/classification-classes/**") as smth_resp:
                self.popups.next_button.click()
            assert create_resp_info.value.ok
            assert data_resp.value.ok
            assert smth_resp.value.ok
            value_hub_id = create_resp_info.value.json()["id"]
            value_hub_name = create_resp_info.value.json()["name"]
            return value_hub_id, value_hub_name

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
                self.arrow_button = page.locator('.chevron.undefined')
                self.nested_group_label = page.locator(".MuiTreeItem-group.MuiCollapse-entered")
                self.delete_button = page.get_by_role("button", name="Delete")
                self.delete_group_type_field_icon = page.locator(
                    '(//div[@class="MuiTreeItem-content"]//span[@kind="greyOutlined"])[2]')
                self.file_input = page.locator("input[type='file']")
                self.navigate_to_hubs_page_button = page.locator(".page__header-left div span")

                # Outline based hub
                self.add_new_field_button = page.get_by_role("button", name="+ Add new field")
                self.drag_and_drop_files_button = page.locator(".direct-upload-dropzone")
                self.browse_files_button = page.locator(".open-upload")
                self.single_field_label_title = page.locator(".name_box")
                self.list_group_field_label_title = page.locator('ul[role="tree"]')
                self.nested_add_new_field = page.locator('//*[@id="scroll"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/ul/div/li/div/div[2]/div/div[2]/span[3]')
                self.arrow_button = page.locator('.chevron.undefined')
                self.nested_group_label = page.locator(".MuiTreeItem-group.MuiCollapse-entered")
                self.delete_single_type_field_icon_outline = page.locator('(//div[@class="rigth_box"]//span[@kind="greyOutlined"])[2]')
                self.meatball_menu = page.locator(".open-hub-actions")
                self.no_fields_text = page.locator(".field_text")
                self.fields_list_text_title = page.locator(".tab-content .name")
                self.outline_template_name = page.locator(".box_name")
                self.outline_template_switch = page.locator("//div[contains(@class, 'toggle-enable')]")
                self.outline_template_meatball_menu = page.locator("//div[contains(@class, 'open-hub-actions')]")
                self.outline_template_footer = page.locator(".box_container footer")
                self.outline_template_meatball_menu_rename_point = page.locator("//div[contains(@class, 'rename-hub')]")
                self.rename_popup_input = page.locator('input[placeholder="Outline name"]')
                self.rename_popup_cancel_button = page.get_by_role("button", name="Cancel")
                self.outline_template_meatball_menu_delete_point = page.locator("//div[contains(@class, 'remove-hub')]")
                self.outline_template_card = page.locator(".box_container")

                # Value based hub
                self.upload_documents_button = page.get_by_role("button", name="Upload Documents")
                self.add_data_points_button = page.get_by_role("button", name="ADD DATA POINTS")
                self.import_data_points_in_json_format_button = page.get_by_role("button", name="import data points in json format")
                self.data_points_tab = page.locator("[id*='hubs_data-points-tab']")
                self.dictionary_tab = page.locator("[id*='hubs_synonyms-tab']")
                self.nested_value_add_new_field = page.locator('//*[@id="scroll"]/div/div[2]/div[2]/div/div/div/ul/div/div/ul/li/div/div[2]/div/div[2]/span[3]')
                self.classification_tab = page.locator("[id*='hubs_classificatio-tab']")
                self.field_name_input = page.locator('input[placeholder="Add field name"]')
                self.searchable_checkbox = page.locator('(//div[@class="option"] //span[@class="MuiIconButton-label"])[1] /input')
                self.delete_single_type_field_icon = page.locator('span[id*="hubs_delete-data-point"]')
                self.delete_group_type_field_icon = page.locator('(//div[@class="MuiTreeItem-content"]//span[@kind="greyOutlined"])[2]')
                self.no_data_points_title_text = page.locator(".tab-content h4")
                self.no_data_points_description_text = page.locator(".tab-content p")
                self.added_field = page.locator('ul[role="tree"] .MuiTreeItem-content')
                self.single_field = page.locator('ul[role="tree"] .MuiTreeItem-content').filter(has_text=HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
                self.group_field = page.locator('ul[role="tree"] .MuiTreeItem-content').filter(has_text=HUB_PAGE_VALUE_GROUP_FIELD_NAME)
                self.list_field = page.locator('ul[role="tree"] .MuiTreeItem-content').filter(has_text=HUB_PAGE_VALUE_LIST_FIELD_NAME)
                self.nested_field = page.locator('ul[role="tree"] .MuiTreeItem-content').filter(has_text=HUB_PAGE_VALUE_NESTED_FIELD_NAME)
                self.required_checkbox = page.locator('(//div[@class="option"] //span[@class="MuiIconButton-label"])[2] /input')
                self.advanced_section = page.locator('.selection-strategy')
                self.kve_checkbox = page.locator('(//span[@class="MuiIconButton-label"])[3] /input')
                self.qna_checkbox = page.locator('(//span[@class="MuiIconButton-label"])[4] /input')
                self.script_checkbox = page.locator('(//span[@class="MuiIconButton-label"])[5] /input')
                self.qna_input = page.locator("input[name='question']")
                self.verify_button = page.locator('//div[@class="options-wrapper"]/div').filter(has_text="Verify")

            def upload_file(self, document):
                """
                Uploads a pdf file

                :param document: Document name with its type, example 'document.pdf'
                """
                self.file_input.set_input_files("data/" + document + "")

            def click_the_edit_button_on_the_field_label(self, field_name):
                """
                Click the Edit button on the field label

                :param field_name: Name of the field
                """
                self.page.locator(f"//span[contains(@id, 'hubs_edit-data-point_{field_name}')]").click()