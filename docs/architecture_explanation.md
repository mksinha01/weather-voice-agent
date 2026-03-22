# Architecture: Connecting the Frontend and the AI Agent

In this project, the React Frontend and the Python AI Agent **do not communicate directly with each other**. Instead, they use a real-time cloud router called **LiveKit Cloud** to pass audio and data back and forth. 

Here is a detailed breakdown of how the architecture works and how the connections are established.

---

## The Three Main Components

1. **The React Frontend** (The User's Browser)
2. **The FastApi Token Server** (`main.py`)
3. **The Python Worker Agent** (`scheme_awareness_agent.py`)
4. *(External Component)*: **LiveKit Cloud** (The central meeting room)

---

## How the Connection is Made (Step-by-Step)

### Step 1: Requesting Permission (The Token)
Before the browser can connect to LiveKit, it needs permission. You cannot put your LiveKit Secret Keys in the React code because users could steal them.
* When the user clicks **"Start Call"** in React, the frontend makes an HTTP GET request to your FastAPI server (`http://localhost:8000/token?room=room_123&user=user_456`).
* The **FastAPI Server** uses your hidden `LIVEKIT_API_SECRET` to sign a JWT (JSON Web Token) that essentially says: *"This specific user is allowed to join this specific room, and they are allowed to publish and subscribe to audio."*
* The FastApi Server sends this JWT back to the React Frontend.

### Step 2: The Frontend Joins the Cloud
* The React frontend takes the Token and its websocket URL (`wss://<your-project>.livekit.cloud`) and connects to **LiveKit Cloud**.
* LiveKit verifies the token and places the user into a WebRTC "Room". 
* The user's browser starts streaming their microphone audio up to LiveKit Cloud.

### Step 3: Triggering the AI Worker
* Meanwhile, your Python Agent (`scheme_awareness_agent.py`) has been running in the background. It is authenticated as a "Worker" using your environment variables and is constantly connected to LiveKit's **Dispatch Service**.
* When LiveKit Cloud notices a new user joining an empty room, a Dispatch event is triggered.
* LiveKit Cloud pings your waiting Python Worker and hands it a "Job" for that specific room.

### Step 4: The Agent Joins the Room
* The Python script accepts the job and executes the `entrypoint` function.
* The script calls `ctx.connect()`, which formally enters the AI Agent into the exact same WebRTC Room as the user.
* It starts the `AgentSession()`, which mounts your specific logic (OpenAI, Sarvam STT, Sarvam TTS) to the room.

### Step 5: The Real-Time Conversation
Now that both the User and the Agent are inside the LiveKit Cloud Room, real-time communication happens seamlessly via LiveKit's routing:

1. **User Speaks:** The User's browser sends microphone audio to LiveKit Cloud $\rightarrow$ LiveKit routes it down to the Python Worker.
2. **Agent Listens:** The Python Worker feeds the audio into **Sarvam STT** to get text.
3. **Agent Thinks:** The text is fed to **OpenAI/gpt-4o** to generate a text response.
4. **Agent Speaks:** The text response is fed to **Sarvam TTS** to generate audio bytes.
5. **Route Back to User:** The Python worker pushes those audio bytes back up to LiveKit Cloud $\rightarrow$ LiveKit routes it to the React Frontend.
6. **Frontend Plays:** The React frontend receives the `trackSubscribed` event and plays the audio through the user's speakers.

---

## Why Use This Architecture?

### 1. Bypassing Network Restrictions
WebRTC (Real-Time Communication) requires complex port forwarding, UDP packet streaming, and NAT traversal. If your Python backend tried to send raw audio directly to the user's IP address, standard home routers and firewalls would block it. LiveKit Cloud sits in the middle on open ports (443) and handles the complex peer-to-peer networking.

### 2. High Scalability
By using the Worker/Job model, your FastAPI Token Server just hands out tickets (which uses almost no CPU). Your Python Workers handle the heavy AI lifting. If you had 100 users, LiveKit Cloud would just queue up 100 jobs, and you could spin up 50 Python instances across different servers to handle them asynchronously without them bottlenecking each other.
