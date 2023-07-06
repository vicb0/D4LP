import os
import json

import updater
import youtube
import spotify
from consts import *


def setup_settings():
    default = {
        "download_path": f"{os.getenv('USERPROFILE')}\\Downloads\\songs"
    }

    with open("./settings.json", "w", encoding="utf8") as f:
        json.dump(default, f, indent=4, ensure_ascii=False)

    return default


def load_settings():
    if not os.path.isfile("./settings.json"):
        return setup_settings()

    with open("./settings.json", "r", encoding="utf8") as f:
        return json.loads(f.read().replace("\\", "/"))


def select(string):
    if string.startswith("https://www.youtube.com"):
        return "link"
    
    if os.path.isfile(string.replace("\"", "")):
        return "spotify"

    if string and not string.isspace():
        return "name"


def help_():
    print("""Commands:
    chkupd -> Manually check for updates.
    settings -> Check/change settings.
    dir -> Get the download directory.
    about -> Check some information about the program.
""")


def about():
    print(f"""Installed version: {VERSION}
Check this program's source code here: {REPO}
Check for different versions here: {REPO_DIST}
""")


def change_download_path():
    new_dir = input("Insert a valid directory (empty to cancel): ")

    if not new_dir.strip():
        return

    if not os.path.isdir(new_dir):
        print("Directory not valid.")
        return
    if not os.access(new_dir, os.W_OK):
        print("Program does not have permission to write to this directory.")
        return

    with open("./settings.json", "w", encoding="utf8") as f:
        json.dump({"download_path": new_dir}, f, indent=4, ensure_ascii=False)

    SETTINGS["download_path"] = new_dir


def change_settings():
    linker = {
        "1": change_download_path
    }

    string = input("""1 -> Change download path.
Anything else -> Go back.
""")

    if (func := linker.get(string.strip())) is not None:
        func()


def get_download_path():
    print(f"Download directory set to: {SETTINGS['download_path']}")


def close():
    os._exit(1)


def main():
    global SETTINGS
    updater.check_for_updates()

    SETTINGS = load_settings()
    
    downloader_linker = {
        "link": youtube.download_by_link,
        "name": youtube.download_by_name,
        "spotify": spotify.download_playlist
    }

    others_linker = {
        "help": help_,
        "chkupd": updater.check_for_updates,
        "about": about,
        "dir": get_download_path,
        "settings": change_settings,
        "exit": close
    }

    print("Type 'help' for more information.")
    while True:
        string = input(">")
        
        if (func := others_linker.get(string.lower().strip())) is not None:
            func()
            continue

        opt = select(string)

        try:
            downloader_linker[opt](string, SETTINGS["download_path"])
        except KeyError:
            pass


if __name__ == "__main__":
    main()
