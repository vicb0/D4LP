import os
from threading import Thread

from urllib.error import HTTPError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import youtube


def parse_html(link):
    req = Request(link)
    response = urlopen(req)

    return BeautifulSoup(response, "html.parser")


def parse_name(html):
    return html.find("h1").text


def parse_author(html):
    return html.find("a").text


def download_single(link, path, counters, n):
    try:
        html = parse_html(link)
    except HTTPError as err:
        counters['count'] += 1
        counters['logs'].append(f"Could not parse html. Error: {err} ({link}) {counters['count']}/{n}")
        return

    try:
        name = parse_name(html)
        author = parse_author(html)
    except Exception as err:
        counters['count'] += 1
        counters['logs'].append(f"Could not parse the song's data. Error: {err} ({link}) {counters['count']}/{n}")
        return

    search_string = f"{author} {name}"

    try:
        yt_obj = youtube.download_by_name(search_string)
    except Exception as err:
        counters['count'] += 1
        counters['logs'].append(f"Could not find song '{search_string}' on Youtube. Error: {err} ({link}) {counters['count']}/{n}")
        return

    name = youtube.convert_to_filename(yt_obj)

    if name in counters['downloaded']:
        counters['count'] += 1
        counters['logs'].append(f"'{name}' was duplicated, therefore skipped. {counters['count']}/{n}")
        return

    counters['downloaded'].add(name)

    if os.path.isfile(f"{path}/{name}"):
        counters['count'] += 1
        counters['logs'].append(f"'{name}' was duplicated, therefore skipped. {counters['count']}/{n}")
        return

    try:
        youtube.download(yt_obj, name, path)
    except Exception as err:
        counters['count'] += 1
        counters['logs'].append(f"Could not download '{name}'. Error: {err} ({link}) {counters['count']}/{n}")

    counters['count'] += 1
    counters['success'] += 1
    youtube.sync_print(f"Downloaded {name} {counters['count']}/{n}")


def download_playlist(file_dir, path):
    with open(file_dir.replace("\"", ""), "r") as f:
        links = {link.strip() for link in f.readlines() if link and not link.isspace()}

    threads = []
    counters = {"success": 0, 'count': 0, 'downloaded': set(), 'logs': []}
    n = len(links)

    while links:
        count = 1
        while links and count <= 100:
            link = links.pop()
            count += 1

            t = Thread(target=download_single, args=[link, path, counters, n])
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
           thread.join(10)

        for thread in threads:
            if thread.is_alive():
                counters['logs'].append(f"Timeout on '{thread._args[0]}'.")

        threads = []

    print(f"\n{counters['success']} out of {n} downloaded successfully.")
    for log in counters['logs']:
        print(log)
    print("\nUse the command 'open' to quickly open the folder with the songs.")


def main():
    # Used for testing
    download_single("https://open.spotify.com/track/5P1BZpdmaVFm0OwPbWe5Dz", "./songs")


if __name__ == "__main__":
    main()
