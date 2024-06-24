import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "sk-proj-lVvZJDBYciMMPlJIE6d5T3BlbkFJaZ1IqtlHu263kiHbpLnZ"
client = OpenAI()


def chatgpt_api(yt):
    content = get_message(yt)
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=content)
    reply = chat.choices[0].message.content
    reply_split = ""
    content.append({"role": "assistant", "content": reply})
    num_reply = len(reply)

    if num_reply > 2000:
        val = num_reply - 2000
        result = reply[:-val]
        reply_split = reply[len(result):]
        reply = result


def get_message(yt):
    messages = [
        {
            "role": "system",
            "content": "Take on the role of a seasoned writer and summarize the following. Response should include A Title, 5 sections, a title for each section, a paragraph summary for each section, bullet points, and 1 quotation for each section.\n Video Title:\n; Section 1:\n; Summary:\n; 3 bullet points:\n \nQuotation:"
        },
        {
            "role": "user",
            "content": yt.transcript
        }
    ]

    return messages
