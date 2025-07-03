# Express Deals Git Setup Script
Set-Location "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green

Write-Host "Checking git status..." -ForegroundColor Yellow
git status

Write-Host "Adding all files..." -ForegroundColor Yellow
git add .

Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Final commit: Complete Express Deals e-commerce platform with all features

- Complete product catalog with categories and search
- Shopping cart functionality with session management
- Secure payment processing with Stripe integration
- User authentication and account management
- Order management and tracking system
- Responsive Bootstrap UI with modern design
- Environment variable configuration
- Comprehensive documentation
- Production-ready settings and deployment configuration

Features included:
- Product browsing and detailed views
- Cart management (add, remove, update quantities)
- Secure checkout process
- Payment processing with Stripe
- Order history and tracking
- User registration and login
- Admin interface for management
- Email notifications
- Static file handling
- Error handling and logging
- Security best practices"

Write-Host "Checking remote repository..." -ForegroundColor Yellow
git remote -v

Write-Host "If no remote exists, add your GitHub repository URL:" -ForegroundColor Cyan
Write-Host "git remote add origin https://github.com/yourusername/express-deals.git" -ForegroundColor Cyan

Write-Host "Pushing to main branch..." -ForegroundColor Yellow
git push -u origin main

Write-Host "Git setup complete!" -ForegroundColor Green
