import sys
from tkinter import *
from tkinter import filedialog


class TkInterLayer():
    def __init__(self):
        self.__tk=Tk()
        self.__tk.withdraw()

        if sys.platform=="win32":
            self.__tk.iconbitmap("Interface/Image/Icon.ico")

    def GetPathForDownloading(self) -> str:
        return filedialog.askdirectory(title="Select path for saving", initialdir="/")

    def GetCenterOfMonitor(self, windowSize: tuple) -> tuple:
        centerX= self.__tk.winfo_screenwidth() / 2 - windowSize[0] / 2
        centerY= self.__tk.winfo_screenheight() / 2 - windowSize[1] / 2

        return (centerX, centerY)