from typing import Union
from fastapi import FastAPI
from methods import *

app = FastAPI()


@app.get("/")
async def read_root():
    messasge = "Application is running...."
    return messasge


@app.post("/youtube/data")
async def get_ytData(obj: YoutubeLink):
    provided = obj.link
    data = start(provided)

    return data

