import requests
import json
import argparse

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable self-signed certificate warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def login(phone):

    try:
        data = { 'phone': phone }
        response = requests.post("http://localhost:3000/login", json=data)
        return json.loads(response.content)['url']
    except Exception as exception:
        print(f"Error login: {exception}")


def auth(url):
    try:
        response = requests.get(url, verify=False)
        return json.loads(response.content)["devicePhoneNumberVerified"]
    except Exception as exception:
        print(f"Error auth: {exception}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Network Enablement API client example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("phone", help="Phone Number to verify")
    args = vars(parser.parse_args())

    url = login(args["phone"])

    if auth(url):
        print("Client successfully authenticated!")
    else:
        print("Unable to verify client credentials")
