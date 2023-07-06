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


def download_single(link, path):
    try:
        html = parse_html(link)
    except HTTPError:
        print("Error: Not a valid link.")
        return 0

    try:
        name = parse_name(html)
        author = parse_author(html)    
        youtube.download_by_name(f"{author} {name}", path)
    except Exception as err:
        print(f"Error: {err}")
        return 0
    
    return 1


def download_playlist(file_dir, path):
    with open(file_dir.replace("\"", ""), "r") as f:
        links = f.readlines()

    success = 0
    for c, link in enumerate(links, 1):
        if link and not link.isspace():
            print(f"{c}/{len(links)}")
            success += download_single(link, path)
            
    print(f"{success} out of {len(links)} downloaded successfully.")


def main():
    # Used for testing
    download_single("https://open.spotify.com/track/5P1BZpdmaVFm0OwPbWe5Dz", "./songs")


if __name__ == "__main__":
    main()
