@echo off
title AI News Radar - Web Mode
echo.
echo  ========================================
echo   AI News Radar - Web Mode
echo  ========================================
echo.
echo  http://localhost:7429
echo.

cd /d "%~dp0"

where python >nul 2>&1
if %ERRORLEVEL%==0 (
    python -m streamlit run app.py --server.port 7429
) else (
    C:\Python313\python.exe -m streamlit run app.py --server.port 7429
)

pause
