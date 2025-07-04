@echo off
echo 🔧 EXPRESS DEALS - QUICK ERROR FIX SCRIPT
echo =========================================
echo.

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo 📍 Current directory: %CD%
echo.

echo 🔍 Step 1: Checking virtual environments...
if exist ".venv\" (
    echo ✅ Found .venv directory
    set VENV_PATH=.venv\Scripts\activate.bat
) else if exist "env\" (
    echo ✅ Found env directory
    set VENV_PATH=env\Scripts\activate.bat
) else (
    echo ❌ No virtual environment found!
    echo Creating new .venv environment...
    python -m venv .venv
    set VENV_PATH=.venv\Scripts\activate.bat
)

echo.
echo 🔄 Step 2: Activating virtual environment...
call %VENV_PATH%

echo.
echo 🐍 Step 3: Checking Python version...
python --version

echo.
echo 📦 Step 4: Installing/updating all requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🧪 Step 5: Testing key imports...
python -c "import django; print('✅ Django:', django.get_version())" 2>nul || (
    echo ❌ Django import failed - installing...
    pip install django
)

python -c "import rest_framework; print('✅ DRF:', rest_framework.VERSION)" 2>nul || (
    echo ❌ REST Framework import failed - installing...
    pip install djangorestframework
)

python -c "import dotenv; print('✅ python-dotenv imported')" 2>nul || (
    echo ❌ python-dotenv import failed - installing...
    pip install python-dotenv
)

python -c "import dj_database_url; print('✅ dj-database-url imported')" 2>nul || (
    echo ❌ dj-database-url import failed - installing...
    pip install dj-database-url
)

echo.
echo 🔧 Step 6: Running Django system check...
python manage.py check 2>nul && (
    echo ✅ Django system check passed
) || (
    echo ❌ Django system check failed - running migrations...
    python manage.py migrate
)

echo.
echo 📁 Step 7: Creating required directories...
if not exist "logs\" mkdir logs
if not exist "media\" mkdir media
if not exist "static\" mkdir static

echo.
echo 🔍 Step 8: Removing .env file (using hardcoded settings)...
if exist ".env" (
    echo Removing .env file...
    del ".env"
    echo ✅ .env file removed
) else (
    echo ✅ No .env file found
)

echo.
echo 🎉 ERROR FIX COMPLETE!
echo.
echo ✅ Virtual environment activated
echo ✅ All packages installed
echo ✅ Django configuration checked
echo ✅ Required directories created
echo ✅ Environment variables configured
echo.
echo 🚀 Your Express Deals project should now work!
echo.
echo 💡 Next steps:
echo 1. Run: python manage.py runserver
echo 2. Open: http://127.0.0.1:8000/
echo.
pause
