import time

import pytest
from playwright.sync_api import Playwright, expect, sync_playwright
from data.constants import DOMAIN_STAGE_URL, LOGIN_PAGE_TITLE
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.api.api_base import get_user_token, delete_hub
from utilities.data_processing import get_list_from_file, get_value_by_key_from_list

@pytest.fixture
def context_and_playwright():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        yield context, playwright
        context.close()
        browser.close()


@pytest.mark.hubs
@pytest.mark.outline_based
def test_create_an_outline_based_hub(context_and_playwright):
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
#
# @pytest.mark.hubs
# @pytest.mark.outline_based
# def test_create_group_type_field_in_outline_based_hub(playwright: Playwright):
#     payloads = get_list_from_file("payloads.json", "payloads")
#     authentication_payload = get_value_by_key_from_list(payloads, "authentication")
#     users_list = get_list_from_file("user_credentials.json", "users")
#     support_data = get_value_by_key_from_list(users_list, "support")
#     authentication_payload["email"] = support_data["email"]
#     authentication_payload["password"] = support_data["password"]
#     # Get user token to set the cookies
#     response = get_user_token(playwright, authentication_payload)
#     user_token = response.json()["accessToken"]
#     # Set the browser
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     # Set the cookie with the token
#     context.add_cookies([{
#         "name": "access-token-plextera",  # or "auth_token", depending on your app
#         "value": user_token,
#         "domain": "studio.dev.plextera.com",
#         "path": "/",
#         "httpOnly": False,
#         "secure": True,
#         "sameSite": "Lax"
#     }])
#     page = context.new_page()
#     # Steps
#     page.goto(DOMAIN_STAGE_URL)
#     on_home_page = HomePage(page)
#     on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
#     on_documents_insights_page.hubs_button.click()
#     on_documents_insights_page.hubs_page.create_outline_based_hub()
#     on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
#     on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
#     with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
#         on_documents_insights_page.hubs_page.hub_page.save_button.click()
#     response = resp_info.value
#     assert response.ok
#     # Verification
#     expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
#     # Delete created hub
#     current_url = page.url
#     hub_id = current_url.split("/hubs/")[1]
#     response = delete_hub(playwright, hub_id, user_token)
#     assert response.ok
#     on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
#     on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
#     on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
#     # Verification
#     on_login_page = LoginPage(page)
#     expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)
#
# @pytest.mark.hubs
# @pytest.mark.outline_based
# def test_create_list_type_field_in_outline_based_hub(playwright: Playwright):
#     payloads = get_list_from_file("payloads.json", "payloads")
#     authentication_payload = get_value_by_key_from_list(payloads, "authentication")
#     users_list = get_list_from_file("user_credentials.json", "users")
#     support_data = get_value_by_key_from_list(users_list, "support")
#     authentication_payload["email"] = support_data["email"]
#     authentication_payload["password"] = support_data["password"]
#     # Get user token to set the cookies
#     response = get_user_token(playwright, authentication_payload)
#     user_token = response.json()["accessToken"]
#     # Set the browser
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     # Set the cookie with the token
#     context.add_cookies([{
#         "name": "access-token-plextera",  # or "auth_token", depending on your app
#         "value": user_token,
#         "domain": "studio.dev.plextera.com",
#         "path": "/",
#         "httpOnly": False,
#         "secure": True,
#         "sameSite": "Lax"
#     }])
#     page = context.new_page()
#     # Steps
#     page.goto(DOMAIN_STAGE_URL)
#     on_home_page = HomePage(page)
#     on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
#     on_documents_insights_page.hubs_button.click()
#     on_documents_insights_page.hubs_page.create_outline_based_hub()
#     on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
#     on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
#     with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
#         on_documents_insights_page.hubs_page.hub_page.save_button.click()
#     response = resp_info.value
#     assert response.ok
#     # Verification
#     expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
#     # Delete created hub
#     current_url = page.url
#     hub_id = current_url.split("/hubs/")[1]
#     response = delete_hub(playwright, hub_id, user_token)
#     assert response.ok
#     on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
#     on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
#     on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
#     # Verification
#     on_login_page = LoginPage(page)
#     expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)
#
#
# @pytest.mark.hubs
# @pytest.mark.outline_based
# def test_create_group_type_field_nested_inside_list_type_field_in_outline_based_hub(playwright: Playwright):
#     payloads = get_list_from_file("payloads.json", "payloads")
#     authentication_payload = get_value_by_key_from_list(payloads, "authentication")
#     users_list = get_list_from_file("user_credentials.json", "users")
#     support_data = get_value_by_key_from_list(users_list, "support")
#     authentication_payload["email"] = support_data["email"]
#     authentication_payload["password"] = support_data["password"]
#     # Get user token to set the cookies
#     response = get_user_token(playwright, authentication_payload)
#     user_token = response.json()["accessToken"]
#     # Set the browser
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     # Set the cookie with the token
#     context.add_cookies([{
#         "name": "access-token-plextera",  # or "auth_token", depending on your app
#         "value": user_token,
#         "domain": "studio.dev.plextera.com",
#         "path": "/",
#         "httpOnly": False,
#         "secure": True,
#         "sameSite": "Lax"
#     }])
#     page = context.new_page()
#     # Steps
#     page.goto(DOMAIN_STAGE_URL)
#     on_home_page = HomePage(page)
#     on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
#     on_documents_insights_page.hubs_button.click()
#     on_documents_insights_page.hubs_page.create_outline_based_hub()
#     on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
#     on_documents_insights_page.hubs_page.hub_page.list_radiobutton.click()
#     with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
#         on_documents_insights_page.hubs_page.hub_page.save_button.click()
#     response = resp_info.value
#     assert response.ok
#     # Verification
#     expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
#     on_documents_insights_page.hubs_page.hub_page.nested_add_new_field.click()
#     on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
#     with page.expect_response("**/api/hubs/**/abstract-fields/**/add-sub-field") as resp_info:
#         on_documents_insights_page.hubs_page.hub_page.save_button.click()
#     response = resp_info.value
#     assert response.ok
#     on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
#     expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
#     # Delete created hub
#     current_url = page.url
#     hub_id = current_url.split("/hubs/")[1]
#     response = delete_hub(playwright, hub_id, user_token)
#     assert response.ok
#     on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
#     on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
#     on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
#     # Verification
#     on_login_page = LoginPage(page)
#     expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)
#
#
# @pytest.mark.hubs
# @pytest.mark.outline_based
# def test_create_single_type_field_nested_inside_group_type_field_in_outline_based_hub(playwright: Playwright):
#     payloads = get_list_from_file("payloads.json", "payloads")
#     authentication_payload = get_value_by_key_from_list(payloads, "authentication")
#     users_list = get_list_from_file("user_credentials.json", "users")
#     support_data = get_value_by_key_from_list(users_list, "support")
#     authentication_payload["email"] = support_data["email"]
#     authentication_payload["password"] = support_data["password"]
#     # Get user token to set the cookies
#     response = get_user_token(playwright, authentication_payload)
#     user_token = response.json()["accessToken"]
#     # Set the browser
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     # Set the cookie with the token
#     context.add_cookies([{
#         "name": "access-token-plextera",  # or "auth_token", depending on your app
#         "value": user_token,
#         "domain": "studio.dev.plextera.com",
#         "path": "/",
#         "httpOnly": False,
#         "secure": True,
#         "sameSite": "Lax"
#     }])
#     page = context.new_page()
#     # Steps
#     page.goto(DOMAIN_STAGE_URL)
#     on_home_page = HomePage(page)
#     on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
#     on_documents_insights_page.hubs_button.click()
#     on_documents_insights_page.hubs_page.create_outline_based_hub()
#     on_documents_insights_page.hubs_page.hub_page.add_new_field_button.click()
#     on_documents_insights_page.hubs_page.hub_page.group_radiobutton.click()
#     with page.expect_response("**/api/hubs/**/abstract-fields") as resp_info:
#         on_documents_insights_page.hubs_page.hub_page.save_button.click()
#     response = resp_info.value
#     assert response.ok
#     # Verification
#     expect(on_documents_insights_page.hubs_page.hub_page.list_group_field_label_title).to_be_visible()
#     on_documents_insights_page.hubs_page.hub_page.nested_add_new_field.click()
#     with page.expect_response("**/api/hubs/**/abstract-fields/**/add-sub-field") as resp_info:
#         on_documents_insights_page.hubs_page.hub_page.save_button.click()
#     response = resp_info.value
#     assert response.ok
#     on_documents_insights_page.hubs_page.hub_page.arrow_button.click()
#     expect(on_documents_insights_page.hubs_page.hub_page.nested_group_label).to_be_visible()
#     # Delete created hub
#     current_url = page.url
#     hub_id = current_url.split("/hubs/")[1]
#     response = delete_hub(playwright, hub_id, user_token)
#     assert response.ok
#     on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
#     on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
#     on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
#     # Verification
#     on_login_page = LoginPage(page)
#     expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)
#
#
# @pytest.mark.hubs
# @pytest.mark.value_based
# def test_create_a_value_based_hub(playwright: Playwright):
#     payloads = get_list_from_file("payloads.json", "payloads")
#     authentication_payload = get_value_by_key_from_list(payloads, "authentication")
#     users_list = get_list_from_file("user_credentials.json", "users")
#     support_data = get_value_by_key_from_list(users_list, "support")
#     authentication_payload["email"] = support_data["email"]
#     authentication_payload["password"] = support_data["password"]
#     # Get user token to set the cookies
#     response = get_user_token(playwright, authentication_payload)
#     user_token = response.json()["accessToken"]
#     # Set the browser
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     # Set the cookie with the token
#     context.add_cookies([{
#         "name": "access-token-plextera",  # or "auth_token", depending on your app
#         "value": user_token,
#         "domain": "studio.dev.plextera.com",
#         "path": "/",
#         "httpOnly": False,
#         "secure": True,
#         "sameSite": "Lax"
#     }])
#     page = context.new_page()
#     # Steps
#     page.goto(DOMAIN_STAGE_URL)
#     on_home_page = HomePage(page)
#     on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
#     on_documents_insights_page.hubs_button.click()
#     on_documents_insights_page.hubs_page.create_value_based_hub()
#     # Verification
#     expect(on_documents_insights_page.hubs_page.hub_page.upload_documents_button).to_be_visible()
#     expect(on_documents_insights_page.hubs_page.hub_page.gear_button).to_be_visible()
#     expect(on_documents_insights_page.hubs_page.hub_page.edit_hub_name).to_be_visible()
#     expect(on_documents_insights_page.hubs_page.hub_page.add_data_points_button).to_be_visible()
#     expect(on_documents_insights_page.hubs_page.hub_page.import_data_points_in_json_format_button).to_be_visible()
#     # expect(on_documents_insights_page.hubs_page.hub_page.data_points_tab).to_be_visible()
#     # expect(on_documents_insights_page.hubs_page.hub_page.dictionary_tab).to_be_visible()
#     # expect(on_documents_insights_page.hubs_page.hub_page.classification_tab).to_be_visible()
#     # Delete created hub
#     current_url = page.url
#     hub_id = current_url.split("/hubs/")[1]
#     response = delete_hub(playwright, hub_id, user_token)
#     assert response.ok
#     on_documents_insights_page.sidebar.sidebar_bottom_section.hover()
#     on_documents_insights_page.sidebar.personal_cabinet_dropdown_menu.click()
#     on_documents_insights_page.sidebar.personal_cabinet_log_out_point.click()
#     # Verification
#     on_login_page = LoginPage(page)
#     expect(on_login_page.page_title).to_contain_text(LOGIN_PAGE_TITLE)


