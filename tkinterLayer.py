import sys
from tkinter import *
from tkinter import filedialog


class TkinterLayer():
    def __init__(self):
        self.__root=Tk()
        self.__root.withdraw()

        if sys.platform=="win32":
            self.__root.iconbitmap("Interface/Image/Icon.ico")

    def GetPathForDownload(self):
        return filedialog.askdirectory(title="Select path for saving",
                                       initialdir="/")

    def GetCenterOfMonitor(self, windowSize: tuple):
        CenterX=self.__root.winfo_screenwidth() / 2 - windowSize[0] / 2
        CenterY=self.__root.winfo_screenheight() / 2 - windowSize[1] / 2

        return (CenterX, CenterY)