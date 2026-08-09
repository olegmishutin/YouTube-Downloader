import os

from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip
from pytubefix import YouTube


class Downloader:
    def __init__(self):
        self.videoPath = ""
        self.video = None
        self.cacheFiles = ("videoCache.mp4", "audioCache.mp3")
        self.codecs = {
            "2160p": (266, 305, 313, 315, 337, 401, 701),
            "1440p": (264, 271, 308, 336, 304, 400, 700),
            "1080p": (137, 248, 299, 303, 335, 399, 699),
            "720p": (136, 247, 298, 302, 334, 398, 698),
            "480p": (135, 244, 333, 397, 697),
            "360p": (134, 243, 332, 396, 696),
            "240p": (133, 242, 331, 395, 695),
            "144p": (160, 278, 330, 394, 694),
        }

    def GetVideoInfo(self, source: str) -> str:
        try:
            self.video = YouTube(source, use_oauth=True, allow_oauth_cache=True)

            for invalidCharacter in ("\\", "/", ":", "*", "?", '"', "<", ">", "|"):
                self.video.title = self.video.title.replace(invalidCharacter, " ")
            self.video.title = " ".join(self.video.title.split())

            return f"Author: {self.video.author}<br>Title: {self.video.title}"
        except Exception:  # noqa: BLE001
            self.video = None
            return "Incorrect link or server error" if source else ""

    def GetVideoItag(
        self, progressive=False, fileExtension: str | None = None, resolution=""
    ) -> tuple:
        return tuple(
            self.video.streams.filter( # type: ignore
                progressive=progressive, file_extension=fileExtension, res=resolution
            ).itag_index.keys()
        )

    def GetVideoResolutions(self) -> list:
        availableResolutions = []

        if self.video:
            for resolution in self.codecs:
                for codec in self.codecs.get(resolution): # type: ignore
                    if codec in self.GetVideoItag(resolution=resolution):
                        availableResolutions.append(resolution)
                        break

        return availableResolutions

    def CombineAudioVideoFiles(self) -> None:
        videoClip = VideoFileClip(self.cacheFiles[0])
        videoClip.audio = CompositeAudioClip([AudioFileClip(self.cacheFiles[1])]) # type: ignore
        videoClip.write_videofile(
            self.videoPath,
            temp_audiofile="tempAudioFile.mp3",
            preset='ultrafast',
            threads=2,
        )

    def DownloadVideo(self, source: str, pathForSaving: str, resolution: str) -> str:
        if self.video:
            try:
                progressiveDownload = self.GetVideoItag(
                    progressive=True, fileExtension="mp4", resolution=resolution
                )
                self.videoPath = f"{pathForSaving}/{self.video.title}.mp4"

                if progressiveDownload:
                    self.video.streams.get_by_itag(progressiveDownload[0]).download( # type: ignore
                        filename=self.videoPath
                    )
                else:
                    self.video.streams.get_by_itag(
                        self.GetVideoItag(resolution=resolution)[0]
                    ).download(filename=self.cacheFiles[0]) # type: ignore

                    self.video.streams.get_by_itag(251).download( # type: ignore
                        filename=self.cacheFiles[1]
                    )
                    self.CombineAudioVideoFiles()
            except Exception:  # noqa: BLE001
                return "Server error, try again"
            finally:
                if not progressiveDownload: # type: ignore
                    for cacheFile in self.cacheFiles:
                        os.remove(f"{os.getcwd()}/{cacheFile}")

            return f"Video downloaded in {pathForSaving}"
        return "Incorrect link or server error"
