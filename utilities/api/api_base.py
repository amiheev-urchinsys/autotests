from playwright.sync_api import Playwright

stage = "https://api.dev.plextera.com"


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
