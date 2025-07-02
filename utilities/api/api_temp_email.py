import re
from playwright.sync_api import Playwright

mailslurp = "https://api.mailslurp.com"


def create_new_email_address(playwright: Playwright):
    api_request_context = playwright.request.new_context(base_url=mailslurp)
    response = api_request_context.post(
        "/inboxes/withDefaults",
        headers={
            "Context-type": "application/json",
            "X-API-KEY": "35d1de41187637bb7e3cbbabd6a09e247ff4ffa08282a6e801932420882741fa"
        }
    )
    response_data = response.json()
    new_email_name = response_data["emailAddress"]
    new_email_id = response_data["id"]

    return new_email_name, new_email_id


def wait_for_email_and_read(playwright: Playwright, email_id):
    api_request_context = playwright.request.new_context(base_url=mailslurp)
    response = api_request_context.get(
        f"/waitForLatestEmail?inboxId={email_id}&timeout=8000&unreadOnly=true",
        headers={
            "Context-type": "application/json",
            "X-API-KEY": "35d1de41187637bb7e3cbbabd6a09e247ff4ffa08282a6e801932420882741fa"
        }
    )
    response_data = response.json()
    body = response_data["body"]
    link = re.search(r'href="([^"]+register-invite[^"]+)"', body)
    return link.group(1)


def delete_email(playwright: Playwright, email_id):
    api_request_context = playwright.request.new_context(base_url=mailslurp)
    response = api_request_context.delete(
        f"/inboxes/{email_id}",
        headers={
            "Context-type": "application/json",
            "X-API-KEY": "35d1de41187637bb7e3cbbabd6a09e247ff4ffa08282a6e801932420882741fa"
        }
    )
    return response