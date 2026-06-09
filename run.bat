@echo off
setlocal enabledelayedexpansion

echo.
echo 🚀 Database Query Optimizer - Starting
echo ========================================
echo.

REM Check Docker
echo [1/4] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker found

REM Start PostgreSQL
echo [2/4] Starting PostgreSQL container...
docker-compose up -d
timeout /t 5 /nobreak

REM Wait for database
echo [3/4] Waiting for database to be ready...
setlocal enabledelayedexpansion
set /a count=0
:wait_loop
docker-compose exec -T postgres pg_isready -U banking_user >nul 2>&1
if errorlevel 1 (
    set /a count+=1
    if !count! gtr 30 (
        echo ❌ Database failed to start
        pause
        exit /b 1
    )
    timeout /t 1 /nobreak
    goto wait_loop
)
echo ✅ Database is ready

REM Install Python dependencies
echo [4/4] Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt
cd ..
echo ✅ Dependencies installed

REM Check for .env file
if not exist "backend\.env" (
    echo.
    echo ⚠️  WARNING: .env file not found
    echo Please edit backend\.env and add your ANTHROPIC_API_KEY
    echo.
    pause
)

REM Start Flask app
echo.
echo ✨ Starting Flask application...
echo 📱 Dashboard will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py
pause
