import os
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Downloader():
    def __init__(self, cachePathName: str):
        self.__cachePath=cachePathName
        self.__youtube=None

    def GetVideoInfo(self, source: str):
        try:
            self.__youtube=YouTube(source)

            author=self.__youtube.author
            title=self.__youtube.title

            return f"Author: {author}; Title: {title}"
        except Exception:
            self.__youtube=None

            return "Incorrect link or server error" if source else ""

    def GetFileName(self):
        file=os.path.basename(os.listdir(self.__cachePath)[0])
        fileName=os.path.splitext(file)[0]

        return fileName

    def CombineAudioVideoFiles(self, filename: str, pathToCombine: str):
        videoClip=VideoFileClip(f"{self.__cachePath}/{filename}.mp4")
        audioClip=AudioFileClip(f"{self.__cachePath}/{filename}.webm")

        try:
            videoClip.audio=CompositeAudioClip([audioClip])
            videoClip.write_videofile(f"{pathToCombine}/{filename}.mp4",
                                      temp_audiofile=\
                                          f"{self.__cachePath}/Cache.mp3")
        finally:
            shutil.rmtree(self.__cachePath)

    def GetMaxResolution(self):
        resolutionCodec={"1080p": [137, 299, 399, 699],
                         "720p": [136, 298, 398, 698],
                         "480p": [135, 397, 697],
                         "360p": [134, 396, 696],
                         "240p": [133, 395, 695],
                         "144p": [160, 394, 694]}

        for resolution in resolutionCodec:
            filter=self.__youtube.streams.filter(file_extension='mp4',
                                                 audio_codec=None,
                                                 res=resolution).itag_index

            for codec in resolutionCodec.get(resolution):
                if codec in filter.keys():
                    return codec

    def DownloadVideo(self, source: str, pathForSaving: str):
        if self.__youtube:
            if not os.path.isdir(self.__cachePath):
                os.mkdir(self.__cachePath)

            try:
                downloader=\
                    self.__youtube.streams.get_by_itag(
                        self.GetMaxResolution())
                downloader.download(output_path=self.__cachePath)

                downloader=self.__youtube.streams.get_by_itag(251)
                downloader.download(output_path=self.__cachePath)
            except (Exception, KeyboardInterrupt):
                shutil.rmtree(self.__cachePath)

                return "Server error, try again"

            self.CombineAudioVideoFiles(self.GetFileName(), pathForSaving)
            return f"Video downloaded in {pathForSaving}"
        else:
            return "Incorrect link"