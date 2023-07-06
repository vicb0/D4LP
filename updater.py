import os
import webbrowser

import requests

from consts import *


def check_for_updates():
    try:
        response = requests.get(REPO_RELEASES)
    except requests.exceptions.ConnectionError:
        input("No internet available.")
        os._exit(1)
    except requests.exceptions.RequestException as err:
        print(f"Couldn't check for updates. The program might not work properly.\nError: {err}")
        return

    latest = response.json()[0].get("tag_name")

    if latest > VERSION:
        confirm_update()
    else:
        print("Your program is up to date!")


def confirm_update():
    print("A new version is available. Not updating might lead to the program not working properly. Do you wish to update? (y/yes/n/no)")

    while True:
        opt = input().lower()

        if opt in ("y", "yes"):
            webbrowser.open(REPO_RELEASES)
            os._exit(1)
        elif opt in ("n", "no"):
            break
        
    os.system("clear||cls")


def main():
    # Used for testing
    check_for_updates()


if __name__ == "__main__":
    main()
