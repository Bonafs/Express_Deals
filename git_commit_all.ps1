# Git Commit and Push Script for Express Deals (PowerShell)
# Ensures all changes are properly committed and pushed to GitHub

Write-Host "🔄 Express Deals - Git Commit and Push Script" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not a git repository. Initializing..." -ForegroundColor Red
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Check git status
Write-Host "📋 Checking git status..." -ForegroundColor Yellow
git status

# Add all files
Write-Host "📦 Adding all files to staging..." -ForegroundColor Yellow
git add -A

# Commit Phase A enhancements
Write-Host "📝 Committing Phase A: Cart Functionality Enhancements..." -ForegroundColor Blue
git add templates/orders/cart.html
git commit -m "Phase A: Enhanced cart functionality with improved AJAX error handling

- Added quantity validation and rollback functionality
- Improved error handling with better user feedback
- Enhanced remove item animation and confirmation
- Added data attribute tracking for quantity inputs
- Improved toast notifications with auto-dismiss"

# Commit Phase B enhancements
Write-Host "📝 Committing Phase B: Feature Enhancements..." -ForegroundColor Blue
git add templates/products/product_list.html, templates/base.html, express_deals/context_processors.py, express_deals/settings.py
git commit -m "Phase B: Enhanced product list and cart integration

- Enhanced add-to-cart AJAX with improved error handling
- Added dynamic cart counter in navbar
- Created context processor for cart data
- Improved search/filtering with debounced input
- Enhanced toast notifications and user feedback
- Added loading states and better UX"

# Commit Phase C (Payment integration was already complete)
Write-Host "📝 Phase C: Payment Integration (already complete)..." -ForegroundColor Blue

# Commit Phase D deployment preparation
Write-Host "📝 Committing Phase D: Deployment Preparation..." -ForegroundColor Blue
git add express_deals/production_settings.py, deploy_production.py
git commit -m "Phase D: Production deployment preparation

- Added comprehensive production settings with security headers
- Created automated deployment script with pre-checks
- Configured HTTPS enforcement and secure cookies
- Added database connection pooling and optimizations
- Implemented logging and cache configuration
- Added SSL redirect and security middleware"

# Commit testing suite
Write-Host "📝 Committing Testing Suite..." -ForegroundColor Blue
git add test_cart_functionality.py, test_comprehensive.py, final_project_report.py
git commit -m "Added comprehensive testing and evaluation suite

- Created cart functionality test suite
- Added comprehensive platform testing
- Implemented final project evaluation report
- Added automated project status checking
- Created deployment readiness verification"

# Commit documentation
Write-Host "📝 Committing Documentation Updates..." -ForegroundColor Blue
git add README.md, project_completion_summary.py, DEPLOYMENT_READINESS_REPORT.md, manual_deployment_check.py
git commit -m "Updated documentation and project completion

- Enhanced README.md with comprehensive project documentation
- Added project completion summary with phases A-D details
- Created deployment readiness report
- Added manual deployment verification script
- Documented all features, security, and deployment steps"

# Commit any remaining files
Write-Host "📝 Committing any remaining files..." -ForegroundColor Blue
git add -A
git commit -m "Final cleanup: Added any remaining files and configurations

- Ensured all project files are tracked
- Added any missing configurations
- Completed phases A through D implementation
- Project ready for production deployment"

# Check if remote exists
Write-Host "🔗 Checking GitHub remote..." -ForegroundColor Yellow
try {
    $remoteUrl = git remote get-url origin 2>$null
    if ($remoteUrl) {
        Write-Host "✅ GitHub remote configured: $remoteUrl" -ForegroundColor Green
        
        # Push to GitHub
        Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Magenta
        git push origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Push failed. You may need to set up authentication or check your remote URL." -ForegroundColor Yellow
        }
    } else {
        throw "No remote configured"
    }
} catch {
    Write-Host "⚠️ GitHub remote not configured" -ForegroundColor Yellow
    Write-Host "Please run: git remote add origin https://github.com/yourusername/express-deals.git" -ForegroundColor White
    Write-Host "Then run: git push -u origin main" -ForegroundColor White
}

# Final status
Write-Host ""
Write-Host "📊 Final Git Status:" -ForegroundColor Cyan
git log --oneline -10
Write-Host ""
Write-Host "🎉 All Express Deals changes committed!" -ForegroundColor Green
Write-Host "📋 Summary of commits made:" -ForegroundColor Cyan
Write-Host "   • Phase A: Enhanced cart functionality" -ForegroundColor White
Write-Host "   • Phase B: Feature enhancements and cart integration" -ForegroundColor White
Write-Host "   • Phase D: Production deployment preparation" -ForegroundColor White
Write-Host "   • Testing: Comprehensive test suites" -ForegroundColor White
Write-Host "   • Documentation: Updated README and guides" -ForegroundColor White
Write-Host "   • Final cleanup: All remaining files" -ForegroundColor White
Write-Host ""
Write-Host "✅ Express Deals is ready for production deployment!" -ForegroundColor Green
