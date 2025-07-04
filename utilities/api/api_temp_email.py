import re
from playwright.sync_api import Playwright

mailslurp = "https://api.mailslurp.com"


def create_new_email_address(playwright: Playwright):
    """
    Create a new temporary email address.

    :param playwright: An instance of the Playwright library used to create the API request context.
    :return: Email name and its id
    """
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
    """
    Wait for email letter and return its html body

    :param playwright: An instance of the Playwright library used to create the API request context.
    :param email_id: Email ID
    :return: html body of a letter
    """
    api_request_context = playwright.request.new_context(base_url=mailslurp)
    response = api_request_context.get(
        f"/waitForLatestEmail?inboxId={email_id}&timeout=8000&unreadOnly=true",
        headers={
            "Context-type": "application/json",
            "X-API-KEY": "35d1de41187637bb7e3cbbabd6a09e247ff4ffa08282a6e801932420882741fa"
        }
    )
    response_data = response.json()
    return response_data['body']


def delete_email(playwright: Playwright, email_id):
    """
    Delete created temporary email address.

    :param playwright: An instance of the Playwright library used to create the API request context.
    :param email_id: Email ID
    :return: Response...
    """
    api_request_context = playwright.request.new_context(base_url=mailslurp)
    response = api_request_context.delete(
        f"/inboxes/{email_id}",
        headers={
            "Context-type": "application/json",
            "X-API-KEY": "35d1de41187637bb7e3cbbabd6a09e247ff4ffa08282a6e801932420882741fa"
        }
    )
    return response


def delete_emails_in_inbox(playwright: Playwright, email_id):
    """
    Delete created temporary email address.

    :param playwright: An instance of the Playwright library used to create the API request context.
    :param email_id: Email ID
    :return: Response...
    """
    api_request_context = playwright.request.new_context(base_url=mailslurp)
    response = api_request_context.delete(
        f"/emptyInbox?inboxId={email_id}",
        headers={
            "Context-type": "application/json",
            "X-API-KEY": "35d1de41187637bb7e3cbbabd6a09e247ff4ffa08282a6e801932420882741fa"
        }
    )
    return response
