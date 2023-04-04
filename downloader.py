import os
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Downloader():
    def __init__(self, cachePathName: str):
        self.cachePath=cachePathName
        self.youtube=None

    def GetVideoInfo(self, source: str):
        try:
            self.youtube=YouTube(source)

            author=self.youtube.author
            title=self.youtube.title

            return f"Author: {author}; Title: {title}"
        except Exception:
            self.youtube=None

            return "Incorrect link or server error" if source else ""

    def GetFilename(self):
        file=os.path.basename(os.listdir(self.cachePath)[0])
        fileName=os.path.splitext(file)[0]

        return fileName

    def CombineAudioVideoFiles(self, filename: str, pathToCombine: str):
        videoClip=VideoFileClip(f"{self.cachePath}/{filename}.mp4")
        audioClip=AudioFileClip(f"{self.cachePath}/{filename}.webm")

        try:
            videoClip.audio=CompositeAudioClip([audioClip])
            videoClip.write_videofile(f"{pathToCombine}/{filename}.mp4",
                                      temp_audiofile=\
                                          f"{self.cachePath}/Cache.mp3")
        finally:
            shutil.rmtree(self.cachePath)

    def GetMaxResolution(self):
        resolutionCodec={"1080p": 137, "720p": 136, "480p": 135, "360p": 134,
                         "240p": 133, "144p": 166}

        for resolution in resolutionCodec:
            filter=self.youtube.streams.filter(file_extension='mp4',
                                               audio_codec=None,
                                               res=resolution).itag_index

            if resolutionCodec.get(resolution) in filter.keys():
                return resolutionCodec.get(resolution)

    def DownloadVideo(self, source: str, pathForSaving: str):
        if self.youtube:
            if not os.path.isdir(self.cachePath):
                os.mkdir(self.cachePath)

            try:
                downloader=\
                    self.youtube.streams.get_by_itag(self.GetMaxResolution())
                downloader.download(output_path=self.cachePath)

                downloader=self.youtube.streams.get_by_itag(251)
                downloader.download(output_path=self.cachePath)
            except (Exception, KeyboardInterrupt):
                shutil.rmtree(self.cachePath)

                return "Server error, try again"

            self.CombineAudioVideoFiles(self.GetFilename(), pathForSaving)
            return f"Video downloaded in {pathForSaving}"
        else:
            return "Incorrect link"
