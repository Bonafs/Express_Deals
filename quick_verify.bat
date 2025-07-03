@echo off
echo.
echo 🎯 EXPRESS DEALS - QUICK VERIFICATION SCRIPT
echo ==============================================
echo.

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo 📍 Current Directory: %CD%
echo.

echo 🔍 Step 1: Checking if virtual environment exists...
if exist "env\Scripts\python.exe" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment not found - please create one first
    echo Run: python -m venv env
    pause
    exit /b 1
)

echo.
echo 🔍 Step 2: Activating virtual environment...
call env\Scripts\activate.bat

echo.
echo 🔍 Step 3: Checking Python version...
python --version

echo.
echo 🔍 Step 4: Testing key package imports...

echo Testing Django...
python -c "import django; print('✅ Django', django.get_version())" 2>nul || (echo ❌ Django FAILED && set ERROR=1)

echo Testing REST Framework...
python -c "import rest_framework; print('✅ REST Framework', rest_framework.VERSION)" 2>nul || (echo ❌ REST Framework FAILED && set ERROR=1)

echo Testing Celery...
python -c "import celery; print('✅ Celery', celery.__version__)" 2>nul || (echo ❌ Celery FAILED && set ERROR=1)

echo Testing Channels...
python -c "import channels; print('✅ Channels', channels.__version__)" 2>nul || (echo ❌ Channels FAILED && set ERROR=1)

echo Testing Scrapy...
python -c "import scrapy; print('✅ Scrapy', scrapy.__version__)" 2>nul || (echo ❌ Scrapy FAILED && set ERROR=1)

echo.
if defined ERROR (
    echo ❌ Some packages failed to import
    echo 🔧 Please run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
) else (
    echo 🎉 All packages imported successfully!
)

echo.
echo 🔍 Step 5: Running Django system check...
python manage.py check 2>nul && echo ✅ Django system check passed || echo ❌ Django system check failed

echo.
echo 🔍 Step 6: Testing REST Framework import...
python -c "from rest_framework import serializers; print('✅ REST Framework serializers imported successfully')" 2>nul || echo ❌ REST Framework serializers failed

echo.
echo 🎉 VERIFICATION COMPLETE!
echo.
echo 🚀 Your Express Deals environment is ready!
echo.
echo 💡 Next steps:
echo    1. Run: python manage.py runserver
echo    2. Open: http://127.0.0.1:8000/
echo    3. Access admin: http://127.0.0.1:8000/admin/
echo    4. Test alerts: http://127.0.0.1:8000/alerts/
echo.
pause
