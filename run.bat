@echo off
echo Stopping existing servers...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo Starting Backend and Frontend...
start "Backend Server" cmd /k "cd backend && python app.py"
start "Frontend Server" cmd /k "cd frontend && npm run dev"
