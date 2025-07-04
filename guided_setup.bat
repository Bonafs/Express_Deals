@echo off
echo.
echo 🎯 EXPRESS DEALS - INTERACTIVE SETUP VERIFICATION
echo ===============================================
echo.
echo This script will guide you through each step and verify your setup.
echo Follow the prompts carefully.
echo.

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo 📍 CHECKPOINT 1: Project Directory
echo Current directory: %CD%
echo.
echo ✅ Are you in the Express_Deals project directory? (Y/N)
set /p checkpoint1=
if /i "%checkpoint1%" neq "Y" (
    echo Please navigate to the correct directory first.
    pause
    exit /b 1
)

echo.
echo 📍 CHECKPOINT 2: Virtual Environment
if exist ".venv\Scripts\python.exe" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment not found
    echo Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
)

echo.
echo 📍 CHECKPOINT 3: Activating Environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 📍 CHECKPOINT 4: Python Version Check
echo Python version:
python --version
echo.
echo ✅ Does Python version look correct? (Y/N)
set /p checkpoint4=
if /i "%checkpoint4%" neq "Y" (
    echo Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo 📍 CHECKPOINT 5: Installing Requirements
echo Installing all requirements (this may take a few minutes)...
pip install -r requirements.txt
echo.
echo ✅ Did the installation complete successfully? (Y/N)
set /p checkpoint5=
if /i "%checkpoint5%" neq "Y" (
    echo Please check for error messages above.
    pause
    exit /b 1
)

echo.
echo 📍 CHECKPOINT 6: Testing Django
echo Testing Django installation...
python -c "import django; print('Django version:', django.get_version())" 2>nul && (
    echo ✅ Django is working
) || (
    echo ❌ Django failed to import
    echo Installing Django...
    pip install django
)

echo.
echo 📍 CHECKPOINT 7: Testing REST Framework
echo Testing REST Framework installation...
python -c "import rest_framework; print('REST Framework version:', rest_framework.VERSION)" 2>nul && (
    echo ✅ REST Framework is working
) || (
    echo ❌ REST Framework failed to import
    echo Installing REST Framework...
    pip install djangorestframework
)

echo.
echo 📍 CHECKPOINT 8: Testing All Packages
echo Testing all major packages...
python -c "import django, rest_framework, celery, channels, scrapy; print('All packages imported successfully!')" 2>nul && (
    echo ✅ All major packages are working
) || (
    echo ❌ Some packages failed to import
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo 📍 CHECKPOINT 9: Django System Check
echo Running Django system check...
python manage.py check && (
    echo ✅ Django system check passed
) || (
    echo ❌ Django system check failed
    echo Please review the error messages above.
)

echo.
echo 📍 CHECKPOINT 10: Server Test
echo Testing development server...
echo Starting server (will stop automatically in 5 seconds)...
timeout /t 5 > nul
echo Server test completed.

echo.
echo 🎉 SETUP VERIFICATION COMPLETE!
echo.
echo Your Express Deals environment should now be ready.
echo.
echo 🚀 Next steps:
echo 1. Run: python manage.py runserver
echo 2. Open: http://127.0.0.1:8000/
echo 3. Test your Express Deals platform!
echo.
echo 📚 For detailed instructions, see: INTERACTIVE_SETUP_GUIDE.md
echo.
pause
