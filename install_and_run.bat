@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title AI News Radar - Setup
color 0B

echo.
echo  ============================================================
echo       AI News Radar - One-Click Setup
echo  ============================================================
echo.
echo   This script will:
echo     1. Check if Python is installed
echo     2. Create a virtual environment
echo     3. Install all dependencies
echo     4. Help you set up your API key
echo     5. Launch the app
echo.
echo   Press any key to begin...
pause >nul
echo.

REM === Step 1: Check Python ===
echo  [1/5] Checking Python installation...

where py >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py -3
    for /f "tokens=*" %%i in ('py -3 --version 2^>^&1') do set PYTHON_VER=%%i
    echo         Found: !PYTHON_VER!
    goto :python_ok
)

where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo         Found: !PYTHON_VER!
    goto :python_ok
)

echo.
echo  [ERROR] Python is not installed!
echo.
echo  ===== HOW TO INSTALL PYTHON =====
echo.
echo   1. Open this link in your browser:
echo      https://www.python.org/downloads/
echo.
echo   2. Click the big yellow "Download Python" button
echo.
echo   3. Run the downloaded file
echo.
echo   4. IMPORTANT: Check the box that says
echo      "Add Python to PATH" at the bottom!
echo.
echo   5. Click "Install Now"
echo.
echo   6. After installation, close this window
echo      and double-click this file again.
echo.
echo  ==================================
echo.
start https://www.python.org/downloads/
pause
exit /b 1

:python_ok
echo         [OK] Python is ready!
echo.

REM === Step 2: Create virtual environment ===
echo  [2/5] Setting up virtual environment...

if not exist ".venv" (
    %PYTHON_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo         [OK] Virtual environment created!
) else (
    echo         [OK] Virtual environment already exists.
)
echo.

REM === Activate venv ===
call .venv\Scripts\activate.bat

REM === Step 3: Install dependencies ===
echo  [3/5] Installing dependencies...
echo         This may take 2-3 minutes on first run...
echo.

pip install -r requirements.txt --quiet 2>nul
if %errorlevel% neq 0 (
    echo         Retrying with verbose output...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)
echo         [OK] All dependencies installed!
echo.

REM === Step 4: Setup API Key ===
echo  [4/5] Setting up API key...

if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
    ) else (
        echo GEMINI_API_KEY=your_api_key_here> .env
    )
    echo.
    echo  ===== API KEY SETUP =====
    echo.
    echo   You need a free Google Gemini API key.
    echo.
    echo   1. Opening Google AI Studio...
    echo      (If it doesn't open, go to: https://aistudio.google.com/apikey)
    echo.
    echo   2. Sign in with your Google account
    echo.
    echo   3. Click "Create API Key"
    echo.
    echo   4. Copy the key
    echo.
    echo   5. The .env file will open in Notepad.
    echo      Replace "your_api_key_here" with your key.
    echo      Save and close Notepad.
    echo.
    echo  =========================
    echo.
    start https://aistudio.google.com/apikey
    timeout /t 3 >nul
    notepad ".env"
    echo.
    echo   After saving your API key, press any key to continue...
    pause >nul
) else (
    echo         [OK] .env file already exists.
)
echo.

REM === Create data directory ===
if not exist "data" mkdir data

REM === Step 5: Launch ===
echo  [5/5] Launching AI News Radar...
echo.
echo  ============================================================
echo.
echo   AI News Radar is starting!
echo.
echo   Your browser will open automatically.
echo   If not, open: http://localhost:6601
echo.
echo   To stop: close this window or press Ctrl+C
echo.
echo  ============================================================
echo.

streamlit run app.py --server.port 6601 --server.headless true --theme.base dark --browser.gatherUsageStats false

pause
