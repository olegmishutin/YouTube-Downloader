from tkinter import *
from tkinter import filedialog

root=Tk()
root.withdraw()


def GetFileDialog():
    return filedialog.askdirectory(initialdir="/")


def GetCenterOfMonitor(windowSize: tuple):
    screenWidthCenter=root.winfo_screenwidth() / 2 - windowSize[0] / 2
    screenHeightCenter=root.winfo_screenheight() / 2 - windowSize[1] / 2

    return (screenWidthCenter, screenHeightCenter)