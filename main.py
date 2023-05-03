import os
import eel
import sys
import subprocess
from downloader import Downloader
from tkInterLayer import TkInterLayer


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
            opener="open" if sys.platform=="darwin" else "xdg-open"
            subprocess.call([opener, path])


if __name__=="__main__":
    windowSize=(800, 550)
    pytubeCachePath="pytube"

    if not os.path.isdir(pytubeCachePath):
        os.mkdir(pytubeCachePath)
        os.mkdir(f"{pytubeCachePath}/__cache__")

    tkInterLayer=TkInterLayer()
    videoDownloader=Downloader()

    eel.init("Interface")
    eel.start("index.html", port=0, size=windowSize, shutdown_delay=0,
              position=tkInterLayer.GetCenterOfMonitor(windowSize))