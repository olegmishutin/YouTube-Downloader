import sys
from tkinter import *
from tkinter import filedialog


class TkInterLayer(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        if sys.platform=="win32":
            self.iconbitmap("Interface/Image/Icon.ico")

    def GetPathForDownloading(self) -> str:
        return filedialog.askdirectory(title="Select path for saving", initialdir="/")

    def GetCenterOfMonitor(self, windowSize: tuple) -> tuple:
        centerX= self.winfo_screenwidth() / 2 - windowSize[0] / 2
        centerY= self.winfo_screenheight() / 2 - windowSize[1] / 2

        return (centerX, centerY)