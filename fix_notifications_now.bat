@echo off
echo 🚨 URGENT NOTIFICATION MODULE FIX
echo ================================

echo.
echo 1️⃣ Checking virtual environments...
if exist ".venv" (
    echo ✅ .venv directory found
) else (
    echo ❌ .venv not found - creating it now...
    python -m venv .venv
    echo ✅ .venv created
)

echo.
echo 2️⃣ Activating .venv...
call .venv\Scripts\activate.bat

echo.
echo 3️⃣ Installing django-notifications-hq...
pip install django-notifications-hq==1.8.3

echo.
echo 4️⃣ Installing all requirements...
pip install -r requirements.txt

echo.
echo 5️⃣ Testing notification import...
python -c "import notifications; print('✅ notifications module working'); print('Version:', notifications.__version__)"

echo.
echo 6️⃣ Testing Django setup...
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings'); django.setup(); from scraping.notifications import NotificationService; print('✅ NotificationService imported successfully')"

echo.
echo 7️⃣ Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo 🎉 NOTIFICATION MODULE FIX COMPLETE!
echo.
echo To test, run:
echo   .venv\Scripts\activate
echo   python manage.py shell
echo   from scraping.notifications import NotificationService

pause
