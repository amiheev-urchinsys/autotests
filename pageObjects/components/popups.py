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



