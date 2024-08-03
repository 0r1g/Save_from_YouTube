from fastapi import FastAPI, HTTPException, Body, Query, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
from typing import Annotated
from sqlalchemy.orm import Session
from db.crud import get_track_by_title
from utils.download_video import download_youtube_audio
from utils.check_url import check_url
from db import crud, models, schemas
from db.database import engine, get_db
from auth.auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Save Audio from YouTube')

app.mount('/static', StaticFiles(directory="tracks"), "static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": 200}


@app.get("/tracks", response_class=HTMLResponse)
def get_all_tracks(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "tracks": crud.get_all_tracks(db)})


@app.get("/tracks/{track_id}", response_class=HTMLResponse)
def get_track(request: Request, track_id: str, db: Session = Depends(get_db)):
    track = get_track_by_title(db=db, title=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Not Found")
    return templates.TemplateResponse("track.html", {"request": request, "name": track_id})


@app.post("/upload")
def upload_audio(
    link: Annotated[HttpUrl, Body(example="https://www.youtube.com/watch?v=dQw4w9WgXcQ")],
    db: Session = Depends(get_db),
):
    if not check_url(str(link)):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        track_title = download_youtube_audio(str(link))
    except BaseException:
        raise HTTPException(status_code=404, detail="Not Found")

    track_data = schemas.TrackCreate(title=f"{track_title}")
    if not get_track_by_title(db=db, title=track_title):
        crud.create_track(db=db, track=track_data)

    return {"message": "Valid YouTube URL", "url": link, "title": track_title}


@app.get("/download", response_class=FileResponse)
def download_audio(track_name: Annotated[str, Query()]):
    return f"tracks/{track_name}.mp3"
