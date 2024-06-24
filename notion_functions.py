import requests
import json
from pydantic import BaseModel
from methods import YoutubeData


class NotionInfo(BaseModel):
    NOTION_TOKEN: str
    DATABASE_ID: str
    YT: YoutubeData


def notion_api(tk, db_id, yt):
    token = tk
    database = db_id
    youtubeAPI = yt
    url_endpoint = "https://api.notion.com/v1/pages"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    payload = get_payload(database, youtubeAPI)
    response = requests.request("POST", url_endpoint, headers=headers, data=payload)
    print(response.text)
    return response.text


def get_payload(d, api):
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
                            "content": api.title
                        }
                    }
                ]
            },
            "URL": {
                "url": api.url
            },
            "Author": {
                "rich_text": [
                    {
                        "text": {
                            "content": api.author
                        }
                    }
                ]
            },
            "Thumbnail": {
                "rich_text": [
                    {
                        "text": {
                            "content": api.thumbnail
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
                    "rich_text": [{"type": "text", "text": {"content": api.transcript}}]
                }
            }

        ],
        "cover": {
            "type": "external",
            "external": {
                "url": api.thumbnail
            }
        }
    })

    return data

# TESTING Commands
# url = "https://api.notion.com/v1/pages"
# NOTION_TOKEN = "secret_9Lg9HixKbsIoK2c3dqMo4Ff8VdI27uN6OtcDuH5y9XF"
# DATABASE_ID = "0a36c0aeb6614f878fdfb0b9413d3182"
#
# my_id = "ssdf-test-id"
# author = "Wesbert J Edouard"
# title = "Test Title"
# my_url = "https://www.youtube.com/embed/eH5QAdnVWsc"
# thumbnail = "https://i.ytimg.com/vi/eH5QAdnVWsc/hq720.jpg"
# transcript = "Test Transcript"
#
# YT_OBJECT = YoutubeData(my_id, author, title, my_url, thumbnail, transcript)

# notion_api(NOTION_TOKEN, DATABASE_ID, YT_OBJECT)
