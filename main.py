from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

rootPath = "/api"

app = FastAPI(root_path=rootPath)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, hx_request: Optional[str] = Header(None)):
    films = [
        {"name": "Blade Runner", "director": "Ridley Scott"},
        {"name": "Pulp Fiction", "director": "Quentin Tarantino"},
        {"name": "Mulholland Drive", "director": "David Lynch"},
    ]
    context = {"request": request, "films": films, "rootPath": rootPath}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)
