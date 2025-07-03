@echo off
REM Express Deals Environment Setup and Verification Script
REM This script ensures the correct Python environment is activated and packages are installed

echo 🚀 Express Deals - Environment Setup and Verification
echo ================================================

REM Navigate to project directory
cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo 📍 Current directory: %CD%

REM Check if virtual environment exists
if exist "env\Scripts\activate.bat" (
    echo ✅ Virtual environment found in 'env' directory
) else (
    echo ❌ Virtual environment not found! Creating new one...
    python -m venv env
    echo ✅ New virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call env\Scripts\activate.bat

REM Check Python version
echo 🐍 Python version:
python --version

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📋 Installing requirements from requirements.txt...
pip install -r requirements.txt

REM Check specific packages
echo 🔍 Checking key package installations:

echo Checking Django...
python -c "import django; print(f'Django {django.get_version()} installed')" 2>nul && echo ✅ Django OK || echo ❌ Django FAILED

echo Checking Django REST Framework...
python -c "import rest_framework; print(f'DRF {rest_framework.VERSION} installed')" 2>nul && echo ✅ REST Framework OK || echo ❌ REST Framework FAILED

echo Checking Celery...
python -c "import celery; print(f'Celery {celery.__version__} installed')" 2>nul && echo ✅ Celery OK || echo ❌ Celery FAILED

echo Checking Channels...
python -c "import channels; print(f'Channels {channels.__version__} installed')" 2>nul && echo ✅ Channels OK || echo ❌ Channels FAILED

echo Checking Scrapy...
python -c "import scrapy; print(f'Scrapy {scrapy.__version__} installed')" 2>nul && echo ✅ Scrapy OK || echo ❌ Scrapy FAILED

REM Run Django system check
echo 🔧 Running Django system check...
python manage.py check --deploy

REM Show installed packages
echo 📦 Installed packages:
pip list | findstr -i "django celery channels scrapy rest"

echo.
echo 🎉 Environment verification complete!
echo.
echo 💡 To activate this environment in the future, run:
echo    cd "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
echo    env\Scripts\activate.bat
echo.
echo 🚀 Your Express Deals environment is ready!

pause
