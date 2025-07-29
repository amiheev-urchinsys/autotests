import time

import pytest
from playwright.sync_api import expect
from data.constants import DOMAIN_STAGE_URL, HUB_PAGE_OUTLINE_TEMPLATE_NAME, HUB_PAGE_VALUE_FIELDS_TITLE_TEXT, \
    HUBS_PAGE_RENAME_POPUP_TITLE, HUBS_PAGE_TAGS_POPUP_TITLE
from pageObjects.homePage import HomePage
from utilities.api.api_base import get_user_token, delete_hub
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_an_outline_based_hub_only_required_fields(context_and_playwright):
    """
    Verify that a user can successfully create an outline based only required fields populated

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to hubs page

    Expected:
    - Outline hub card is displayed on the Hubs page

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
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
    # Continue as before
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    outline_hub_id, _ = on_documents_insights_page.hubs_page.create_outline_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_an_outline_based_hub_all_fields(context_and_playwright):
    """
    Verify that a user can successfully create an outline based hub with all fields populated

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to hubs page

    Expected:
    - Outline hub card is displayed on the Hubs page

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
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
    # Continue as before
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    outline_hub_id, _ = on_documents_insights_page.hubs_page.create_outline_based_hub(True)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_card_description).to_have_text("description")
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok

@pytest.mark.hubs
@pytest.mark.outline_based
def test_disable_an_outline_based_hub_only_required_fields(context_and_playwright):
    """
    Verify that a user can successfully disable an outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to hubs page
    - Click the switch on the hub card

    Expected:
    - Switch is disabled on the hub card

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
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
    # Continue as before
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    outline_hub_id, _ = on_documents_insights_page.hubs_page.create_outline_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    on_documents_insights_page.hubs_page.hub_card_switch.click()
    with page.expect_response("**/api/hubs/" + outline_hub_id + "") as resp_info:
        on_documents_insights_page.hubs_page.popups.disable_button.click()
    assert resp_info.value.ok
    # Verification

    # Delete hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok



@pytest.mark.hubs
@pytest.mark.outline_based
def test_delete_outline_hub_using_delete_point_from_settings_menu(context_and_playwright):
    """
        Verify that a user can successfully delete an outline based hub from hubs page

        Steps:
        - Load user credentials and payload from the JSON file.
        - Send login request and set cookie
        - Open home page and navigate to the 'Documents Insights' page
        - Open, fill in and send the 'Create a hub' form
        - Navigate to the Hubs page
        - Open settings menu on the hubs card and delete hub

        Expected:
        - No hub card is displayed
        """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
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
    # Continue as before
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    outline_hub_id, _ = on_documents_insights_page.hubs_page.create_outline_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_delete_point.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"") as resp_info:
        on_documents_insights_page.hubs_page.popups.delete_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).not_to_be_visible()
    on_documents_insights_page.hubs_page.hub_card_switch.click()
    on_documents_insights_page.hubs_page.popups.delete_button.click()


@pytest.mark.hubs
@pytest.mark.outline_based
def test_open_view_details_popup_of_the_outline_hub(context_and_playwright):
    """
    Verify that a user can successfully open the View Details popup using the settings menu of the outline hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to hubs page
    - Open settings menu and click the View Details point

    Expected:
    - The View Details popup is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
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
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    outline_hub_id, _ = on_documents_insights_page.hubs_page.create_outline_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    # Navigate to Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    # Open the View Detail popup
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_view_details_point.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.popups.view_details_content_section).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_rename_an_outline_hub(context_and_playwright):
    """
    Verify that a user can successfully rename an outline hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to hubs page
    - Open the Rename popup using settings menu from the outline hub card
    - Fill in the input field and send the form

    Expected:
    - Updated outline hub card is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
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
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    outline_hub_id, _ = on_documents_insights_page.hubs_page.create_outline_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    # Navigate to Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    # Open the Rename popup
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_rename_point.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.popups.body).to_be_visible()
    expect(on_documents_insights_page.hubs_page.popups.body).to_contain_text(HUBS_PAGE_RENAME_POPUP_TITLE)
    # Update an outline hub title
    on_documents_insights_page.hubs_page.popups.rename_input.fill("update outline hub")
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"") as resp_info:
        on_documents_insights_page.hubs_page.popups.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card_title).to_have_text("update outline hub")
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_a_value_based_hub_only_required_fields(context_and_playwright):
    """
    Verify that a user can successfully create a value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form

    Expected:
    - Elements as 'add new field button', 'drag and drop', 'browse files', 'edit hub name', 'settings menu' and three tabs should be
    visible

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Navigate to Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_a_value_based_hub_only_all_fields_key_value_extractor(context_and_playwright):
    """
    Verify that a user can successfully create a value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form

    Expected:
    - Elements as 'add new field button', 'drag and drop', 'browse files', 'edit hub name', 'settings menu' and three tabs should be
    visible

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub(True, False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Navigate to Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_card_description).to_have_text("description")
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_a_value_based_hub_only_all_fields_label_based_extractor(context_and_playwright):
    """
    Verify that a user can successfully create a value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form

    Expected:
    - Elements as 'add new field button', 'drag and drop', 'browse files', 'edit hub name', 'settings menu' and three tabs should be
    visible

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub(True, True)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).not_to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Navigate to Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_card_description).to_have_text("description")
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok





