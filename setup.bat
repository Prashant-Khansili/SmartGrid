@echo off
REM SmartGrid Dashboard - Quick Setup Script for Windows
REM This script automates the entire setup process

echo.
echo ========================================
echo   SmartGrid Dashboard - Setup Script
echo   Windows (PowerShell Required)
echo ========================================
echo.

REM 1. Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python found

REM 2. Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo ✅ Virtual environment already exists
) else (
    python -m venv venv
    echo ✅ Virtual environment created
)

REM 3. Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM 4. Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo ✅ pip upgraded

REM 5. Install dependencies
echo.
echo Installing dependencies (this may take 2-3 minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM 6. Verify installation
echo.
echo Verifying installation...
python -c "import streamlit; import tensorflow; import sklearn; print('✅ All packages verified!')" 2>nul
if errorlevel 1 (
    echo ⚠️  Some packages may not be installed correctly
) else (
    echo ✅ Installation verified successfully
)

REM 7. Create necessary directories
echo.
echo Creating directories...
if not exist data\raw mkdir data\raw
if not exist outputs mkdir outputs
if not exist outputs\models mkdir outputs\models
echo ✅ Directories created

REM 8. Summary
echo.
echo ========================================
echo   ✅ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Activate environment: .\venv\Scripts\Activate.ps1
echo 2. Start dashboard:     cd dashboard
echo 3. Run dashboard:       streamlit run app.py
echo 4. Open browser:        http://localhost:8501
echo.
echo For detailed instructions, see: SETUP_GUIDE.md
echo.

pause
