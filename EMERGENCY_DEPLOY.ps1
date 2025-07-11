# Express Deals Emergency Deployment Script - PowerShell
# This script will force deploy all fixes to Heroku

Write-Host "=== EXPRESS DEALS EMERGENCY DEPLOYMENT ===" -ForegroundColor Yellow
Write-Host "Starting deployment process..." -ForegroundColor Green

try {
    # Change to project directory
    Set-Location "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
    Write-Host "Changed to project directory: $(Get-Location)" -ForegroundColor Cyan
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & ".\.venv\Scripts\Activate.ps1"
    
    # Check Python version
    Write-Host "Python version: $(python --version)" -ForegroundColor Cyan
    
    # Check git status
    Write-Host "Checking git status..." -ForegroundColor Cyan
    git status --porcelain
    
    # Add all files
    Write-Host "Staging all changes..." -ForegroundColor Cyan
    git add -A
    
    # Commit changes
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "EMERGENCY DEPLOYMENT: Express Deals fixes - $timestamp"
    Write-Host "Committing: $commitMessage" -ForegroundColor Cyan
    git commit -m $commitMessage
    
    # Push to GitHub
    Write-Host "Pushing to GitHub main..." -ForegroundColor Cyan
    git push origin main
    
    # Set Heroku remote
    Write-Host "Setting Heroku remote..." -ForegroundColor Cyan
    heroku git:remote -a express-deals
    
    # Force push to Heroku
    Write-Host "FORCE PUSHING TO HEROKU MAIN..." -ForegroundColor Red
    git push heroku main --force
    
    # Run database migrations
    Write-Host "Running database migrations..." -ForegroundColor Cyan
    heroku run python manage.py migrate --app express-deals
    
    # Collect static files
    Write-Host "Collecting static files..." -ForegroundColor Cyan
    heroku run python manage.py collectstatic --noinput --app express-deals
    
    # Check deployment status
    Write-Host "Checking deployment status..." -ForegroundColor Cyan
    heroku ps --app express-deals
    
    # Test the live site
    Write-Host "Testing live site..." -ForegroundColor Cyan
    $response = Invoke-WebRequest -Uri "https://express-deals-16b6c1fa4311.herokuapp.com/" -Method Head -TimeoutSec 30
    Write-Host "Site response: $($response.StatusCode)" -ForegroundColor Green
    
    Write-Host "=== DEPLOYMENT COMPLETE ===" -ForegroundColor Green
    Write-Host "Your site is live at: https://express-deals-16b6c1fa4311.herokuapp.com/" -ForegroundColor Yellow
    
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
}

Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
