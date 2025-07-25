import time

import pytest
from playwright.sync_api import expect
from data.constants import DOMAIN_STAGE_URL, HUB_PAGE_OUTLINE_TEMPLATE_NAME
from pageObjects.homePage import HomePage
from utilities.api.api_base import get_user_token, delete_hub
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list

@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_single_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field for the outline based hub

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).not_to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.fields_list_text_title).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.single_field_label_title).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_group_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Group-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form, select Group type and send it

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).not_to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.fields_list_text_title).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok

@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_list_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a List-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form, select List type and send it

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).not_to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.fields_list_text_title).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_group_type_field_nested_inside_list_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Group-type field nested inside the List-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form, select List type and send it
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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.nested_add_new_field.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields/"+ field_id +"/add-sub-field") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).not_to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.fields_list_text_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
    expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_single_type_field_nested_inside_group_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create a Single-type field nested inside the Group-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form, select Group type and send it
    - Click + on the list-type field and create a single-type field
    - Click arrow button to reveal the nested single-type field

    Expected:
    - A Group-type field with nested Single-type filed is displayed

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.nested_add_new_field.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields/"+ field_id +"/add-sub-field") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).not_to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.fields_list_text_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
    expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_delete_single_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully delete a Single-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form and send it
    - Click the Delete button on the Single-type block

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.single_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.delete_single_type_field_icon_outline.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields/"+ field_id +"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.single_field_label_title).not_to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_delete_group_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully delete a Group-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form, select Group type and send it
    - Click the Delete button on the Group-type block

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.delete_group_type_field_icon.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields/"+ field_id +"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).not_to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_delete_list_type_field_in_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully delete a List-type field for the outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Open the 'Create a new field' form, select List type and send it
    - Click the Delete button on the Group-type block

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    field_id = resp_info.value.json()["id"]
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.delete_group_type_field_icon.click()
    with page.expect_response("**/api/hubs/"+ outline_hub_id +"/abstract-fields/"+ field_id +"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.no_fields_text).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).not_to_be_visible()
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_outline_document_template(context_and_playwright):
    """
    Verify that a user can successfully create outline document template

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Upload file

    Expected:
    - Outline template card is displayed

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    # Upload document
    with page.expect_response("**/api/outlines") as resp_info, \
            page.expect_response("**/api/hubs/smart/"+ outline_hub_id +"/add-outline") as resp2_info, \
            page.expect_response("**/api/hubs/"+ outline_hub_id +"?include=short_outline,channels") as resp3_info:
        on_documents_insights_page.hubs_page.hub_page.upload_file("outline_document.pdf")
    assert resp_info.value.ok
    assert resp2_info.value.ok
    assert resp3_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_name).to_have_text(HUB_PAGE_OUTLINE_TEMPLATE_NAME)
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_switch).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_meatball_menu).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_footer).to_be_visible()
    time.sleep(5)
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_rename_outline_template_card(context_and_playwright):
    """
    Verify that a user can successfully rename outline document template

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Upload file
    - Open the Rename popup and update the name

    Expected:
    - Updated title of outline template card is displayed

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    # Upload document
    with page.expect_response("**/api/outlines") as resp_info, \
            page.expect_response("**/api/hubs/smart/"+outline_hub_id+"/add-outline") as add_outline_info, \
            page.expect_response("**/api/hubs/"+outline_hub_id+"?include=short_outline,channels") as resp3_info:
        on_documents_insights_page.hubs_page.hub_page.upload_file("outline_document.pdf")
    assert resp_info.value.ok
    assert add_outline_info.value.ok
    assert resp3_info.value.ok
    outline_hub_outline_template_id = add_outline_info.value.json()["outlines"][0]["id"]
    # Update outline template name
    on_documents_insights_page.hubs_page.hub_page.outline_template_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_page.outline_template_meatball_menu_rename_point.click()
    on_documents_insights_page.hubs_page.hub_page.rename_popup_input.fill("Update")
    with page.expect_response("**/api/outlines/"+outline_hub_outline_template_id+"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_name).to_have_text("Update")
    time.sleep(5)
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok


@pytest.mark.hubs
@pytest.mark.outline_based
def test_delete_outline_template_card(context_and_playwright):
    """
    Verify that a user can successfully delete outline document template

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form
    - Upload file
    - Open the settings menu and delete the outline template card

    Expected:
    - Empty outline templates list is displayed

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
    outline_hub_id = on_documents_insights_page.hubs_page.create_outline_based_hub()
    # Upload document
    with page.expect_response("**/api/outlines") as resp_info, \
            page.expect_response("**/api/hubs/smart/"+outline_hub_id+"/add-outline") as add_outline_info, \
            page.expect_response("**/api/hubs/"+outline_hub_id+"?include=short_outline,channels") as resp3_info:
        on_documents_insights_page.hubs_page.hub_page.upload_file("outline_document.pdf")
    assert resp_info.value.ok
    assert add_outline_info.value.ok
    assert resp3_info.value.ok
    outline_hub_outline_template_id = add_outline_info.value.json()["outlines"][0]["id"]
    # Update outline template name
    on_documents_insights_page.hubs_page.hub_page.outline_template_meatball_menu.click()
    on_documents_insights_page.hubs_page.hub_page.outline_template_meatball_menu_delete_point.click()
    with page.expect_response("**/api/outlines/"+outline_hub_outline_template_id+"") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.delete_button.click()
    assert resp_info.value.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.outline_template_card).not_to_be_visible()
    time.sleep(5)
    # Delete created hub
    response = delete_hub(playwright, outline_hub_id, user_token)
    assert response.ok
