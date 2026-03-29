@echo off
chcp 65001 >nul 2>&1
title AI News Radar - Desktop Mode
color 0B

echo.
echo  ============================================
echo   AI News Radar - Desktop Mode
echo  ============================================
echo.

REM === Check venv ===
if not exist ".venv\Scripts\activate.bat" (
    echo  [ERROR] Please run "install_and_run.bat" first!
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

REM === Check pywebview ===
pip show pywebview >nul 2>&1
if %errorlevel% neq 0 (
    echo  [SETUP] Installing desktop mode dependencies...
    pip install pywebview pystray plyer --quiet
)

REM === Launch desktop mode ===
echo  Starting desktop app...
python launcher.py

pause
