from playwright.sync_api import Playwright


def get_user_token(playwright: Playwright):
    api_request_context = playwright.request.new_context(base_url="https://api.dev.plextera.com")
    response = api_request_context.post(
        "/api/auth/login",
        data={
            "email": "amiheev@urchinsys.com",
            "password": "4h@TU3Wa"
        }
    )

    return response
