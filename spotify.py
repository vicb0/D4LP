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
    except HTTPError:
        counters['count'] += 1
        youtube.sync_print(f"Error: Not a valid link. ({link}) {counters['count']}/{n}")
        return 0

    try:
        name = parse_name(html)
        author = parse_author(html)    
        name = youtube.download_by_name(f"{author} {name}", path)
    except Exception as err:
        counters['count'] += 1
        youtube.sync_print(f"Error: {err} ({link}) {counters['count']}/{n}")
        return 0
    
    counters['success'] += 1
    counters['count'] += 1
    youtube.sync_print(f"Downloaded {name} {counters['count']}/{n}")
    return 1


def download_playlist(file_dir, path):
    with open(file_dir.replace("\"", ""), "r") as f:
        links = [link.strip() for link in f.readlines() if link and not link.isspace()]

    threads = []
    counters = {"success": 0, 'count': 0}
    n = len(links)
    offset = 0

    while links:
        for i in range(n - 1 - offset, -1, -1):
            t = Thread(target=download_single, args=[links[i], path, counters, n])
            threads.append(t)
            links.pop(-1)
            offset += 1

            if len(threads) >= 100:
                break

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(60)

        threads = []

    print(f"{counters['success']} out of {n} downloaded successfully.")


def main():
    # Used for testing
    download_single("https://open.spotify.com/track/5P1BZpdmaVFm0OwPbWe5Dz", "./songs")


if __name__ == "__main__":
    main()
