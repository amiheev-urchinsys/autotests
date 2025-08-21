from utilities.api.api_base import authenticate_with_user
from utilities.data_processing import get_key_value_from_file

def build_auth_request_payload(user_profile):
    """
    This function creates a payload that will be used in the authenticate request

    :param user_profile: A key from a user_credentials.json file
    :return: created payload for authenticate request
    """
    authentication_payload = get_key_value_from_file("payloads.json", "authentication_payload")
    user_data = get_key_value_from_file("user_credentials.json", user_profile)
    authentication_payload["email"] = user_data["email"]
    authentication_payload["password"] = user_data["password"]
    return authentication_payload

def get_user_token(playwright, user_profile):
    """
    This functions returns user token

    :param playwright: a fixture
    :param user_profile: A key from a user_credentials.json file
    :return: user token
    """
    authentication_payload = build_auth_request_payload(user_profile)
    response = authenticate_with_user(playwright, authentication_payload)
    user_token = response.json()["accessToken"]
    return user_token

def set_cookies(context, user_token):
    """
    This function sets user cookies
    """
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])

def authenticate_with_user_profile(playwright, context, user_profile):
    user_token = get_user_token(playwright, user_profile)
    set_cookies(context, user_token)