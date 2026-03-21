
# Government Scheme Voice Agent

This project contains an interactive voice AI agent built with LiveKit and React. It helps citizens understand government schemes using voice interaction.

The application consists of three main components:
1. **Token Server (FastAPI)**: Hands out secure Access Tokens to connect to the LiveKit room.
2. **AI Agent Worker (Python)**: The actual brain (using OpenAI and Sarvam) that sits in the room and converses with users.
3. **Frontend User Interface (React)**: The web UI for the user to start a call and interact with the agent.

## Prerequisites

- Python 3.9+
- Node.js 16+
- [LiveKit Cloud](https://cloud.livekit.io/) account (for WebSocket URL, API Key, and Secret)
- OpenAI API Key
- Sarvam API Key

## Setup & Configuration

### 1. Backend Environment Setup
Create a .env file in the root directory and add:
\\\env
LIVEKIT_URL=wss://<YOUR-LIVEKIT-PROJECT-URL>.livekit.cloud
LIVEKIT_API_KEY=<YOUR-API-KEY>
LIVEKIT_API_SECRET=<YOUR-API-SECRET>
OPENAI_API_KEY=<YOUR-OPENAI-API-KEY>
SARVAM_API_KEY=<YOUR-SARVAM-API-KEY>
\\\

### 2. Frontend Environment Setup
In the livekit-frontend/.env file:
\\\env
REACT_APP_LIVEKIT_WS_URL=wss://<YOUR-LIVEKIT-PROJECT-URL>.livekit.cloud
REACT_APP_TOKEN_SERVER_URL=http://localhost:8000/token?
\\\

### 3. Install Dependencies
**Backend:**
\\\ash
# Create and activate your virtual environment
python -m venv .venv
.venv\Scripts\activate
# Install requirements
pip install -r requirement.txt
\\\

**Frontend:**
\\\ash
cd livekit-frontend
npm install
\\\

---

## How to Run

You will need **three separate terminals** running simultaneously to operate the entire application locally.

### Terminal 1: Token Server
From the root directory with your virtual environment active:
\\\ash
python main.py
\\\
*(Starts FastAPI token server on http://localhost:8000)*

### Terminal 2: AI Agent Worker
From the root directory with your virtual environment active:
\\\ash
python scheme_awareness_agent.py dev
\\\
*(Waits in the background for someone to call via LiveKit)*

### Terminal 3: React Frontend
\\\ash
cd livekit-frontend
npm start
\\\
*(Starts client UI on http://localhost:3000)*

## Usage
Once all three processes are running:
1. Open http://localhost:3000 in your browser.
2. Click **Start Call**.
3. You will connect to the room, the Python Agent will join, and you can begin having a conversation automatically!

