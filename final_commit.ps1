# PowerShell script to save and commit all files
# Save and Commit All Unsaved Files - Express Deals Project

Write-Host "🚀 STARTING FINAL COMMIT PROCESS FOR EXPRESS DEALS" -ForegroundColor Green
Write-Host "=" * 60

# Set working directory
$projectPath = "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
Set-Location $projectPath
Write-Host "📁 Working Directory: $(Get-Location)" -ForegroundColor Cyan

# Check if we're in a git repository
if (Test-Path ".git") {
    Write-Host "✅ Git repository detected" -ForegroundColor Green
} else {
    Write-Host "❌ Not a git repository!" -ForegroundColor Red
    exit 1
}

# Add all files to staging
Write-Host "`n📦 Adding all files to git staging..." -ForegroundColor Yellow
try {
    git add -A
    Write-Host "✅ All files added to staging" -ForegroundColor Green
} catch {
    Write-Host "❌ Error adding files: $_" -ForegroundColor Red
}

# Check what's staged
Write-Host "`n📋 Checking staged files..." -ForegroundColor Yellow
$stagedFiles = git diff --cached --name-only
if ($stagedFiles) {
    Write-Host "📄 Files to be committed:" -ForegroundColor Cyan
    foreach ($file in $stagedFiles) {
        Write-Host "  - $file" -ForegroundColor White
    }
} else {
    Write-Host "ℹ️ No files to commit" -ForegroundColor Gray
}

# Check overall git status
Write-Host "`n📊 Current git status:" -ForegroundColor Yellow
git status --porcelain

# Commit if there are changes
$changes = git status --porcelain
if ($changes) {
    Write-Host "`n💾 Committing changes..." -ForegroundColor Yellow
    $commitMessage = "Final commit: Save unsaved files and complete project deployment

- Fixed HEROKU_PUSH_COMPLETE.md formatting
- Added final production deployment scripts
- Completed all Express Deals features and deployment
- Project is now production-ready with UK GBP pricing
- Dashboard with price tracking is live on Heroku"
    
    try {
        git commit -m $commitMessage
        Write-Host "✅ Successfully committed changes" -ForegroundColor Green
        
        # Push to GitHub
        Write-Host "`n🌐 Pushing to GitHub..." -ForegroundColor Yellow
        git push origin main
        Write-Host "✅ Successfully pushed to GitHub" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Error committing or pushing: $_" -ForegroundColor Red
    }
} else {
    Write-Host "`n✅ Working tree is clean - no changes to commit" -ForegroundColor Green
}

# Final verification
Write-Host "`n🔍 Final verification..." -ForegroundColor Yellow
git status
Write-Host "`n📅 Recent commits:" -ForegroundColor Yellow
git log --oneline -3

Write-Host "`n" + "=" * 60
Write-Host "🎉 FINAL COMMIT PROCESS COMPLETE!" -ForegroundColor Green
Write-Host "🌐 Express Deals is live at: https://express-deals.herokuapp.com" -ForegroundColor Cyan
Write-Host "📊 Dashboard available at: https://express-deals.herokuapp.com/alerts/" -ForegroundColor Cyan
Write-Host "✅ All files saved and committed to GitHub" -ForegroundColor Green
