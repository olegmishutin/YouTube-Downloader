import sys
from tkinter import *
from tkinter import filedialog


class TkinterLayer():
    def __init__(self):
        self.root=Tk()
        self.root.withdraw()

        if sys.platform=="win32":
            self.root.iconbitmap("Interface/Image/Icon.ico")

    def GetPathForDownload(self):
        return filedialog.askdirectory(title="Select path for saving",
                                       initialdir="/")

    def GetCenterOfMonitor(self, windowSize: tuple):
        CenterX=self.root.winfo_screenwidth() / 2 - windowSize[0] / 2
        CenterY=self.root.winfo_screenheight() / 2 - windowSize[1] / 2

        return (CenterX, CenterY)
