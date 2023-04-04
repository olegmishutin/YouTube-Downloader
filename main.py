import os
import eel
import sys
import subprocess
from downloader import Downloader
from tkinterLayer import TkinterLayer


@eel.expose
def GetVideoInfo(src: str):
    return ytDownloader.GetVideoInfo(src)


@eel.expose
def SelectFolder():
    return tkLayer.GetPathForDownload()


@eel.expose
def CheckPath(path: str):
    return True if os.path.isdir(path) else False


@eel.expose
def DowloadVideo(src: str, dir: str):
    return ytDownloader.DownloadVideo(src, dir)


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

    tkLayer=TkinterLayer()
    ytDownloader=Downloader(cachePathName="cache")

    eel.init("Interface")
    eel.start("index.html", size=windowSize, shutdown_delay=0,
              position=tkLayer.GetCenterOfMonitor(windowSize))
