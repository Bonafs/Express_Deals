# Express Deals Environment Setup and Verification Script (PowerShell)
# This script ensures the correct Python environment is activated and packages are installed

Write-Host "🚀 Express Deals - Environment Setup and Verification" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Navigate to project directory
Set-Location "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

Write-Host "📍 Current directory: $(Get-Location)" -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "✅ Virtual environment found in '.venv' directory" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found! Creating new one..." -ForegroundColor Red
    python -m venv .venv
    Write-Host "✅ New virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Check Python version
Write-Host "🐍 Python version:" -ForegroundColor Blue
python --version

# Upgrade pip
Write-Host "📦 Upgrading pip..." -ForegroundColor Magenta
python -m pip install --upgrade pip

# Install requirements
Write-Host "📋 Installing requirements from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check specific packages
Write-Host "🔍 Checking key package installations:" -ForegroundColor Cyan

Write-Host "Checking Django..." -ForegroundColor White
try {
    $djangoVersion = python -c "import django; print(django.get_version())" 2>$null
    Write-Host "✅ Django $djangoVersion installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Django FAILED" -ForegroundColor Red
}

Write-Host "Checking Django REST Framework..." -ForegroundColor White
try {
    $drfVersion = python -c "import rest_framework; print(rest_framework.VERSION)" 2>$null
    Write-Host "✅ REST Framework $drfVersion installed" -ForegroundColor Green
} catch {
    Write-Host "❌ REST Framework FAILED" -ForegroundColor Red
}

Write-Host "Checking Celery..." -ForegroundColor White
try {
    $celeryVersion = python -c "import celery; print(celery.__version__)" 2>$null
    Write-Host "✅ Celery $celeryVersion installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Celery FAILED" -ForegroundColor Red
}

Write-Host "Checking Channels..." -ForegroundColor White
try {
    $channelsVersion = python -c "import channels; print(channels.__version__)" 2>$null
    Write-Host "✅ Channels $channelsVersion installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Channels FAILED" -ForegroundColor Red
}

Write-Host "Checking Scrapy..." -ForegroundColor White
try {
    $scrapyVersion = python -c "import scrapy; print(scrapy.__version__)" 2>$null
    Write-Host "✅ Scrapy $scrapyVersion installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Scrapy FAILED" -ForegroundColor Red
}

# Run Django system check
Write-Host "🔧 Running Django system check..." -ForegroundColor Blue
python manage.py check --deploy

# Show installed packages
Write-Host "📦 Installed packages:" -ForegroundColor Magenta
pip list | Select-String -Pattern "django|celery|channels|scrapy|rest"

Write-Host ""
Write-Host "🎉 Environment verification complete!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 To activate this environment in the future, run:" -ForegroundColor Yellow
Write-Host "   Set-Location 'c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals'" -ForegroundColor White
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Your Express Deals environment is ready!" -ForegroundColor Green

Read-Host "Press Enter to continue..."
