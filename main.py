import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from livekit.api import AccessToken, VideoGrants
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/token")
def get_token(room: str, user: str):
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if not api_key or not api_secret:
        return {"error": "Server misconfiguration. LIVEKIT_API_KEY or LIVEKIT_API_SECRET not set."}
        
    grant = VideoGrants(room_join=True, room=room, can_publish=True, can_subscribe=True)
    access_token = AccessToken(api_key, api_secret)
    access_token.with_identity(user)
    access_token.with_grants(grant)
    
    return {"token": access_token.to_jwt()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

