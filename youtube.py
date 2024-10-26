import re
from threading import Lock

from pytubefix import YouTube, Search


print_lock = Lock()


def sync_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


def convert_to_filename(obj):
    name = re.sub(r"\\|\/|\:|\*|\?|\"|\<|\>|\|", "", obj.title)
    name = f"{name}.mp3"

    return name


def download(obj, name, path):
    sync_print("Downloading", name)

    obj.streams.filter(only_audio=True).order_by("abr").desc().first().download(
        filename=name,
        output_path=path
    )

    return name


def download_by_link(link):
    yt = YouTube(link)
    
    return yt


def download_by_name(name):
    s = Search(name)
    yt = s.videos[0]

    return yt


def main():
    # Used for testing
    pass


if __name__ == "__main__":
    main()

