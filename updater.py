import json

import requests

from consts import *


def check_for_updates():
    response = requests.get(REPO)
    latest = response.json()[0].get("tag_name")

    if latest > VERSION:
        print("UPDATE")


def main():
    # Used for testing
    check_for_updates()


if __name__ == "__main__":
    main()
