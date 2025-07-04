# PowerShell Script to change virtual environment from 'env' to '.venv'

Write-Host "🔄 Changing virtual environment from 'env' to '.venv'" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Create new virtual environment with .venv name
Write-Host "📦 Creating new .venv virtual environment..." -ForegroundColor Yellow
try {
    python -m venv .venv
    Write-Host "✅ New .venv virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create .venv virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate the new environment and install requirements
Write-Host "🔄 Activating .venv and installing requirements..." -ForegroundColor Yellow
try {
    & ".venv\Scripts\Activate.ps1"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "✅ Requirements installed in .venv" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install requirements" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Update .gitignore to include .venv
Write-Host "📝 Updating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = ""
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
}

if (-not $gitignoreContent.Contains(".venv")) {
    Add-Content ".gitignore" "`n.venv/`n# Virtual environment"
    Write-Host "✅ .gitignore updated" -ForegroundColor Green
} else {
    Write-Host "✅ .gitignore already contains .venv" -ForegroundColor Green
}

Write-Host "🎉 Virtual environment successfully changed to .venv!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Yellow
Write-Host "1. Delete the old 'env' directory: Remove-Item -Recurse -Force env" -ForegroundColor White
Write-Host "2. Update any IDE/editor settings to use .venv" -ForegroundColor White
Write-Host "3. Use: .venv\Scripts\Activate.ps1 to activate environment" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue"
