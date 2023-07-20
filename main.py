import os
import eel
import sys
import subprocess
from downloader import Downloader
from tkInterLayer import TkInterLayer


@eel.expose
def DataThemeSetting(mode: str, theme: str) -> str:
    with open(dataThemeFile, mode) as file:
        if mode=="r":
            return file.read()
        file.write(theme)


@eel.expose
def GetVideoInfo(source: str) -> str:
    return videoDownloader.GetVideoInfo(source)


@eel.expose
def GetVideoResolutions() -> list:
    return videoDownloader.GetVideoResolutions()


@eel.expose
def GetPathForDownloading() -> str:
    return tkInterLayer.GetPathForDownloading()


@eel.expose
def CheckPath(path: str) -> bool:
    return os.path.isdir(path)


@eel.expose
def DowloadVideo(source: str, path: str, resolution: str) -> str:
    return videoDownloader.DownloadVideo(source, path, resolution)


@eel.expose
def OpenSavingPath(path: str):
    if os.path.isdir(path):
        if sys.platform=="win32":
            os.startfile(path)
        else:
            subprocess.call(["open" if sys.platform=="darwin" else "xdg-open", path])


if __name__=="__main__":
    windowSize=(800, 550)
    dataThemeFile="dataTheme.txt"

    pytubeLocalPath="pytube"
    pytubeLocalCachePath=f"{pytubeLocalPath}/__cache__"

    if not os.path.isfile(dataThemeFile):
        DataThemeSetting('w', "dark")

    if not os.path.isdir(pytubeLocalPath):
        os.mkdir(pytubeLocalPath)

    if not os.path.isdir(pytubeLocalCachePath):
        os.mkdir(pytubeLocalCachePath)

    tkInterLayer=TkInterLayer()
    videoDownloader=Downloader()

    if sys.platform=="win32":
        tkInterLayer.iconbitmap("Interface/Image/Icon.ico")

    eel.init("Interface")
    eel.start("index.html", port=0, size=windowSize, shutdown_delay=0,
              position=tkInterLayer.GetCenterOfMonitor(windowSize))