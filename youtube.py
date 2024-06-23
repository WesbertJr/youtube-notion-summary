from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube
import requests
import json


class YoutubeData:
    def __init__(self, video_id, author, title, url, thumbnail, transcript):
        self.video_id = video_id
        self.author = author
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
        self.transcript = transcript


def formatLink(url):
    link = url.split('=')
    video_id = link[1]
    return video_id

# https://www.youtube.com/watch?v=8R-cetf_sZ4


def call_youtube(link, id):
    yt = YouTube(link)  # Create Youtube Object..

    # call the function
    video_subtitles = YouTubeTranscriptApi.get_transcript(id)
    # print(transcript)
    formatter = TextFormatter()
    # .format_transcript(transcript) turns the transcript into a JSON string.
    transcript = formatter.format_transcript(video_subtitles)
    data = YoutubeData(video_id, yt.author, yt.title, yt.embed_url, yt.thumbnail_url, transcript)

    # Define Video Details
    print("Title : ", data.title)
    print("URL : ", data.url)
    print("Author : ", data.author)
    print("Thumbnail : ", data.thumbnail)
    # print("Transcript : ", data.transcript)
    return data


user_input = "https://www.youtube.com/watch?v=8R-cetf_sZ4"
video_id = formatLink(user_input)

call_youtube(user_input, video_id)
