import os
import json

import updater
import youtube
import spotify


def setup_settings():
    default = {
        "download_path": f"{os.getenv('USERPROFILE')}\\Downloads\\songs"
    }

    with open("./settings.json", "w") as f:
        json.dump(default, f)

    return default


def load_settings():
    if not os.path.isfile("./settings.json"):
        return setup_settings()

    with open("./settings.json", "r") as f:
        return json.loads(f.read().replace("\\", "/"))


def select(string):
    if string.startswith("https://www.youtube.com"):
        return "link"
    
    if os.path.isfile(string.replace("\"", "")):
        return "spotify"

    if string and not string.isspace():
        return "name"


def main():
    updater.check_for_updates()
    settings = load_settings()
    
    linker = {
        "link": youtube.download_by_link,
        "name": youtube.download_by_name,
        "spotify": spotify.download_playlist
    }

    while True:
        opt = input(">")
        
        try:
            linker[select(opt)](opt, settings["download_path"])
        except KeyError:
            pass


if __name__ == "__main__":
    main()
