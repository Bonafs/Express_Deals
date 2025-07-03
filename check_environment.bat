@echo off
echo 🚀 Express Deals - Quick Environment Check
echo ========================================

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo 📍 Project Directory: %CD%

echo 🔄 Activating virtual environment...
call env\Scripts\activate.bat

echo 🐍 Python Information:
python --version
echo Python location: 
where python

echo 📦 Checking Django REST Framework...
python -c "import rest_framework; print('✅ REST Framework version:', rest_framework.VERSION)" 2>nul || echo "❌ REST Framework NOT installed"

echo 📦 Checking Django...
python -c "import django; print('✅ Django version:', django.get_version())" 2>nul || echo "❌ Django NOT installed"

echo 🔧 Running comprehensive environment check...
python verify_environment.py

echo.
echo 💡 If you see errors above, run: setup_environment.bat
echo 🚀 Environment check complete!
pause
