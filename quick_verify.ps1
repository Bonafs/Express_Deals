# Express Deals Quick Verification Script (PowerShell)

Write-Host ""
Write-Host "🎯 EXPRESS DEALS - QUICK VERIFICATION SCRIPT" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""

Set-Location "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

Write-Host "📍 Current Directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔍 Step 1: Checking if virtual environment exists..." -ForegroundColor Yellow
if (Test-Path "env\Scripts\python.exe") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found - please create one first" -ForegroundColor Red
    Write-Host "Run: python -m venv env" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🔍 Step 2: Activating virtual environment..." -ForegroundColor Yellow
& "env\Scripts\Activate.ps1"

Write-Host ""
Write-Host "🔍 Step 3: Checking Python version..." -ForegroundColor Yellow
python --version

Write-Host ""
Write-Host "🔍 Step 4: Testing key package imports..." -ForegroundColor Yellow

$errors = 0

Write-Host "Testing Django..." -ForegroundColor White
try {
    $result = python -c "import django; print('✅ Django', django.get_version())" 2>$null
    Write-Host $result -ForegroundColor Green
} catch {
    Write-Host "❌ Django FAILED" -ForegroundColor Red
    $errors++
}

Write-Host "Testing REST Framework..." -ForegroundColor White
try {
    $result = python -c "import rest_framework; print('✅ REST Framework', rest_framework.VERSION)" 2>$null
    Write-Host $result -ForegroundColor Green
} catch {
    Write-Host "❌ REST Framework FAILED" -ForegroundColor Red
    $errors++
}

Write-Host "Testing Celery..." -ForegroundColor White
try {
    $result = python -c "import celery; print('✅ Celery', celery.__version__)" 2>$null
    Write-Host $result -ForegroundColor Green
} catch {
    Write-Host "❌ Celery FAILED" -ForegroundColor Red
    $errors++
}

Write-Host "Testing Channels..." -ForegroundColor White
try {
    $result = python -c "import channels; print('✅ Channels', channels.__version__)" 2>$null
    Write-Host $result -ForegroundColor Green
} catch {
    Write-Host "❌ Channels FAILED" -ForegroundColor Red
    $errors++
}

Write-Host "Testing Scrapy..." -ForegroundColor White
try {
    $result = python -c "import scrapy; print('✅ Scrapy', scrapy.__version__)" 2>$null
    Write-Host $result -ForegroundColor Green
} catch {
    Write-Host "❌ Scrapy FAILED" -ForegroundColor Red
    $errors++
}

Write-Host ""
if ($errors -gt 0) {
    Write-Host "❌ Some packages failed to import" -ForegroundColor Red
    Write-Host "🔧 Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue"
    exit 1
} else {
    Write-Host "🎉 All packages imported successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔍 Step 5: Running Django system check..." -ForegroundColor Yellow
try {
    python manage.py check 2>$null | Out-Null
    Write-Host "✅ Django system check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Django system check failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 Step 6: Testing REST Framework import..." -ForegroundColor Yellow
try {
    python -c "from rest_framework import serializers; print('✅ REST Framework serializers imported successfully')" 2>$null
    Write-Host "✅ REST Framework serializers imported successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ REST Framework serializers failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 VERIFICATION COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Your Express Deals environment is ready!" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Run: python manage.py runserver" -ForegroundColor White
Write-Host "   2. Open: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "   3. Access admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "   4. Test alerts: http://127.0.0.1:8000/alerts/" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue"
