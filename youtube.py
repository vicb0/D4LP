import re
from threading import Lock

from pytube import YouTube, Search


print_lock = Lock()


def sync_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


def download(obj, path):
    name = re.sub(r"\\|\/|\:|\*|\?|\"|\<|\>|\|", "", obj.title)
    name = f"{name}.mp3"
    sync_print("Downloading", name)

    obj.streams.filter(only_audio=True).order_by("abr").desc().first().download(
        filename=name,
        output_path=path
    )

    return name


def download_by_link(link, path):
    yt = YouTube(link)
    
    return download(yt, path)


def download_by_name(name, path):
    s = Search(name)
    yt = s.results[0]

    return download(yt, path)


def main():
    # Used for testing
    pass


if __name__ == "__main__":
    main()

