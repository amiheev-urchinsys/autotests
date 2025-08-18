import json
import re


def get_key_value_from_file(file_name, key):
    """
    Returns the list with data from the given file

    :param file_name: Give file name with its extension
    :param key: Give key name
    :return: List with data
    """
    with open("data/" + file_name + "") as f:
        file_data = json.load(f)
        key_value = file_data[key]
    return key_value


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

def write_new_password_to_temp_email(file_name, new_password):
    with open("data/" + file_name + "") as f:
        file_data = json.load(f)

    file_data["temp_email"]["password"] = new_password
    with open("data/" + file_name + "", "w") as f:
        json.dump(file_data, f, indent=4)