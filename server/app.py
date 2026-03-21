import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from livekit import api

# Load .env so LIVEKIT_* variables are available when running uvicorn directly
load_dotenv()

# ENV: LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL (wss://...)
LK_API_KEY = os.getenv("LIVEKIT_API_KEY")
LK_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LK_URL = os.getenv("LIVEKIT_URL")

app = FastAPI(title="Scheme Awareness UI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = Path(__file__).resolve().parent.parent / "web"
app.mount("/web", StaticFiles(directory=web_dir, html=True), name="static")


@app.get("/token")
def token(room: str = "gov-schemes", name: str | None = None):
    if not (LK_API_KEY and LK_API_SECRET and LK_URL):
        raise HTTPException(status_code=500, detail="LIVEKIT credentials not configured")

    # AccessToken API expects grants to be added via add_grants(VideoGrants(...)).
    access_token = api.AccessToken(api_key=LK_API_KEY, api_secret=LK_API_SECRET)
    access_token.with_identity(name or f"user-{uuid.uuid4().hex[:6]}")
    access_token.with_grants(api.VideoGrants(room_join=True, room=room))

    return {"url": LK_URL, "token": access_token.to_jwt()}


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/ping")
def ping():
    return {"pong": True}


@app.get("/index.html")
def index_html():
    # Ensure index is reachable even if default static mount is bypassed.
    index_path = web_dir / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)


@app.get("/")
def root():
    index_path = web_dir / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)
