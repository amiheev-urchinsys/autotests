from playwright.sync_api import Page


class Popups:
    def __init__(self, page: Page):
        self.page = page
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.delete_button = page.get_by_role("button", name="Delete")
        self.disable_button = page.get_by_role("button", name="Disable")
        self.view_details_content_section = page.locator("#view-details")
        self.body = page.locator('div[tabindex="-1"]')
        self.rename_input = page.locator('input[placeholder="Hub name"]')
        self.save_button = page.get_by_role("button", name="Save")
        self.tags_for_hub_key_input = page.locator(".key")
        self.tags_for_hub_value_input = page.locator(".value")
        self.tags_for_hub_add_another_tag_button = page.get_by_role("button", name="+ Add another tag")
        self.verification_settings_list_item = page.locator("//div[contains(@class, 'sub-item')]//label[contains(@class, 'radio-button-label')]")
        self.verification_settings_number_format_list_item = page.locator("//div[contains(@class, 'sub-item')]//label[contains(@class, 'radio-button-label')]").filter(has_text="Number format")
        self.create_hub_outline_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(1)')
        self.create_hub_value_based_type_card = page.locator('div[class="menu"] div[class="menu-item"]:nth-child(2)')
        self.next_button = page.get_by_role("button", name="Next")
        self.create_hub_description_input = page.get_by_role("textbox", name="Enter description")
        self.create_hub_additional_options_checkbox = page.locator('input[type="checkbox"]')
        self.create_hub_key_value_extractor_radiobutton = page.locator("//label[contains(@class, 'radio-button-label')]").filter(has_text="Key-value Extractor")
        self.create_hub_label_based_extractor_radiobutton = page.locator("//label[contains(@class, 'radio-button-label')]").filter(has_text="Label-based Extractor")
