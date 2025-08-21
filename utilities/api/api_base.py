from http.client import responses

import requests
from playwright.sync_api import Playwright

from data.constants import PLEXTERA_STAGE_API_URL, OCRG_STAGE_API_URL


def authenticate_with_user(playwright: Playwright, payload):
    api_request_context = playwright.request.new_context(base_url=PLEXTERA_STAGE_API_URL)
    response = api_request_context.post(
        "/api/auth/login",
        data=payload
    )

    return response


def create_new_owner_user(playwright: Playwright, payload, token):
    api_request_context = playwright.request.new_context(base_url=PLEXTERA_STAGE_API_URL)
    response = api_request_context.post(
        "api/account-service/auth-user/create-invite-owner",
        data=payload,
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response


def delete_hub(playwright: Playwright, hub_id, token):
    api_request_context = playwright.request.new_context(base_url=OCRG_STAGE_API_URL)
    response = api_request_context.delete(
        f"/api/hubs/{hub_id}",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response


def delete_web_automation(playwright: Playwright, web_automation_id, token):
    api_request_context = playwright.request.new_context(base_url=OCRG_STAGE_API_URL)
    response = api_request_context.delete(
        f"/api/sbb/automation/{web_automation_id}",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response


def create_new_hub(playwright: Playwright, payload, token):
    api_request_context = playwright.request.new_context(base_url=OCRG_STAGE_API_URL)
    response = api_request_context.post(
        "/api/hubs/create",
        data=payload,
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response


def delete_organization(playwright: Playwright, organization_id, superuser_token):
    """
    
    :param playwright: Playwright Page object representing the browser tab or frame.
    :param organization_id: Organization id
    :param superuser_token: Token of a user with role superuser
    :return: 
    """
    api_request_context = playwright.request.new_context(base_url=PLEXTERA_STAGE_API_URL)
    response = api_request_context.delete(
        f"/api/account-service/admin-console/organizations/{organization_id}",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + superuser_token
        }
    )

    return response

def get_organization_list(playwright: Playwright, token):
    api_request_context = playwright.request.new_context(base_url=PLEXTERA_STAGE_API_URL)
    response = api_request_context.get(
        f"api/account-service/admin-console/organizations?page=0&size=100",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response

def me(playwright: Playwright, token):
    api_request_context = playwright.request.new_context(base_url=PLEXTERA_STAGE_API_URL)
    response = api_request_context.get(
        f"api/account-service/users/me",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response