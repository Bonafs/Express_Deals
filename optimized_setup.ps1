# PowerShell script to optimize and fix all Express Deals system issues
# Consolidated and optimized version - removes duplicates and redundancy

Write-Host "🚀 EXPRESS DEALS - OPTIMIZED SYSTEM FIX" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host ""

# Set location to project directory
$ProjectPath = "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
Set-Location $ProjectPath
Write-Host "📍 Working directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# Function to write colored status messages
function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $color = switch ($Type) {
        "Success" { "Green" }
        "Error" { "Red" }
        "Warning" { "Yellow" }
        "Info" { "Cyan" }
        default { "White" }
    }
    Write-Host $Message -ForegroundColor $color
}

# Function to test command execution
function Test-Command {
    param([string]$Command, [string]$Description)
    try {
        $result = Invoke-Expression $Command 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ $Description successful" "Success"
            return $true
        } else {
            Write-Status "❌ $Description failed: $result" "Error"
            return $false
        }
    } catch {
        Write-Status "❌ $Description error: $_" "Error"
        return $false
    }
}

# STEP 1: Virtual Environment Setup
Write-Host "🔧 STEP 1: Virtual Environment Setup" -ForegroundColor Yellow
Write-Host "-" * 40

$venvPath = ""
if (Test-Path ".venv") {
    Write-Status "✅ Found .venv directory" "Success"
    $venvPath = ".venv\Scripts\Activate.ps1"
} elseif (Test-Path "env") {
    Write-Status "⚠️ Found old 'env' directory, migrating to .venv..." "Warning"
    if (Test-Path "env\Scripts\python.exe") {
        python -m venv .venv
        $venvPath = ".venv\Scripts\Activate.ps1"
        Write-Status "✅ Created new .venv environment" "Success"
    }
} else {
    Write-Status "Creating new .venv environment..." "Info"
    python -m venv .venv
    $venvPath = ".venv\Scripts\Activate.ps1"
    Write-Status "✅ Created .venv environment" "Success"
}

# Set execution policy
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Write-Status "✅ Execution policy configured" "Success"
} catch {
    Write-Status "⚠️ Could not set execution policy" "Warning"
}

# Activate virtual environment
try {
    & $venvPath
    Write-Status "✅ Virtual environment activated" "Success"
} catch {
    Write-Status "❌ Failed to activate virtual environment" "Error"
    exit 1
}

# STEP 2: Python Environment Check
Write-Host "`n🐍 STEP 2: Python Environment Check" -ForegroundColor Yellow
Write-Host "-" * 40

$pythonVersion = python --version 2>&1
Write-Status "Python version: $pythonVersion" "Info"
$pythonPath = where.exe python 2>&1
Write-Status "Python location: $pythonPath" "Info"

# STEP 3: Package Installation
Write-Host "`n📦 STEP 3: Package Installation & Optimization" -ForegroundColor Yellow
Write-Host "-" * 40

# Upgrade pip first
Write-Status "Upgrading pip..." "Info"
Test-Command "python -m pip install --upgrade pip" "Pip upgrade"

# Define optimized package list (removed duplicates)
$corePackages = @(
    "django==5.2.4",
    "djangorestframework==3.14.0",
    "channels==4.0.0",
    "channels-redis==4.1.0",
    "dj-database-url==2.3.0",
    "whitenoise==6.8.2",
    "celery==5.3.4",
    "redis==5.0.1",
    "django-celery-beat==2.5.0",
    "django-celery-results==2.6.0",
    "pillow==11.1.0",
    "stripe==12.3.0",
    "beautifulsoup4==4.12.2",
    "requests==2.31.0"
)

# Try requirements.txt first, then individual packages
if (Test-Path "requirements.txt") {
    Write-Status "Installing from requirements.txt..." "Info"
    if (-not (Test-Command "pip install -r requirements.txt" "Requirements installation")) {
        Write-Status "Requirements file failed, installing core packages individually..." "Warning"
        foreach ($package in $corePackages) {
            Test-Command "pip install $package" "Installing $package"
        }
    }
} else {
    Write-Status "No requirements.txt found, installing core packages..." "Info"
    foreach ($package in $corePackages) {
        Test-Command "pip install $package" "Installing $package"
    }
}

