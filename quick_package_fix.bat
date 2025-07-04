@echo off
echo 🔧 EXPRESS DEALS - QUICK PACKAGE FIX
echo =======================================

echo.
echo 📦 Installing Django REST Framework...
pip install djangorestframework
if %errorlevel% equ 0 (
    echo ✅ Django REST Framework installed
) else (
    echo ❌ Failed to install Django REST Framework
)

echo.
echo 📦 Installing other required packages...
pip install django dj-database-url celery channels channels-redis redis pillow stripe whitenoise django-celery-beat django-celery-results

echo.
echo 🧪 Testing Django REST Framework import...
python -c "import rest_framework; print('✅ Django REST Framework version:', rest_framework.VERSION)" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Django REST Framework import successful
) else (
    echo ❌ Django REST Framework import failed
)

echo.
echo 🧪 Testing Django setup...
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings'); import django; django.setup(); print('✅ Django setup successful')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Django setup successful
) else (
    echo ❌ Django setup failed
)

echo.
echo 🔍 Running Django system check...
python manage.py check
if %errorlevel% equ 0 (
    echo ✅ Django system check passed
) else (
    echo ❌ Django system check found issues
)

echo.
echo 🎉 Package fix complete!
echo 💡 You can now run: python manage.py runserver
pause
