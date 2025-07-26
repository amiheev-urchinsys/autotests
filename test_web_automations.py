from operator import truediv

import pytest
from playwright.sync_api import expect
from pageObjects.homePage import HomePage
from utilities.api.api_base import get_user_token, delete_hub, delete_web_automation
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list
from data.constants import DOMAIN_STAGE_URL

@pytest.mark.web_automations
def test_create_a_web_automation_required_fields_only(context_and_playwright):
    """
    Verify that a user can successfully create a web automation only required fields populated

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Web Automations' page
    - Create web automation

    Expected:
    - Created web automation is in the list on the Web Automations page

    Post-conditions:
    - Get web automation id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
    # payloads = get_list_from_file("payloads.json", "payloads")
    # authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    # users_list = get_list_from_file("user_credentials.json", "users")
    # support_data = get_value_by_key_from_list(users_list, "support")
    # authentication_payload["email"] = support_data["email"]
    # authentication_payload["password"] = support_data["password"]
    authentication_payload = {
        "email": "amiheev@urchinsys.com",
        "password": "4h@TU3Wa"
    }
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set token in cookies
    context.add_cookies([{
        "name": "access-token-plextera",
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Start test
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_web_automations_page= on_home_page.sidebar.navigate_to_web_automations_page()
    on_web_automations_page.create_button.click()
    on_web_automations_page.popups.create_automation_name_input.fill("create_web_automation_test")
    with page.expect_response("**/api/sbb/automation") as resp_info:
        on_web_automations_page.popups.save_button.click()
    web_automation_id = resp_info.value.json()["id"]
    assert resp_info.value.ok
    with page.expect_response(f"**/api/sbb/automation/{web_automation_id}") as resp_info:
        on_web_automations_page.web_automation_page.save_button.click()
    assert resp_info.value.ok
    # Delete web automation
    response = delete_web_automation(playwright, web_automation_id, user_token)
    assert response.ok

@pytest.mark.web_automations
def test_create_a_web_automation_using_import(context_and_playwright):
    """
    Verify that a user can successfully create a web automation using file import

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Web Automations' page
    - Create web automation using file import

    Expected:
    - Created web automation is in the list on the Web Automations page

    Post-conditions:
    - Get web automation id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
    # payloads = get_list_from_file("payloads.json", "payloads")
    # authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    # users_list = get_list_from_file("user_credentials.json", "users")
    # support_data = get_value_by_key_from_list(users_list, "support")
    # authentication_payload["email"] = support_data["email"]
    # authentication_payload["password"] = support_data["password"]
    authentication_payload = {
        "email": "amiheev@urchinsys.com",
        "password": "4h@TU3Wa"
    }
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set token in cookies
    context.add_cookies([{
        "name": "access-token-plextera",
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Start test
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_web_automations_page = on_home_page.sidebar.navigate_to_web_automations_page()
    on_web_automations_page.import_button.click()
    on_web_automations_page.upload_file("automation_for_import.json")
    expect(on_web_automations_page.popups.import_automation_remove_file).to_be_visible()
    with page.expect_response("**/api/sbb/automation/import") as resp_info, \
        page.expect_response("**/api/sbb/automation/list") as list_info:
        on_web_automations_page.popups.import_automation_import_button.click()
    web_automation_id = resp_info.value.json()["id"]
    assert resp_info.value.ok
    assert list_info.value.ok
    web_automation_list = list_info.value.json()["content"]
    status = False
    for item in web_automation_list:
        if item["id"] == web_automation_id:
            status = True
            break
    assert status == True

    # Delete web automation
    response = delete_web_automation(playwright, web_automation_id, user_token)
    assert response.ok

