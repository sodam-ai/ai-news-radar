@echo off
chcp 65001 >nul 2>&1
title AI News Radar
color 0B

echo.
echo  ============================================
echo       AI News Radar - Starting...
echo  ============================================
echo.

REM === Check Python ===
where py >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py -3
    goto :found_python
)
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
    goto :found_python
)

echo  [ERROR] Python is not installed.
echo.
echo  Please run "install_and_run.bat" first,
echo  or install Python from https://python.org
echo.
pause
exit /b 1

:found_python
echo  [OK] Python found: %PYTHON_CMD%

REM === Check .env ===
if not exist ".env" (
    if exist ".env.example" (
        echo.
        echo  [NOTICE] .env file not found.
        echo  Copying .env.example to .env...
        copy ".env.example" ".env" >nul
        echo.
        echo  !! IMPORTANT !!
        echo  Open ".env" with Notepad and add your API key:
        echo    GEMINI_API_KEY=your_key_here
        echo.
        echo  Get a free key at: https://aistudio.google.com/apikey
        echo.
        notepad ".env"
        echo  After saving .env, press any key to continue...
        pause >nul
    )
)

REM === Install dependencies if needed ===
if not exist ".venv" (
    echo.
    echo  [SETUP] Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM === Activate venv ===
call .venv\Scripts\activate.bat

REM === Install requirements if needed ===
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [SETUP] Installing dependencies (first run only)...
    echo  This may take 2-3 minutes...
    echo.
    pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to install dependencies.
        echo  Try running: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo  [OK] Dependencies installed!
)

REM === Create data directory ===
if not exist "data" mkdir data

REM === Start the app ===
echo.
echo  ============================================
echo   Starting AI News Radar on port 6601...
echo   Open your browser: http://localhost:6601
echo  ============================================
echo.
echo   Press Ctrl+C to stop.
echo.

streamlit run app.py --server.port 6601 --server.headless true --theme.base dark

pause