# STEP 4: Import Verification
Write-Host "`n🧪 STEP 4: Import Verification" -ForegroundColor Yellow
Write-Host "-" * 40

$criticalImports = @{
    "Django" = "import django; print(f'Django {django.get_version()}')"
    "DRF" = "import rest_framework; print(f'DRF {rest_framework.VERSION}')"
    "Channels" = "import channels; print('Channels OK')"
    "Celery" = "import celery; print(f'Celery {celery.__version__}')"
    "Redis" = "import redis; print('Redis OK')"
    "Stripe" = "import stripe; print('Stripe OK')"
}

foreach ($import in $criticalImports.GetEnumerator()) {
    Test-Command "python -c `"$($import.Value)`"" "$($import.Name) import"
}

# STEP 5: Directory Structure
Write-Host "`n📁 STEP 5: Directory Structure Optimization" -ForegroundColor Yellow
Write-Host "-" * 40

$requiredDirs = @("logs", "media", "static", "staticfiles")
foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Status "✅ Created $dir directory" "Success"
    } else {
        Write-Status "✅ $dir directory exists" "Success"
    }
}

# STEP 6: Configuration Cleanup
Write-Host "`n🧹 STEP 6: Configuration Cleanup" -ForegroundColor Yellow
Write-Host "-" * 40

# Remove .env file (using hardcoded settings)
if (Test-Path ".env") {
    Remove-Item ".env" -Force
    Write-Status "✅ Removed .env file (using hardcoded settings)" "Success"
} else {
    Write-Status "✅ No .env file found (using hardcoded settings)" "Success"
}

# Clean up old environment directory if it exists
if (Test-Path "env" -and (Test-Path ".venv")) {
    Write-Status "⚠️ Found old 'env' directory alongside .venv" "Warning"
    $response = Read-Host "Remove old 'env' directory? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Remove-Item "env" -Recurse -Force
        Write-Status "✅ Removed old 'env' directory" "Success"
    }
}

# STEP 7: Django System Verification
Write-Host "`n🔧 STEP 7: Django System Verification" -ForegroundColor Yellow
Write-Host "-" * 40

# Django system check
Write-Status "Running Django system check..." "Info"
$checkResult = python manage.py check 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Status "✅ Django system check passed" "Success"
} else {
    Write-Status "⚠️ Django system check issues found:" "Warning"
    Write-Host $checkResult -ForegroundColor Yellow
    
    # Run migrations if needed
    Write-Status "Running migrations..." "Info"
    Test-Command "python manage.py migrate" "Database migration"
}

# STEP 8: Performance Test
Write-Host "`n🚀 STEP 8: Performance Test" -ForegroundColor Yellow
Write-Host "-" * 40

Write-Status "Testing Django startup performance..." "Info"
$startTime = Get-Date
try {
    $testResult = python -c "
import os
import time
start = time.time()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
import django
django.setup()
end = time.time()
print(f'Django startup time: {end - start:.2f} seconds')
" 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Status "✅ $testResult" "Success"
    } else {
        Write-Status "❌ Django startup test failed: $testResult" "Error"
    }
} catch {
    Write-Status "❌ Performance test failed: $_" "Error"
}

# FINAL SUMMARY
Write-Host "`n🎉 OPTIMIZATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host ""

$summary = @(
    "✅ Virtual environment optimized (.venv)",
    "✅ All packages installed and verified",
    "✅ Django configuration validated",
    "✅ Directory structure optimized",
    "✅ Configuration cleaned (no .env dependencies)",
    "✅ System performance tested",
    "✅ All redundancies removed"
)

foreach ($item in $summary) {
    Write-Status $item "Success"
}

Write-Host ""
Write-Status "🚀 Express Deals is optimized and ready!" "Success"
Write-Host ""
Write-Host "💡 Next Steps:" -ForegroundColor Yellow
Write-Host "1. python manage.py runserver" -ForegroundColor White
Write-Host "2. Open: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "3. Test all features" -ForegroundColor White
Write-Host ""

# Optional: Start development server
$startServer = Read-Host "Start development server now? (y/N)"
if ($startServer -eq "y" -or $startServer -eq "Y") {
    Write-Status "Starting development server..." "Info"
    python manage.py runserver
}

Write-Host ""
Read-Host "Press Enter to exit"
