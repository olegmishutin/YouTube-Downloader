import os
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Downloader():
    def __init__(self):
        self.__cache="cache"
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
        file=os.path.basename(os.listdir(self.__cache)[0])
        fileName=os.path.splitext(file)[0]

        return fileName

    def CombineAudioVideoFiles(self, filename: str, pathToCombine: str):
        videoClip=VideoFileClip(f"{self.__cache}/{filename}.mp4")
        audioClip=AudioFileClip(f"{self.__cache}/{filename}.webm")

        videoClip.audio=CompositeAudioClip([audioClip])
        videoClip.write_videofile(f"{pathToCombine}/{filename}.mp4",
                                  temp_audiofile=\
                                      f"{self.__cache}/Cache.mp3")

    def GetMaxRes(self):
        streams=self.__youtube.streams
        resolutionCodec={"1080p": [137, 299, 399, 699],
                         "720p": [136, 298, 398, 698],
                         "480p": [135, 397, 697],
                         "360p": [134, 396, 696],
                         "240p": [133, 395, 695],
                         "144p": [160, 394, 694]}

        for resolution in resolutionCodec:
            filter=streams.filter(file_extension='mp4',
                                  audio_codec=None,
                                  res=resolution).itag_index

            for codec in resolutionCodec.get(resolution):
                if codec in filter.keys():
                    return codec

    def DownloadVideo(self, source: str, pathForSaving: str):
        if self.__youtube:
            if os.path.isdir(self.__cache) and os.listdir(self.__cache):
                shutil.rmtree(self.__cache)

            os.mkdir(self.__cache)
            try:
                video=self.__youtube.streams.get_by_itag(self.GetMaxRes())
                video.download(output_path=self.__cache)

                audio=self.__youtube.streams.get_by_itag(251)
                audio.download(output_path=self.__cache)

                self.CombineAudioVideoFiles(self.GetFileName(), pathForSaving)
            except Exception:
                return "Server error, try again"
            finally:
                shutil.rmtree(self.__cache)

            return f"Video downloaded in {pathForSaving}"
        return "Incorrect link or server error"