# @pytest.mark.hubs
# @pytest.mark.value_based
# def test_create_single_type_field_value_based_hub(playwright: Playwright):
#     payloads = get_list_from_file("payloads.json", "payloads")
#     authentication_payload = get_value_by_key_from_list(payloads, "authentication")
#     users_list = get_list_from_file("user_credentials.json", "users")
#     support_data = get_value_by_key_from_list(users_list, "support")
#     authentication_payload["email"] = support_data["email"]
#     authentication_payload["password"] = support_data["password"]
#     # Get user token to set the cookies
#     response = get_user_token(playwright, authentication_payload)
#     user_token = response.json()["accessToken"]
#     # Set the browser
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     # Set the cookie with the token
#     context.add_cookies([{
#         "name": "access-token-plextera",  # or "auth_token", depending on your app
#         "value": user_token,
#         "domain": "studio.dev.plextera.com",
#         "path": "/",
#         "httpOnly": False,
#         "secure": True,
#         "sameSite": "Lax"
#     }])
#     page = context.new_page()
#     # Steps
#     page.goto(DOMAIN_STAGE_URL)
#     on_home_page = HomePage(page)
#     on_documents_insights_page = on_home_page.sidebar.navigate_to_documents_insights_page()
#     on_documents_insights_page.hubs_button.click()
#     on_documents_insights_page.hubs_page.create_value_based_hub()
#     # Delete created hub
#     current_url = page.url
#     hub_id = current_url.split("/hubs/")[1]
#     response = delete_hub(playwright, hub_id, user_token)
#     assert response.ok