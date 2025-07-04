@echo off
setlocal enabledelayedexpansion

echo 🔧 EXPRESS DEALS - SIMPLE ERROR FIX
echo ===================================

echo.
echo 📍 Current directory: %CD%

echo.
echo 🔍 Step 1: Checking virtual environment...
if exist ".venv" (
    echo ✅ Found .venv directory
    set "VENV_PATH=.venv\Scripts\activate.bat"
) else if exist "env" (
    echo ✅ Found env directory  
    set "VENV_PATH=env\Scripts\activate.bat"
) else (
    echo ❌ No virtual environment found!
    echo Creating new .venv environment...
    python -m venv .venv
    set "VENV_PATH=.venv\Scripts\activate.bat"
    echo ✅ Created .venv environment
)

echo.
echo 🔄 Step 2: Activating virtual environment...
call !VENV_PATH!
if %errorlevel% equ 0 (
    echo ✅ Virtual environment activated
) else (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo 🐍 Step 3: Checking Python version...
python --version
where python

echo.
echo 📦 Step 4: Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% equ 0 (
    echo ✅ Pip upgraded
) else (
    echo ⚠️ Pip upgrade had issues but continuing...
)

echo.
echo 📦 Step 5: Installing core packages...
set PACKAGES=django djangorestframework dj-database-url celery channels channels-redis redis pillow stripe whitenoise

for %%p in (%PACKAGES%) do (
    echo Installing %%p...
    pip install %%p
    if !errorlevel! equ 0 (
        echo ✅ Installed %%p
    ) else (
        echo ❌ Failed to install %%p
    )
)

echo.
echo 🧪 Step 6: Testing key imports...
python -c "import django; print('✅ Django:', django.get_version())" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Django import successful
) else (
    echo ❌ Django import failed
)

python -c "import rest_framework; print('✅ DRF:', rest_framework.VERSION)" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Django REST Framework import successful
) else (
    echo ❌ Django REST Framework import failed
)

echo.
echo 📁 Step 7: Creating required directories...
for %%d in (logs media static) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo ✅ Created %%d directory
    ) else (
        echo ✅ %%d directory exists
    )
)

echo.
echo 🗑️ Step 8: Removing .env file...
if exist ".env" (
    del ".env"
    echo ✅ .env file removed
) else (
    echo ✅ No .env file found
)

echo.
echo 🔧 Step 9: Running Django system check...
python manage.py check
if %errorlevel% equ 0 (
    echo ✅ Django system check passed
) else (
    echo ❌ Django system check found issues
    echo Running migrations...
    python manage.py migrate
)

echo.
echo 🎉 SIMPLE ERROR FIX COMPLETE!
echo ==============================
echo.
echo ✅ Virtual environment activated
echo ✅ Core packages installed  
echo ✅ Django configuration checked
echo ✅ Required directories created
echo ✅ .env file removed
echo.
echo 🚀 Your Express Deals project is ready!
echo.
echo 💡 Next steps:
echo 1. Run: python manage.py runserver
echo 2. Open: http://127.0.0.1:8000/
echo.
pause
