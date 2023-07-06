from cx_Freeze import setup, Executable

from main import VERSION


setup(
    name="D4LP",
    version=VERSION,
    description="Application for downloading musics from Youtube and Spotify quickly.",
    options={
        "build_exe": {
            "packages": ["os", "json", "re", "bs4", "pytube", "urllib.error", "urllib.request"]
        }
    },
    executables=[
        Executable(
            script="main.py",
            icon="icon.ico",
            shortcut_name="D4LP",
            shortcut_dir="ProgramMenuFolder"
        )
    ]
)
