# Sarvam TTS MP3 Decode Fix

## Context
The Sarvam TTS provider returns MP3 audio, but LiveKit’s decoder expected WAV and threw `Invalid WAV file: missing RIFF/WAVE` errors during startup and on responses.

## What was happening
- Console runs of `scheme_awareness_agent.py` failed TTS synthesis with repeated `no audio frames were pushed for text` after WAV decode errors.
- Logs showed MP3 bytes (`0xff 0xf3 ...`) being sent to the WAV decoder, confirming a MIME/type mismatch.

## Fix applied
- Told LiveKit to treat Sarvam TTS audio as MP3:
  - API (non-streaming) response emitter now advertises `audio/mpeg` so the decoder picks the MP3 pipeline. See [.venv/Lib/site-packages/livekit/plugins/sarvam/tts.py](.venv/Lib/site-packages/livekit/plugins/sarvam/tts.py#L666-L671).
  - Streaming WebSocket emitter also declares `audio/mpeg` to match the returned frames. See [.venv/Lib/site-packages/livekit/plugins/sarvam/tts.py](.venv/Lib/site-packages/livekit/plugins/sarvam/tts.py#L706-L712).
- Removed the unsupported `encoding` kwarg from the agent’s TTS setup (it is not accepted by Sarvam TTS). See [scheme_awareness_agent.py](scheme_awareness_agent.py#L63-L67).

## Outcome
- `python scheme_awareness_agent.py console` now starts cleanly, connects STT/TTS, and no longer throws WAV decode errors. TTS audio streams as expected.

## Important caveat
- The MIME fixes live inside the virtualenv (`.venv`). If you reinstall or upgrade `livekit-plugins-sarvam`, these edits will be overwritten. For a durable fix, vendor the patched file or pin to a wheel that includes the change.

## How to run
1) Activate the project venv if not already: `& .venv\\Scripts\\Activate.ps1`
2) Run the console agent: `python scheme_awareness_agent.py console`
3) Stop with Ctrl+C when finished.
