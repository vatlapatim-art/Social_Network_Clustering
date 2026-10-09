@echo off
echo ===================================================
echo   SOCIAL NETWORK COMMUNITY DETECTION - IMMERSIVE
echo ===================================================
echo Installing backend requirements...
python -m pip install -r requirements.txt

echo Installing frontend requirements...
cd frontend
call npm install
cd ..

echo.
echo Starting FastAPI Backend...
start cmd /k "python -m uvicorn api:app --reload --port 8000"

echo Starting Vite Frontend...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo Both servers are starting!
echo Backend API: http://localhost:8000/docs
echo Frontend UI: http://localhost:3000
echo.
echo Note: Keep this window open. Close the other windows to stop the servers.
pause
