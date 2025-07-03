#!/bin/bash
# Git Commit and Push Script for Express Deals
# Ensures all changes are properly committed and pushed to GitHub

echo "🔄 Express Deals - Git Commit and Push Script"
echo "=============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Initializing..."
    git init
    echo "✅ Git repository initialized"
fi

# Check git status
echo "📋 Checking git status..."
git status

# Add all files
echo "📦 Adding all files to staging..."
git add -A

# Commit Phase A enhancements
echo "📝 Committing Phase A: Cart Functionality Enhancements..."
git add templates/orders/cart.html
git commit -m "Phase A: Enhanced cart functionality with improved AJAX error handling

- Added quantity validation and rollback functionality
- Improved error handling with better user feedback
- Enhanced remove item animation and confirmation
- Added data attribute tracking for quantity inputs
- Improved toast notifications with auto-dismiss"

# Commit Phase B enhancements
echo "📝 Committing Phase B: Feature Enhancements..."
git add templates/products/product_list.html templates/base.html express_deals/context_processors.py express_deals/settings.py
git commit -m "Phase B: Enhanced product list and cart integration

- Enhanced add-to-cart AJAX with improved error handling
- Added dynamic cart counter in navbar
- Created context processor for cart data
- Improved search/filtering with debounced input
- Enhanced toast notifications and user feedback
- Added loading states and better UX"

# Commit Phase C (Payment integration was already complete)
echo "📝 Phase C: Payment Integration (already complete)..."

# Commit Phase D deployment preparation
echo "📝 Committing Phase D: Deployment Preparation..."
git add express_deals/production_settings.py deploy_production.py
git commit -m "Phase D: Production deployment preparation

- Added comprehensive production settings with security headers
- Created automated deployment script with pre-checks
- Configured HTTPS enforcement and secure cookies
- Added database connection pooling and optimizations
- Implemented logging and cache configuration
- Added SSL redirect and security middleware"

# Commit testing suite
echo "📝 Committing Testing Suite..."
git add test_cart_functionality.py test_comprehensive.py final_project_report.py
git commit -m "Added comprehensive testing and evaluation suite

- Created cart functionality test suite
- Added comprehensive platform testing
- Implemented final project evaluation report
- Added automated project status checking
- Created deployment readiness verification"

# Commit documentation
echo "📝 Committing Documentation Updates..."
git add README.md project_completion_summary.py DEPLOYMENT_READINESS_REPORT.md manual_deployment_check.py
git commit -m "Updated documentation and project completion

- Enhanced README.md with comprehensive project documentation
- Added project completion summary with phases A-D details
- Created deployment readiness report
- Added manual deployment verification script
- Documented all features, security, and deployment steps"

# Commit any remaining files
echo "📝 Committing any remaining files..."
git add -A
git commit -m "Final cleanup: Added any remaining files and configurations

- Ensured all project files are tracked
- Added any missing configurations
- Completed phases A through D implementation
- Project ready for production deployment"

# Check if remote exists
echo "🔗 Checking GitHub remote..."
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ GitHub remote configured"
    
    # Push to GitHub
    echo "🚀 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
    else
        echo "⚠️ Push failed. You may need to set up authentication or check your remote URL."
    fi
else
    echo "⚠️ GitHub remote not configured"
    echo "Please run: git remote add origin https://github.com/yourusername/express-deals.git"
    echo "Then run: git push -u origin main"
fi

# Final status
echo ""
echo "📊 Final Git Status:"
git log --oneline -10
echo ""
echo "🎉 All Express Deals changes committed!"
echo "📋 Summary of commits made:"
echo "   • Phase A: Enhanced cart functionality"
echo "   • Phase B: Feature enhancements and cart integration"  
echo "   • Phase D: Production deployment preparation"
echo "   • Testing: Comprehensive test suites"
echo "   • Documentation: Updated README and guides"
echo "   • Final cleanup: All remaining files"
echo ""
echo "✅ Express Deals is ready for production deployment!"
