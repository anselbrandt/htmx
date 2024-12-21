from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transmission_rpc import Client
from dotenv import load_dotenv
import os

load_dotenv()

TRANSMISSION_USERNAME = os.getenv("TRANSMISSION_USERNAME")
TRANSMISSION_PASSWORD = os.getenv("TRANSMISSION_PASSWORD")

rootPath = "/api"

app = FastAPI(root_path=rootPath)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

torrentClient = Client(
    host="raspberrypi.anselbrandt.net",
    port=9091,
    username=TRANSMISSION_USERNAME,
    password=TRANSMISSION_PASSWORD,
)


def style(status):
    if status == "seeding":
        return "flex w-3 h-3 me-3 bg-green-500 rounded-full"
    if status == "downloading":
        return "flex w-3 h-3 me-3 bg-blue-600 rounded-full"
    else:
        return "flex w-3 h-3 me-3 bg-gray-200 rounded-full"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, hx_request: Optional[str] = Header(None)):
    torrents = torrentClient.get_torrents()
    context = {
        "request": request,
        "rootPath": rootPath,
        "torrents": torrents,
        "style": style,
    }
    return templates.TemplateResponse("index.html", context)


class MagnetLink(BaseModel):
    url: str


@app.post("/add")
async def add(magnetlink: MagnetLink):
    try:
        url = magnetlink.url
        res = torrentClient.add_torrent(url)
        return res.name
    except Exception as error:
        print(str(error))
        return str(error)


@app.delete("/delete/{id}")
async def delete(id):
    print(id)
    try:
        torrentClient.remove_torrent(id, delete_data=True)
    except Exception as error:
        print(str(error))
        return str(error)


@app.get("/get")
async def get():
    torrents = torrentClient.get_torrents()
    return torrents
