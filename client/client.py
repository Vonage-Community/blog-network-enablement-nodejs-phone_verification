import requests
import json
import argparse
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable self-signed certificate warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def send_request(url, body, key_response=""):
    """
    Helper function to send API request (GET/POST)

    Args:
        url (str): The URL to send the request.
        body (dict): JSON body. Only for POST requests.
        key_response (str): Optional JSON key whose value should be returned.

    Returns:
        str: The value from the JSON key, or the entire response if no key is provided.

    Raises:
        ValueError: if the URL or Body is invalid. 
        RequestException: Raised for 4xx/5xx HTTP responses.
        KeyError: If the expected key is not present in the response. 
    """

    if not url or not isinstance(url, str):
        raise ValueError("Invalid url provided.")

    if body and not isinstance(body, dict):
        raise ValueError("Invalid body provided.")

    if body:
        response = requests.post(url, json=body)
    else:
        response = requests.get(url, verify=False)

    # Raise HTTPError exception with 4xx or 5xx responses
    response.raise_for_status()

    response_data = response.json()

    if key_response and key_response not in response_data:
        raise KeyError(f"The {key_response} key is missing in the response.")
    else:
        return response_data[key_response]

    return response_data


def login(url, phone):
    """
    Initializes the auth process by calling to the /login method
    from the backend.

    Args:
        url (str): The backend URL.
        phone (dict): The user's phone number.

    Returns:
        str: The authorization URL returned from the server

    Raises:
        ValueError: If the phone number is invalid.
        RequestException: for 4xx/5xx HTTP responses.
        KeyError: If the 'url' key is not present in the response.
    """
    return send_request(url, phone, "url")


def auth(url):
    """
    Authenticates a user by sending the authorization URL retrieved
    by the login() method to the mobile operator.

    Args:
        url (str): The auth URL to send the request to.

    Returns:
        bool: The value of 'devicePhoneNumberVerified' from the server's response.

    Raises:
        ValueError: If the URL is invalid.
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
        KeyError: If the 'devicePhoneNumberVerified' key is missing in the response.
    """
    return send_request(url, None, "devicePhoneNumberVerified")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Network Enablement API client example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("phone", help="Phone Number to verify")
    args = vars(parser.parse_args())

    server = "http://localhost:3000/login"
    data = {"phone": args["phone"]}

    try:
        auth_url = login(server, data)
    except Exception as exception:
        print(f"Error login: {exception}")
        sys.exit(-1)

    try:
        result = auth(auth_url)
        print(f"Response from API call: {result}")
        if result:
            print("Client successfully authenticated!")
        else:
            print("Unable to verify client credentials")
    except Exception as exception:
        print(f"Error login: {exception}")
