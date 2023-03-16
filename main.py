import os
import eel
from downloader import Download
from tkinterLayer import GetFileDialog, GetCenterOfMonitor


@eel.expose
def DowloadVideo(src: str, dir: str):
    return Download(src, dir)


@eel.expose
def SelectFolder():
    return GetFileDialog()


@eel.expose
def CheckPath(path: str):
    return True if os.path.isdir(path) else False


if __name__=="__main__":
    windowSize=(800, 550)

    eel.init("Interface")
    eel.start("index.html", size=windowSize, shutdown_delay=0,
              position=GetCenterOfMonitor(windowSize))