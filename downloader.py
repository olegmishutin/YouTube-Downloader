import os
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

cachePath="cache"


def GetFilename():
    file=os.path.basename(os.listdir(cachePath)[0])
    fileName=os.path.splitext(file)[0]

    return fileName


def CombineAudioVideoFiles(filename: str, pathToCombine: str):
    videoClip=VideoFileClip(f"{cachePath}/{filename}.mp4")
    audioClip=AudioFileClip(f"{cachePath}/{filename}.webm")

    try:
        videoClip.audio=CompositeAudioClip([audioClip])
        videoClip.write_videofile(f"{pathToCombine}/{filename}.mp4",
                                  temp_audiofile=f"{cachePath}/Cache.mp3")
    finally:
        shutil.rmtree(cachePath)


def DefineMaxResolution(youtube):
    resolutionCodec={"1080p": 137, "720p": 136, "480p": 135, "360p": 134,
                     "240p": 133, "144p": 166}

    for resolution in resolutionCodec:
        filter=youtube.streams.filter(file_extension='mp4', res=resolution,
                                      audio_codec=None).itag_index

        if resolutionCodec.get(resolution) in filter.keys():
            return resolutionCodec.get(resolution)


def Download(source: str, pathForSaving: str):
    try:
        youtube=YouTube(source)
    except Exception:
        return ""

    if not os.path.isdir(cachePath):
        os.mkdir(cachePath)

    try:
        downloader=youtube.streams.get_by_itag(DefineMaxResolution(youtube))
        downloader.download(output_path=cachePath)

        downloader=youtube.streams.get_by_itag(251)
        downloader.download(output_path=cachePath)
    except (Exception, KeyboardInterrupt):
        shutil.rmtree(cachePath)
        return "Server error, try again"

    CombineAudioVideoFiles(GetFilename(), pathForSaving)
    return f"Video downloaded in {pathForSaving}"