@echo off
REM Module Mind - Whisper Environment Setup Script for Windows
REM This script automates the setup of the Python environment for transcription

echo ===========================================
echo Module Mind - Whisper Environment Setup
echo ===========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Check FFmpeg
echo.
echo Checking FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] FFmpeg not found
    echo.
    echo Please install FFmpeg:
    echo   1. Download from https://ffmpeg.org/download.html
    echo   2. Or use: winget install ffmpeg
    echo   3. Make sure it's added to your PATH
    pause
    exit /b 1
)
echo [OK] FFmpeg is installed

REM Check if virtual environment exists
echo.
echo Setting up virtual environment...
if exist "whisper_env" (
    echo [WARNING] Virtual environment 'whisper_env' already exists
    set /p DELETE="Do you want to delete and recreate it? (y/n): "
    if /i "%DELETE%"=="y" (
        rmdir /s /q whisper_env
        echo [OK] Removed existing environment
    ) else (
        echo [OK] Using existing environment
        call whisper_env\Scripts\activate.bat
        echo [OK] Environment activated
        goto :end
    )
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv whisper_env
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created

REM Activate virtual environment
echo Activating virtual environment...
call whisper_env\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded

REM Install requirements
echo.
echo Installing requirements (this may take several minutes)...
if exist "config\requirements.txt" (
    pip install -r config\requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
    echo [OK] Requirements installed
) else (
    echo [ERROR] requirements.txt not found at config\requirements.txt
    pause
    exit /b 1
)

REM Test whisper installation
echo.
echo Testing Whisper installation...
python -c "from faster_whisper import WhisperModel; print('Whisper test successful')" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Whisper is working correctly
) else (
    echo [WARNING] Primary Whisper test failed, trying alternative...
    python -c "import whisper; print('Alternative whisper import successful')" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Alternative Whisper module is working
    ) else (
        echo [ERROR] Whisper installation failed
        pause
        exit /b 1
    )
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating default .env file...
    (
        echo # Whisper Configuration
        echo WHISPER_MODEL=base
        echo WHISPER_CACHE_DIR=~/.cache/whisper
        echo WHISPER_VERBOSE=false
    ) > .env
    echo [OK] .env file created with defaults
)

:end
echo.
echo ===========================================
echo Setup completed successfully!
echo ===========================================
echo.
echo To use the transcription environment:
echo   1. Activate: whisper_env\Scripts\activate.bat
echo   2. Run transcription: python transcribe_lecture.py video_file
echo   3. Deactivate when done: deactivate
echo.
echo For more information, see WHISPER_SETUP.md
echo.
pause