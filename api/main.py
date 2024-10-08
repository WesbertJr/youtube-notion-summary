from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube
import requests
import json
from pydantic import BaseModel
import os
from openai import OpenAI

os.environ.get('OPENAI_API_KEY')
os.environ.get('DATABASE_ID')
os.environ.get('NOTION_TOKEN')


class YoutubeLink(BaseModel):
    link: str


class YoutubeInfo:
    def __init__(self, video_id, author, title, url, thumbnail, transcript):
        self.video_id = video_id
        self.author = author
        self.title = title
        self.url = url
        self.thumbnail = thumbnail
        self.transcript = transcript


class ChatGPTInfo:
    def __init__(self, prompt, gpt_primary_res , gpt_secondary_res ):
        self.prompt = prompt
        self.gpt_primary_res = gpt_primary_res
        self.gpt_secondary_res  = gpt_secondary_res


class NotionInfo:
    def __init__(self, notion_token, database_id, status):
        self.notion_token = notion_token
        self.database_id = database_id
        self.status = status


class FastApiData:
    def __init__(self, youtube, chatgpt, notion):
        self.youtube = youtube
        self.chatgpt = chatgpt
        self.notion = notion


def notion_api(tk, db_id, yt, gpt):
    token = tk
    database = db_id
    youtubeAPI = yt
    gptAPI = gpt
    url_endpoint = "https://api.notion.com/v1/pages"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    payload = get_payload(database, youtubeAPI, gptAPI)
    response = requests.request("POST", url_endpoint, headers=headers, data=payload)
    print("Notion Database_ID: " + database)
    print(f"Notion Response: {response.status_code}")
    data = NotionInfo(token, database, response.status_code)

    return data


def get_payload(d, yt_api, res):
    data = json.dumps({
        "parent": {
            "type": "database_id",
            "database_id": d
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": yt_api.title
                        }
                    }
                ]
            },
            "URL": {
                "url": yt_api.url
            },
            "Author": {
                "rich_text": [
                    {
                        "text": {
                            "content": yt_api.author
                        }
                    }
                ]
            },
            "Thumbnail": {
                "rich_text": [
                    {
                        "text": {
                            "content": yt_api.thumbnail
                        }
                    }
                ]
            },
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": res.gpt_primary_res}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": res.gpt_secondary_res}}]
                }
            }

        ],
        "cover": {
            "type": "external",
            "external": {
                "url": yt_api.thumbnail
            }
        },
        "icon": {
            "external": {
                "url": "https://em-content.zobj.net/source/apple/354/large-red-square_1f7e5.png"
            }
        }
    })

    return data


def chatgpt_api(x, y):
    content = get_json(x, y.transcript)
    client = OpenAI()
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=content)
    primary = chat.choices[0].message.content
    secondary = ""
    content.append({"role": "assistant", "content": primary})
    num_reply = len(primary)
    if num_reply > 2000:
        val = num_reply - 2000
        result = primary[:-val]
        secondary = "[---REMOVE SPACE HERE ---]" + primary[len(result):]
        primary = result

    data = ChatGPTInfo(x, primary, secondary)
    print("Chat GPT Prompt: " + data.prompt)
    print("Response: " + data.gpt_primary_res + data.gpt_secondary_res)
    return data


def get_json(prompt, data):
    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": data
        }
    ]

    return messages


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
    data = YoutubeInfo(id, yt.author, yt.title, yt.embed_url, yt.thumbnail_url, transcript)

    # Define Video Details
    # print("Video Id : ", data.video_id)
    # print("Title : ", data.title)
    # print("URL : ", data.url)
    # print("Author : ", data.author)
    # print("Thumbnail : ", data.thumbnail)
    # print("Transcript : ", data.transcript)
    return data


def start(url):
    PROMPT = "Take on the role of a seasoned writer and summarize the following. Response should include A Title, " \
             "5 sections, a title for each section, a paragraph summary for each section, bullet points, " \
             "and 1 quotation for each section.\n Video Title:\n; Section 1:\n; Summary:\n; 3 bullet points:\n " \
             "\nQuotation: "
    user_input = url
    gpt_prompt = PROMPT
    NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
    DATABASE_ID = os.environ.get('DATABASE_ID')

    # redundant logic can simplify by improving class definitions
    youtube_obj = youtube_api(user_input)
    chatgpt_obj = chatgpt_api(gpt_prompt, youtube_obj)
    notion_obj = notion_api(NOTION_TOKEN, DATABASE_ID, youtube_obj, chatgpt_obj)

    data = FastApiData(youtube_obj, chatgpt_obj, notion_obj)

    return data


app = FastAPI()


@app.get("/")
async def read_root():
    message = "Application is running...."
    return message


@app.post("/youtube")
async def read_root(item_id: str):
    url = "https://www.youtube.com/watch?v=" + item_id
    data = start(url)
    return "updated"

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    url = "https://www.youtube.com/watch?v=" + item_id
    data = start(url)
    return "done"
