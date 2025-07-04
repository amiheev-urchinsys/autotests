import json
import re


def get_list_from_file(file_name, list_title):
    """
    Returns the list with data from the given file

    :param file_name: Give file name with its extension
    :param list_title: Give key name that has list value
    :return: List with data
    """
    with open("data/" + file_name + "") as f:
        file_data = json.load(f)
        required_list = file_data[list_title]
    return required_list


def get_value_by_key_from_list(data, target_key):
    """
    Recursively searches for a key in a nested dictionary/list and returns its value.

    :param data: The JSON data (dictionary or list).
    :param target_key: The key whose value is being searched for.
    :return: The value of the target_key if found, otherwise None.
    """
    # If data - is a list, recursively check each element
    if isinstance(data, list):
        for item in data:
            result = get_value_by_key_from_list(item, target_key)
            if result:
                return result

    # If data - is a dictionary, check for the presence of the key
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            # If a key is not found, but the value is a dictionary or a list, continue searching
            elif isinstance(value, (dict, list)):
                result = get_value_by_key_from_list(value, target_key)
                if result:
                    return result

    return None  # return None, if a key is not found


def get_register_link_from_the_email_body(body):
    """
    Returns a register link from the html body of the letter

    :param body: html body of a letter
    :return: Register link
    """
    reg_link = re.search(r'href="([^"]+register-invite[^"]+)"', body)
    return reg_link.group(1)


def get_create_new_password_link_from_the_email_body(body):
    """
    Returns a register link from the html body of the letter

    :param body: api request response
    :return: Register link
    """
    reg_link = re.search(r'href="([^"]+create-password[^"]+)"', body)
    return reg_link.group(1)
