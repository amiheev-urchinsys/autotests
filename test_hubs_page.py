import time

import pytest
from playwright.sync_api import Playwright, expect, sync_playwright
from data.constants import DOMAIN_STAGE_URL, LOGIN_PAGE_TITLE
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.api.api_base import get_user_token, delete_hub
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_an_outline_based_hub(context_and_playwright):
    """
    Verify that a user can successfully create an outline based hub

    Steps:
    - Load user credentials and payload from the JSON file.
    - Send login request and set cookie
    - Open home page and navigate to the 'Documents Insights' page
    - Open, fill in and send the 'Create a hub' form

    Expected:
    - Elements as 'add new field button', 'drag and drop', 'browse files', 'edit hub name', 'settings menu' should be
    visible

    Post-conditions:
    - Get hub id and send 'Delete' request
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
    # Load data
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
    on_documents_insights_page.hubs_page.create_outline_based_hub()
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.add_new_field_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.drag_and_drop_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.browse_files_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    # Logout
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.single_field_label_title).to_be_visible()
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)

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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.nested_add_new_field.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields/**/add-sub-field") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
    expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_outline_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
    on_documents_insights_page.hubs_page.hub_page.nested_add_new_field.click()
    with page.expect_response("**/api/hubs/**/abstract-fields/**/add-sub-field") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
    expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    print(hub_id)
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


@pytest.mark.hubs
@pytest.mark.value_based
def test_create_a_value_based_hub(context_and_playwright):
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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_value_based_hub()
    # Verification
    expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
    expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
    # Delete created hub
    time.sleep(3)
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok
    on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
    on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
    # Verification
    on_login_page = LoginPage(page)
    expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


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
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill("testing field 1")
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    assert response.ok
    time.sleep(3)
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
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
    - Open the 'Create a new field' form and send it

    Expected:
    - A Group-type field block is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill("testing field 1")
    on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/**?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    response2 = resp2_info.value
    assert response.ok, response2.ok
    time.sleep(3)
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
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
    - Open the 'Create a new field' form and send it

    Expected:
    - A List-type field block is displayed

    Post-conditions:
    - Get hub id and send 'Delete' request
    - Log out user from the project
    """
    context, playwright = context_and_playwright
    page = context.new_page()
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
    on_documents_insights_page.hubs_page.create_value_based_hub()
    on_documents_insights_page.hubs_page.hub_page.add_data_points_button.click()
    on_documents_insights_page.hubs_page.hub_page.field_name_input.fill("testing field 1")
    on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
    with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info, \
            page.expect_response("**/api/hubs/**?include=short_outline") as resp2_info:
        on_documents_insights_page.hubs_page.hub_page.save_button.click()
    response = resp_info.value
    response2 = resp2_info.value
    assert response.ok, response2.ok
    time.sleep(3)
    # Delete created hub
    current_url = page.url
    hub_id = current_url.split("/hubs/")[1]
    response = delete_hub(playwright, hub_id, user_token)
    assert response.ok