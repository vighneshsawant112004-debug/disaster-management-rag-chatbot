@echo off
title DisasterAI - Emergency Guidance System
color 0C

echo.
echo  ============================================
echo   DisasterAI - Starting Up...
echo  ============================================
echo.

:: Store root directory
set ROOT=%~dp0

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Please install Python 3.9+
    echo  Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo  [1/6] Python found.

:: Create virtual environment if it doesn't exist
if not exist "%ROOT%venv\Scripts\python.exe" (
    echo  [2/6] Creating virtual environment...
    python -m venv "%ROOT%venv"
    if errorlevel 1 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo         Virtual environment created.
) else (
    echo  [2/6] Virtual environment already exists - skipping.
)

:: Set explicit paths to venv executables (no reliance on activate or PATH)
set VENV_PY=%ROOT%venv\Scripts\python.exe
set VENV_PIP=%ROOT%venv\Scripts\pip.exe
set VENV_ST=%ROOT%venv\Scripts\streamlit.exe

echo  [3/6] Virtual environment ready.

:: Install dependencies only if streamlit.exe is missing inside venv
if not exist "%VENV_ST%" (
    echo  [4/6] Installing dependencies (one-time only^)...
    "%VENV_PIP%" install langchain langchain-community langchain-huggingface langchain-groq faiss-cpu sentence-transformers transformers torch pypdf python-dotenv streamlit numpy --quiet
    if errorlevel 1 (
        echo  [ERROR] Dependency installation failed.
        pause
        exit /b 1
    )
    echo         Dependencies installed successfully.
) else (
    echo  [4/6] Dependencies already installed - skipping.
)

:: Check .env
if not exist "%ROOT%.env" (
    echo  [5/6] No .env found - creating from template...
    if exist "%ROOT%.env.example" (
        copy "%ROOT%.env.example" "%ROOT%.env" >nul
    ) else (
        echo GROQ_API_KEY= > "%ROOT%.env"
    )
    echo.
    echo  ============================================
    echo   ACTION REQUIRED:
    echo   Open .env and add your GROQ_API_KEY
    echo   Get one free at: https://console.groq.com
    echo  ============================================
    echo.
    pause
) else (
    echo  [5/6] .env found.
)

:: Check data folder
if not exist "%ROOT%data\" (
    mkdir "%ROOT%data"
    echo  [!] Created data\ folder - add your disaster PDF files there.
    pause
)

:: Launch app using explicit venv streamlit path
echo  [6/6] Launching DisasterAI...
echo.
echo  Open your browser at: http://localhost:8501
echo  Press Ctrl+C to stop the server.
echo.

"%VENV_ST%" run "%ROOT%streamlit\app.py" --server.port 8501 --browser.gatherUsageStats false

pause