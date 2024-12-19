from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
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

templates = Jinja2Templates(directory="templates")

c = Client(
    host="raspberrypi.anselbrandt.net",
    port=9091,
    username=TRANSMISSION_USERNAME,
    password=TRANSMISSION_PASSWORD,
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, hx_request: Optional[str] = Header(None)):
    context = {"request": request, "rootPath": rootPath}
    return templates.TemplateResponse("index.html", context)


class MagnetLink(BaseModel):
    url: str


@app.post("/add")
async def magnet(magnetlink: MagnetLink):
    url = magnetlink.url
    res = c.add_torrent(url)
    print(res)

    return "success"
