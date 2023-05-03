import os
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Downloader():
    def __init__(self):
        self.__cache="cache"
        self.__video=None
        self.__resolutionsCodecs={"4320p": [138, 402, 571], "2160p": [266, 305, 401, 701],
                                  "1440p": [264, 304, 400, 700], "1080p": [137, 299, 399, 699],
                                  "720p": [136, 298, 398, 698], "480p": [135, 397, 697],
                                  "360p": [134, 396, 696], "240p": [133, 395, 695],
                                  "144p": [160, 394, 694]}

    def GetVideoInfo(self, source: str) -> str:
        try:
            self.__video=YouTube(source, use_oauth=True, allow_oauth_cache=True)

            return f"Author: {self.__video.author}; Title: {self.__video.title}"
        except Exception:
            self.__video=None

            return "Incorrect link or server error" if source else ""

    def GetVideoItag(self, resolution: str):
        return self.__video.streams.filter(file_extension='mp4', progressive=False, res=resolution).itag_index.keys()

    def GetVideoResolutions(self) -> list:
        availableRes=[]

        if self.__video:
            for resolution in self.__resolutionsCodecs:
                for codec in self.__resolutionsCodecs.get(resolution):
                    if (codec in self.GetVideoItag(resolution)) and (resolution not in availableRes):
                        availableRes.append(resolution)

        return availableRes

    def GetVideoCodec(self, resolution) -> list:
        return list(self.GetVideoItag(resolution))[0]

    def GetVideoName(self) -> str:
        file=os.path.basename(os.listdir(self.__cache)[0])
        fileName=os.path.splitext(file)[0]

        return fileName

    def CombineAudioVideoFiles(self, filename: str, pathToCombine: str):
        videoClip=VideoFileClip(f"{self.__cache}/{filename}.mp4")
        audioClip=AudioFileClip(f"{self.__cache}/{filename}.webm")

        videoClip.audio=CompositeAudioClip([audioClip])
        videoClip.write_videofile(f"{pathToCombine}/{filename}.mp4", temp_audiofile=f"{self.__cache}/Cache.mp3")

    def DownloadVideo(self, source: str, pathForSaving: str, resolution: str) -> str:
        if self.__video:
            if os.path.isdir(self.__cache) and os.listdir(self.__cache):
                shutil.rmtree(self.__cache)

            os.mkdir(self.__cache)
            try:
                mp4Downloader=self.__video.streams.get_by_itag(self.GetVideoCodec(resolution))
                mp4Downloader.download(output_path=self.__cache)

                mp3Downloader=self.__video.streams.get_by_itag(251)
                mp3Downloader.download(output_path=self.__cache)

                self.CombineAudioVideoFiles(self.GetVideoName(), pathForSaving)
            except Exception:
                return "Server error, try again"
            finally:
                shutil.rmtree(self.__cache)

            return f"Video downloaded in {pathForSaving}"
        return "Incorrect link or server error"