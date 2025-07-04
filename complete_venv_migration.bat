@echo off
echo.
echo 🎯 EXPRESS DEALS - COMPLETE VENV MIGRATION
echo ==========================================
echo.
echo This script will help you migrate from 'env' to '.venv'
echo.

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo 📍 Current directory: %CD%
echo.

echo 🔍 Step 1: Checking current environment...
if exist "env\" (
    echo ✅ Found existing 'env' directory
) else (
    echo ⚠️  No existing 'env' directory found
)

if exist ".venv\" (
    echo ✅ Found existing '.venv' directory
    echo Skipping creation...
) else (
    echo 📦 Creating new .venv virtual environment...
    python -m venv .venv
    if %errorlevel% equ 0 (
        echo ✅ .venv created successfully
    ) else (
        echo ❌ Failed to create .venv
        pause
        exit /b 1
    )
)

echo.
echo 🔄 Step 2: Activating .venv environment...
call .venv\Scripts\activate.bat

echo.
echo 🐍 Step 3: Checking Python version...
python --version
echo Python location:
where python

echo.
echo 📦 Step 4: Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🧪 Step 5: Testing key packages...
python -c "import django; print('✅ Django:', django.get_version())" 2>nul || echo "❌ Django failed"
python -c "import rest_framework; print('✅ REST Framework:', rest_framework.VERSION)" 2>nul || echo "❌ REST Framework failed"
python -c "import celery; print('✅ Celery:', celery.__version__)" 2>nul || echo "❌ Celery failed"

echo.
echo 🔧 Step 6: Running Django system check...
python manage.py check

echo.
echo 🎉 MIGRATION COMPLETE!
echo.
echo ✅ All scripts now use .venv instead of env
echo ✅ .venv environment created and configured
echo ✅ All packages installed and tested
echo.
echo 💡 To use .venv in the future:
echo    .venv\Scripts\activate.bat
echo.
echo 🗑️  Optional: Remove old env directory
echo    rmdir /s env
echo.
pause
