@echo off
title Kensite Hire Dashboard
cd "%USERPROFILE%\Desktop\Web App"
echo Launching the app...
python --version >nul 2>&1 || (
    echo.
    echo Python is not installed or not on PATH.
    echo Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b
)
echo.
echo Starting Streamlit...
streamlit run streamlit_app.py
pause
