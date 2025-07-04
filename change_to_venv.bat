@echo off
REM Script to change virtual environment from 'env' to '.venv'

echo 🔄 Changing virtual environment from 'env' to '.venv'
echo ================================================

REM Create new virtual environment with .venv name
echo 📦 Creating new .venv virtual environment...
python -m venv .venv

if %errorlevel% neq 0 (
    echo ❌ Failed to create .venv virtual environment
    pause
    exit /b 1
)

echo ✅ New .venv virtual environment created

REM Activate the new environment and install requirements
echo 🔄 Activating .venv and installing requirements...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo ✅ Requirements installed in .venv

REM Update .gitignore to include .venv
echo 📝 Updating .gitignore...
findstr /C:".venv" .gitignore >nul 2>&1
if %errorlevel% neq 0 (
    echo .venv/ >> .gitignore
    echo # Virtual environment >> .gitignore
)

echo ✅ .gitignore updated

echo 🎉 Virtual environment successfully changed to .venv!
echo.
echo 💡 Next steps:
echo 1. Delete the old 'env' directory: rmdir /s env
echo 2. Update any IDE/editor settings to use .venv
echo 3. Use: .venv\Scripts\activate.bat to activate environment
echo.
pause
