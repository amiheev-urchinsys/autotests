from playwright.sync_api import Page


class Popups:
    """
    Represents and manages all reusable popup components within the application UI.

    This class provides access to common popup elements and actions
    that can appear across different page
    """
    def __init__(self, page: Page):
        """
        Initializes the popups object with web element locators.
        :param page: Playwright Page object representing the browser tab or frame.
        """
        self.page = page
        # Buttons
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.delete_button = page.get_by_role("button", name="Delete")
        self.disable_button = page.get_by_role("button", name="Disable")
        self.save_button = page.get_by_role("button", name="Save")
        self.next_button = page.get_by_role("button", name="Next")
        self.tags_for_hub_add_another_tag_button = page.get_by_role("button", name="+ Add another tag")
        self.import_automation_import_button = page.get_by_role("button", name="Import")
        self.import_automation_remove_file = page.get_by_role("button", name=" Remove file ")
        self.invite_button = page.get_by_role("button", name="Invite")
        # Inputs
        self.rename_input = page.locator('input[placeholder="Hub name"]')
        self.tags_for_hub_key_input = page.locator(".key")
        self.tags_for_hub_value_input = page.locator(".value")
        self.create_hub_description_input = page.get_by_role("textbox", name="Enter description")
        self.create_automation_name_input = page.locator("//input[contains(@class, 'this-input')]")
        self.invite_company_user_email_address_input = page.locator('[name="email"]')
        self.invite_company_user_role_selector = page.locator(".MuiSelect-select:has(.placeholder)")
        self.invite_company_user_role_selector_list_administrator_point = page.locator("#\:r2ec\: li").filter(has_text="Administrator")
        self.invite_company_user_role_selector_list_user_point = page.locator("#\:r2ec\: li").filter(has_text="User")
        # Checkboxes
        self.create_hub_additional_options_checkbox = page.locator('input[type="checkbox"]')
        # Radiobuttons
        self.create_hub_key_value_extractor_radiobutton = page.locator(
            "//label[contains(@class, 'radio-button-label')]").filter(has_text="Key-value Extractor")
        self.create_hub_label_based_extractor_radiobutton = page.locator(
            "//label[contains(@class, 'radio-button-label')]").filter(has_text="Label-based Extractor")
        # Lists
        self.verification_settings_list_item = page.locator(
            "//div[contains(@class, 'sub-item')]//label[contains(@class, 'radio-button-label')]")
        self.verification_settings_number_format_list_item = page.locator(
            "//div[contains(@class, 'sub-item')]//label[contains(@class, 'radio-button-label')]").filter(
            has_text="Number format")
        # Cards
        self.create_hub_outline_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(1)')
        self.create_hub_value_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(2)')
        # Elements
        self.body = page.locator('div[tabindex="-1"]')
        self.view_details_content_section = page.locator("#view-details")








