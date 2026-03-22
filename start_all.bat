@echo off
echo Starting Government Scheme Voice Agent Services...

echo [1/3] Starting FastAPI Token Server...
start "Token Server" cmd /k "call .venv\Scripts\activate.bat && python main.py"

echo [2/3] Starting AI Agent Worker...
start "Agent Worker" cmd /k "call .venv\Scripts\activate.bat && python scheme_awareness_agent.py dev"

echo [3/3] Starting React Frontend...
start "React Frontend" cmd /k "cd livekit-frontend && npm start"

echo.
echo All services have been launched in separate windows!
echo You can now open http://localhost:3000 in your browser.
pause
