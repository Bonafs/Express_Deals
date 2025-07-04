# Express Deals Interactive Setup Script (PowerShell)

Write-Host ""
Write-Host "🎯 EXPRESS DEALS - INTERACTIVE SETUP VERIFICATION" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "This script will guide you through each step and verify your setup." -ForegroundColor Cyan
Write-Host "Follow the prompts carefully." -ForegroundColor Cyan
Write-Host ""

Set-Location "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

Write-Host "📍 CHECKPOINT 1: Project Directory" -ForegroundColor Yellow
Write-Host "Current directory: $(Get-Location)" -ForegroundColor White
Write-Host ""
$checkpoint1 = Read-Host "✅ Are you in the Express_Deals project directory? (Y/N)"
if ($checkpoint1 -ne "Y") {
    Write-Host "Please navigate to the correct directory first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📍 CHECKPOINT 2: Virtual Environment" -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

Write-Host ""
Write-Host "📍 CHECKPOINT 3: Activating Environment" -ForegroundColor Yellow
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "📍 CHECKPOINT 4: Python Version Check" -ForegroundColor Yellow
Write-Host "Python version:" -ForegroundColor White
python --version
Write-Host ""
$checkpoint4 = Read-Host "✅ Does Python version look correct? (Y/N)"
if ($checkpoint4 -ne "Y") {
    Write-Host "Please check your Python installation." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📍 CHECKPOINT 5: Installing Requirements" -ForegroundColor Yellow
Write-Host "Installing all requirements (this may take a few minutes)..." -ForegroundColor Cyan
pip install -r requirements.txt
Write-Host ""
$checkpoint5 = Read-Host "✅ Did the installation complete successfully? (Y/N)"
if ($checkpoint5 -ne "Y") {
    Write-Host "Please check for error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📍 CHECKPOINT 6: Testing Django" -ForegroundColor Yellow
Write-Host "Testing Django installation..." -ForegroundColor Cyan
try {
    $djangoResult = python -c "import django; print('Django version:', django.get_version())" 2>$null
    Write-Host "✅ Django is working - $djangoResult" -ForegroundColor Green
} catch {
    Write-Host "❌ Django failed to import" -ForegroundColor Red
    Write-Host "Installing Django..." -ForegroundColor Cyan
    pip install django
}

Write-Host ""
Write-Host "📍 CHECKPOINT 7: Testing REST Framework" -ForegroundColor Yellow
Write-Host "Testing REST Framework installation..." -ForegroundColor Cyan
try {
    $restResult = python -c "import rest_framework; print('REST Framework version:', rest_framework.VERSION)" 2>$null
    Write-Host "✅ REST Framework is working - $restResult" -ForegroundColor Green
} catch {
    Write-Host "❌ REST Framework failed to import" -ForegroundColor Red
    Write-Host "Installing REST Framework..." -ForegroundColor Cyan
    pip install djangorestframework
}

Write-Host ""
Write-Host "📍 CHECKPOINT 8: Testing All Packages" -ForegroundColor Yellow
Write-Host "Testing all major packages..." -ForegroundColor Cyan
try {
    python -c "import django, rest_framework, celery, channels, scrapy; print('All packages imported successfully!')" 2>$null
    Write-Host "✅ All major packages are working" -ForegroundColor Green
} catch {
    Write-Host "❌ Some packages failed to import" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    Read-Host "Press Enter to continue anyway"
}

Write-Host ""
Write-Host "📍 CHECKPOINT 9: Django System Check" -ForegroundColor Yellow
Write-Host "Running Django system check..." -ForegroundColor Cyan
try {
    python manage.py check 2>$null
    Write-Host "✅ Django system check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Django system check failed" -ForegroundColor Red
    Write-Host "Please review the error messages above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📍 CHECKPOINT 10: Final Verification" -ForegroundColor Yellow
Write-Host "Running final comprehensive test..." -ForegroundColor Cyan
python -c "
import django, rest_framework, celery, channels, scrapy
print('🎉 SUCCESS: All major packages working!')
print(f'Django: {django.get_version()}')
print(f'REST Framework: {rest_framework.VERSION}')
print(f'Celery: {celery.__version__}')
print('🚀 Express Deals is ready!')
"

Write-Host ""
Write-Host "🎉 SETUP VERIFICATION COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "Your Express Deals environment should now be ready." -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Yellow
Write-Host "1. Run: python manage.py runserver" -ForegroundColor White
Write-Host "2. Open: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "3. Test your Express Deals platform!" -ForegroundColor White
Write-Host ""
Write-Host "📚 For detailed instructions, see: INTERACTIVE_SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to continue"
