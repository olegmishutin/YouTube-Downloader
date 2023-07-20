from tkinter import *
from tkinter import filedialog


class TkInterLayer(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

    def GetPathForDownloading(self) -> str:
        selectedPath=filedialog.askdirectory(title="Select path for saving", initialdir="/")
        return selectedPath if selectedPath else ""

    def GetCenterOfMonitor(self, windowSize: tuple) -> tuple:
        return (self.winfo_screenwidth() / 2 - windowSize[0] / 2, self.winfo_screenheight() / 2 - windowSize[1] / 2)