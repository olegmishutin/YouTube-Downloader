import os
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Downloader():
    def __init__(self):
        self.__cache="cache"
        self.__youtube=self.__streams=None

        self.__resolutionCodec={"1080p": [137, 299, 399, 699],
                                "720p": [136, 298, 398, 698],
                                "480p": [135, 397, 697],
                                "360p": [134, 396, 696],
                                "240p": [133, 395, 695],
                                "144p": [160, 394, 694]}

    def GetVideoInfo(self, source: str):
        try:
            self.__youtube=YouTube(source)

            author=self.__youtube.author
            title=self.__youtube.title

            return f"Author: {author}; Title: {title}"
        except Exception:
            self.__youtube=None

            return "Incorrect link or server error" if source else ""

    def GetVideoResolutions(self):
        availableRes=[]

        if self.__youtube:
            self.__streams=self.__youtube.streams

            for res in self.__resolutionCodec:
                filter=self.__streams.filter(file_extension='mp4',
                                             audio_codec=None,
                                             res=res).itag_index

                for codec in self.__resolutionCodec.get(res):
                    if (codec in filter.keys()) and (res not in availableRes):
                        availableRes.append(res)

        return availableRes

    def GetVideoCodec(self, res):
        filter=self.__streams.filter(file_extension='mp4',
                                     audio_codec=None,
                                     res=res).itag_index

        return list(filter.keys())[0]

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

    def DownloadVideo(self, source: str, pathForSaving: str, res: str):
        if self.__youtube:
            if os.path.isdir(self.__cache) and os.listdir(self.__cache):
                shutil.rmtree(self.__cache)

            os.mkdir(self.__cache)
            try:
                video=self.__streams.get_by_itag(self.GetVideoCodec(res))
                video.download(output_path=self.__cache)

                audio=self.__streams.get_by_itag(251)
                audio.download(output_path=self.__cache)

                self.CombineAudioVideoFiles(self.GetFileName(), pathForSaving)
            except Exception:
                return "Server error, try again"
            finally:
                shutil.rmtree(self.__cache)

            return f"Video downloaded in {pathForSaving}"
        return "Incorrect link or server error"