import time

import pytest
from playwright.sync_api import expect
from data.constants import DOMAIN_STAGE_URL, HUB_PAGE_VALUE_FIELDS_TITLE_TEXT, HUB_PAGE_VALUE_SINGLE_FIELD_NAME, \
    HUB_PAGE_VALUE_GROUP_FIELD_NAME, HUB_PAGE_VALUE_LIST_FIELD_NAME, HUB_PAGE_VALUE_NESTED_FIELD_NAME
from pageObjects.homePage import HomePage
from utilities.api.api_base import get_user_token, delete_hub
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_single_type_field_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form and send it

    Expected:
    - A Single-type field block is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    expect(on_documents_insights_page.hubs_page.hub_page.added_field).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.single_field).to_be_visible()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_group_type_field_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Group-type field for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form select Group type, enter name and send it

    Expected:
    - A Group-type field block is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    # Create group-type field
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_GROUP_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/"+ value_hub_id +"?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    assert resp2_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    expect(on_documents_insights_page.hubs_page.hub_page.added_field).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.group_field).to_be_visible()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_list_type_field_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a List-type field for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form select List type, enter name and send it

    Expected:
    - A List-type field block is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_LIST_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/"+ value_hub_id +"?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    assert resp2_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    expect(on_documents_insights_page.hubs_page.hub_page.added_field).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.list_field).to_be_visible()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_group_type_field_nested_inside_list_type_field_in_value_based_hub(context_and_playwright):
    """
     Verify that a user can successfully create a Group-type field nested inside the List-type field for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form select List type, enter name and send it
    - Click + on the list-type field and create a group-type field
    - Click arrow button to reveal the nested group-type field

    Expected:
    - A List-type field with nested Group-type filed is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_LIST_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/"+ value_hub_id +"?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    assert resp2_info.value.ok
    field_id = resp_info.value.json()["id"]
    on_documents_insights_page.hubs_page.hub_page.nested_value_add_new_field.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_NESTED_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields/"+ field_id +"/add-sub-field") as resp_info, \
            page.expect_response("**/api/hubs/"+ value_hub_id +"?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    assert resp2_info.value.ok
    # Verification
    on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
    # expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.nested_field).to_be_visible()
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_delete_single_type_field_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully delete a Single-type field for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form and send it
    - Click the Delete button on the Single-type field

    Expected:
    - A Single-type field block is not displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    on_documents_insights_page.hubs_page.hub_page.delete_single_type_field_icon.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields/**") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_delete_group_type_field_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully delete a Group-type field on the value based hub page

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form select Group type, enter name and send it
    - Click the Delete button on the Group-type field

    Expected:
    - A Group-type field block is not displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_GROUP_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/"+ value_hub_id +"?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    assert resp2_info.value.ok
    field_id = response.json()["id"]
    on_documents_insights_page.hubs_page.hub_page.delete_group_type_field_icon.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields/"+ field_id +"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_delete_list_type_field_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully delete a List-type field for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form select List type, enter name and send it
    - Click the Delete button on the Group-type field

    Expected:
    - A List-type field block is not displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_LIST_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/"+ value_hub_id +"?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    assert resp2_info.value.ok
    field_id = response.json()["id"]
    on_documents_insights_page.hubs_page.hub_page.delete_group_type_field_icon.click()
    with page.expect_response("**/api/hubs/"+ value_hub_id +"/abstract-fields/"+ field_id +"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    time.sleep(3)
    # Delete created hub
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_check_uncheck_searchable_checkbox_in_create_single_type_field_form_on_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field with searchable checkbox active for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form
    - Select Searchable checkbox and send the form
    - Click Edit button on the created field

    Expected:
    - Searchable checkbox is checked

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.searchable_checkbox.click()
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.searchable_checkbox).to_be_checked()
    # Uncheck searchable checkbox
    on_documents_insights_page.hubs_page.hub_page.searchable_checkbox.click()
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields/"+ field_id +"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(
        HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.searchable_checkbox).not_to_be_checked()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_check_uncheck_required_checkbox_in_create_single_type_field_form_on_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field with searchable checkbox active for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form
    - Select Searchable checkbox and send the form
    - Click Edit button on the created field

    Expected:
    - Searchable checkbox is checked

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.required_checkbox.click()
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.required_checkbox).to_be_checked()
    # Uncheck searchable checkbox
    on_documents_insights_page.hubs_page.hub_page.required_checkbox.click()
    with page.expect_response("**/api/hubs/" + value_hub_id + "/abstract-fields/" + field_id + "") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(
        HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.required_checkbox).not_to_be_checked()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.value_based
def test_check_uncheck_qna_checkbox_in_advanced_section_when_create_single_type_field_form_on_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field with searchable checkbox active for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form
    - Select Searchable checkbox and send the form
    - Click Edit button on the created field

    Expected:
    - Searchable checkbox is checked

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.advanced_section.click()
    on_documents_insights_page.hubs_page.hub_page.qna_checkbox.click()
    on_documents_insights_page.hubs_page.hub_page.qna_input.fill("get only date")
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.advanced_section.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.qna_checkbox).to_be_checked()
    # Uncheck qna checkbox
    on_documents_insights_page.hubs_page.hub_page.qna_checkbox.click()
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields/" + field_id + "") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.advanced_section.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.qna_checkbox).not_to_be_checked()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok

# UPLOAD NOT WORKING
@pytest.mark.hubs
@pytest.mark.value_based
def test_check_uncheck_script_checkbox_in_advanced_section_when_create_single_type_field_form_on_value_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field with searchable checkbox active for the value based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form
    - Select Searchable checkbox and send the form
    - Click Edit button on the created field

    Expected:
    - Searchable checkbox is checked

    Post-conditions:
    - Get hub id and send 'Delete' request
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Get test data from files
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
    value_hub_id, _ = on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.advanced_section.click()
    on_documents_insights_page.hubs_page.hub_page.script_checkbox.click()
    time.sleep(2)
    on_documents_insights_page.hubs_page.hub_page.upload_file("script_test_file.py")
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_data_points_title_text).to_have_text(HUB_PAGE_VALUE_FIELDS_TITLE_TEXT)
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.advanced_section.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.script_checkbox).to_be_checked()
    # Uncheck script checkbox
    on_documents_insights_page.hubs_page.hub_page.script_checkbox.click()
    on_documents_insights_page.hubs_page.hub_page.kve_checkbox.click()
    with page.expect_response("**/api/hubs/"+value_hub_id+"/abstract-fields/" + field_id + "") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Click the Edit button
    on_documents_insights_page.hubs_page.hub_page.click_the_edit_button_on_the_field_label(
        HUB_PAGE_VALUE_SINGLE_FIELD_NAME)
    on_documents_insights_page.hubs_page.hub_page.advanced_section.click()
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.script_checkbox).not_to_be_checked()
    # Delete created hub
    time.sleep(3)
    response = delete_hub(playwright, value_hub_id, user_token)
    assert response.ok