@echo off
REM DocWeaver - Start All Services Script (Windows)
REM This script starts all three services in separate command windows

echo.
echo ========================================
echo   DocWeaver - Starting All Services
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo    Create .env with: GEMINI_API_KEY=your_key_here
    echo.
)

echo [1/3] Installing dependencies...
echo.

REM Install Python dependencies
echo   - Installing Python dependencies...
pip install -r REQUIREMENTS.txt >nul 2>&1

REM Install Node dependencies
echo   - Installing Node dependencies...
cd frontend
call npm install >nul 2>&1
cd ..

echo.
echo [2/3] Dependencies installed!
echo.
echo [3/3] Starting services...
echo.

REM Start FastAPI Backend
echo   - Starting FastAPI Backend (Port 8000)
start "DocWeaver API" cmd /k "cd clinical_orchestrator && python api.py"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start Streamlit Demo
echo   - Starting Streamlit Demo (Port 8501)
start "DocWeaver Demo" cmd /k "cd clinical_orchestrator && streamlit run app.py"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start Next.js Frontend
echo   - Starting Next.js Frontend (Port 3000)
start "DocWeaver Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   All Services Starting!
echo ========================================
echo.
echo Services will be available at:
echo   - Frontend:  http://localhost:3000
echo   - API:       http://localhost:8000
echo   - Demo:      http://localhost:8501
echo.
echo Check the new command windows for startup progress
echo.
echo To stop services, close the command windows
echo.
pause
