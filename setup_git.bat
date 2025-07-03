@echo off
cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
echo Current directory: %CD%

echo Checking git status...
git status

echo Adding all files...
git add .

echo Committing changes...
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

echo Checking remote repository...
git remote -v

echo If no remote exists, add your GitHub repository URL:
echo git remote add origin https://github.com/yourusername/express-deals.git

echo Pushing to main branch...
git push -u origin main

echo Git setup complete!
pause
