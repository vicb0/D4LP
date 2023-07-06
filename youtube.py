import re

from pytube import YouTube, Search


def download(obj, path):
    name = re.sub(r"\\|\/|\:|\*|\?|\"|\<|\>|\|", "", obj.title)
    name = f"{name}.mp3"
    print("Downloading", name)

    obj.streams.filter(only_audio=True).order_by("abr").desc().first().download(
        filename=name,
        output_path=path
    )


def download_by_link(link, path):
    yt = YouTube(link)
    
    download(yt, path)


def download_by_name(name, path):
    s = Search(name)
    yt = s.results[0]

    download(yt, path)


def main():
    # Used for testing
    pass


if __name__ == "__main__":
    main()

