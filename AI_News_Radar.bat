@echo off
title AI News Radar - Desktop
echo.
echo  ========================================
echo   AI News Radar - Desktop App
echo  ========================================
echo.
echo  Starting...
echo.

cd /d "%~dp0"

:: Python 자동 감지
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    python desktop.py %*
) else (
    C:\Python313\python.exe desktop.py %*
)

pause
