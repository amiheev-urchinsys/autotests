from http.client import responses

import requests
from playwright.sync_api import Playwright

stage = "https://api.dev.plextera.com"
stage_ocrg = "https://ocrf.ocrgateway.com"


def get_user_token(playwright: Playwright, payload):
    api_request_context = playwright.request.new_context(base_url=stage)
    response = api_request_context.post(
        "/api/auth/login",
        data=payload
    )

    return response


def create_new_owner_user(playwright: Playwright, payload, token):
    api_request_context = playwright.request.new_context(base_url=stage)
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
    api_request_context = playwright.request.new_context(base_url=stage_ocrg)
    response = api_request_context.delete(
        f"/api/hubs/{hub_id}",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response

def delete_web_automation(playwright: Playwright, web_automation_id, token):
    api_request_context = playwright.request.new_context(base_url=stage_ocrg)
    response = api_request_context.delete(
        f"/api/sbb/automation/{web_automation_id}",
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response

def create_new_hub(playwright: Playwright, payload, token):
    api_request_context = playwright.request.new_context(base_url=stage_ocrg)
    response = api_request_context.post(
        "/api/hubs/create",
        data=payload,
        headers={
            "Context-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response