@pytest.mark.hubs
@pytest.mark.value_based
def test_delete_a_value_based_hub_using_delete_point_from_settings_menu(context_and_playwright):
    """
    Verify that a user can successfully delete a value based hub from hubs page

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to the Hubs page
    - Open settings menu on the hubs card and delete hub

    Expected:
    - No hub card is displayed
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_delete_point.click()
    time.sleep(3)
    with page.expect_response("**/api/hubs/"+ value_hub_id +"") as resp_info:
        on_documents_insights_page.hubs_page.popups.delete_button.click()
    assert resp_info.value.ok
    expect(on_documents_insights_page.hubs_page.hub_card).not_to_be_visible()


@pytest.mark.hubs
@pytest.mark.value_based
def test_rename_a_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully rename a value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to the Hubs page
    - Open the Rename popup using setting menu of the value based hub card
    - Fill in the input and send the form

    Expected:
    - Updated value hub card is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Navigate to the Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    # Open the Rename popup
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_rename_point.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.popups.body).to_be_visible()
    expect(on_documents_insights_page.hubs_page.popups.body).to_contain_text(HUBS_PAGE_RENAME_POPUP_TITLE)
    # Update an outline hub title
    on_documents_insights_page.hubs_page.popups.rename_input.fill("update outline hub")
    with page.expect_response("**/api/hubs/" + value_hub_id + "") as resp_info:
        on_documents_insights_page.hubs_page.popups.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card_title).to_have_text("update outline hub")
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_add_tag_to_a_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully add a tag to a value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to the Hubs page
    - Open the Tags for hub popup using setting menu of the value based hub card
    - Fill in the Enter Key, Enter Value inputs and send the form
    - Open the Tags for hub popup using setting menu of the value based hub card

    Expected:
    - Entered tags values are displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, value_hub_name = on_documents_insights_page.hubs_page.create_value_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Navigate to the Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    # Open the Tags for hub popup
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_tags_point.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.popups.body).to_be_visible()
    expect(on_documents_insights_page.hubs_page.popups.body).to_contain_text(HUBS_PAGE_TAGS_POPUP_TITLE + " " +value_hub_name)
    # Update an outline hub title
    on_documents_insights_page.hubs_page.popups.tags_for_hub_key_input.fill("key")
    on_documents_insights_page.hubs_page.popups.tags_for_hub_value_input.fill("value")
    with page.expect_response("**/api/outlines/**/meta-attributes") as resp_info:
        on_documents_insights_page.hubs_page.popups.save_button.click()
    assert resp_info.value.ok
    # Open the Tags for hub popup
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_tags_point.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.popups.tags_for_hub_key_input).to_have_value("key")
    expect(on_documents_insights_page.hubs_page.popups.tags_for_hub_value_input).to_have_value("value")
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_open_view_details_popup_of_a_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully open View Details popup of a value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Navigate to Hubs page
    - Open the View Details popup using settings menu of a value based hub card

    Expected:
    - The View Details popup is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test_smth data from files
    payloads = get_list_from_file("payloads.json", "payloads")
    authentication_payload = get_value_by_key_from_list(payloads, "authentication")
    users_list = get_list_from_file("user_credentials.json", "users")
    support_data = get_value_by_key_from_list(users_list, "support")
    authentication_payload["email"] = support_data["email"]
    authentication_payload["password"] = support_data["password"]
    # Get user token to set the cookies
    response = get_user_token(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    # Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    # Steps
    page.goto(DOMAIN_STAGE_URL)
    on_home_page = HomePage(page)
    on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
    on_documents_insights_page.hubs_button.click()
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub(False)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Navigate to Hubs page
    with page.expect_response("**/api/hubs/page?sortBy=name") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.navigate_to_hubs_page_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_card).to_be_visible()
    # Open the View Detail popup
    on_documents_insights_page.hubs_page.hub_card_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_card_meatball_menu_view_details_point.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.popups.view_details_content_section).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok