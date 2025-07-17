#!/usr/bin/env powershell

# Express Deals Heroku Deployment Script
Write-Host "🚀 Starting Express Deals Heroku Deployment..." -ForegroundColor Green

# Check if we're in the correct directory
Write-Host "📁 Current Directory: $(Get-Location)" -ForegroundColor Yellow

# Activate virtual environment if it exists
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "⚠️  Virtual environment not found, using system Python" -ForegroundColor Yellow
}

# Check Python version
Write-Host "🐍 Python Version:" -ForegroundColor Yellow
python --version

# Check Django
Write-Host "🎯 Django Check:" -ForegroundColor Yellow
python -c "import django; print('Django', django.VERSION)"

# Check git status
Write-Host "📋 Git Status:" -ForegroundColor Yellow
git status --porcelain

# Check if Heroku CLI is available
Write-Host "☁️  Heroku CLI:" -ForegroundColor Yellow
heroku --version

# Set Heroku config
Write-Host "⚙️  Setting Heroku config..." -ForegroundColor Yellow
heroku config:set DISABLE_COLLECTSTATIC=1

# Push to Heroku
Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Green
git push heroku main

Write-Host "✅ Deployment script completed!" -ForegroundColor Green
