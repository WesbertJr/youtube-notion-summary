from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube


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
    formatted_id = link[1]
    return formatted_id


def youtube_api(link):
    id = formatLink(link)
    yt = YouTube(link)  # Create Youtube Object..

    # call the function
    video_subtitles = YouTubeTranscriptApi.get_transcript(id)
    # print(transcript)
    formatter = TextFormatter()
    # .format_transcript(transcript) turns the transcript into a JSON string.
    transcript = formatter.format_transcript(video_subtitles)
    data = YoutubeData(id, yt.author, yt.title, yt.embed_url, yt.thumbnail_url, transcript)

    # Define Video Details
    print("Video Id : ", id)
    print("Title : ", data.title)
    print("URL : ", data.url)
    print("Author : ", data.author)
    print("Thumbnail : ", data.thumbnail)
    # print("Transcript : ", data.transcript)
    return data


user_input = "https://www.youtube.com/watch?v=8R-cetf_sZ4"

youtube_api(user_input)
