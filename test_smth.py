import time

from playwright.sync_api import Playwright, expect
from pageObjects.homePage import HomePage
from pageObjects.loginPage import LoginPage
from utilities.api.api_base import get_user_token


def test_auth(playwright: Playwright):
    response = get_user_token(playwright)
    user_token = response.json()["accessToken"]
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # 👇 Set the cookie with the token
    context.add_cookies([{
        "name": "access-token-plextera",  # or "auth_token", depending on your app
        "value": user_token,
        "domain": "studio.dev.plextera.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }])
    page = context.new_page()

    page.goto("https://studio.dev.plextera.com")
    on_login_page = LoginPage(page)
    on_home_page = HomePage(page)

    on_home_page.sidebar.sidebar_bottom_section.hover()
    on_home_page.sidebar.personal_cabinet_dropdown_menu.click()
    on_home_page.sidebar.personal_cabinet_log_out_point.click()

    expect(on_login_page.page_title).to_contain_text("Welcome to Plextera")