import json
import os
import subprocess
import sys

import eel

from downloader import Downloader
from tkInterLayer import TkInterLayer


@eel.expose
def Settings(settings_param: str, mode: str, data="") -> str | None:
    if mode == "r":
        return settings[settings_param]

    settings[settings_param] = data

    with open(settingFile, "w") as file:
        json.dump(settings, file)


@eel.expose
def GetVideoInfo(source: str) -> str:
    return videoDownloader.GetVideoInfo(source)


@eel.expose
def GetVideoResolutions() -> list:
    return videoDownloader.GetVideoResolutions()


@eel.expose
def GetPathForDownloading() -> str:
    path = tkInterLayer.GetPathForDownloading()

    if os.path.exists(path):
        return path
    return ''


@eel.expose
def DownloadVideo(source: str, resolution: str) -> str:
    if os.path.exists(settings["videos_folder"]):
        return videoDownloader.DownloadVideo(
            source, settings["videos_folder"], resolution
        )
    return "Path for videos not set or does not exist"


@eel.expose
def OpenVideosFolder() -> None:
    if os.path.exists(settings["videos_folder"]):
        if sys.platform == "win32":
            os.startfile(settings["videos_folder"])
        else:
            subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", settings["videos_folder"]])


if __name__ == "__main__":
    windowSize = (800, 550)

    settings = {"theme": "dark", "videos_folder": ""}
    settingFile = "settings.json"

    pytubeLocalPath = "pytube"
    pytubeLocalCachePath = f"{pytubeLocalPath}/__cache__"

    if os.path.isfile(settingFile):
        with open(settingFile, "r") as file:
            settings = json.load(file)
    else:
        with open(settingFile, "w") as file:
            json.dump(settings, file)

    if not os.path.isdir(pytubeLocalPath):
        os.mkdir(pytubeLocalPath)

    if not os.path.isdir(pytubeLocalCachePath):
        os.mkdir(pytubeLocalCachePath)

    tkInterLayer = TkInterLayer()
    videoDownloader = Downloader()

    if sys.platform == "win32":
        tkInterLayer.iconbitmap("Interface/Image/Icon.ico")

    eel.init("Interface")
    eel.start(
        "index.html",
        port=0,
        size=windowSize,
        shutdown_delay=0,
        position=tkInterLayer.GetCenterOfMonitor(windowSize),
    )
