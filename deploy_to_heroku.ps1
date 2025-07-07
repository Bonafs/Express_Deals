# 🚀 EXPRESS DEALS - HEROKU DEPLOYMENT AUTOMATION

Write-Host "🚀 EXPRESS DEALS - HEROKU DEPLOYMENT AUTOMATION" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

Write-Host ""
Write-Host "🔑 Step 1: Login to Heroku" -ForegroundColor Yellow
heroku login

Write-Host ""
Write-Host "🏗️ Step 2: Create Heroku Application" -ForegroundColor Yellow
$APP_NAME = Read-Host "Enter your app name (e.g., express-deals-yourname)"
heroku create $APP_NAME
heroku git:remote -a $APP_NAME

Write-Host ""
Write-Host "📦 Step 3: Add Required Add-ons" -ForegroundColor Yellow
heroku addons:create heroku-postgresql:essential-0
heroku addons:create heroku-redis:essential-0

Write-Host ""
Write-Host "🔐 Step 4: Generate Secret Key" -ForegroundColor Yellow
$SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
Write-Host "Generated Secret Key: $SECRET_KEY" -ForegroundColor Cyan

Write-Host ""
Write-Host "⚙️ Step 5: Set Environment Variables" -ForegroundColor Yellow
heroku config:set SECRET_KEY="$SECRET_KEY"
heroku config:set DJANGO_SETTINGS_MODULE="express_deals.heroku_settings"

Write-Host ""
Write-Host "📧 Step 6: Email Configuration (SendGrid)" -ForegroundColor Yellow
$SENDGRID_KEY = Read-Host "Enter SendGrid API key (or press Enter to skip)"
if ($SENDGRID_KEY -ne "") {
    heroku config:set SENDGRID_API_KEY="$SENDGRID_KEY"
    heroku config:set DEFAULT_FROM_EMAIL="noreply@$APP_NAME.herokuapp.com"
}

Write-Host ""
Write-Host "💳 Step 7: Payment Configuration (Stripe)" -ForegroundColor Yellow
$STRIPE_PK = Read-Host "Enter Stripe Publishable Key (or press Enter to skip)"
if ($STRIPE_PK -ne "") {
    heroku config:set STRIPE_PUBLISHABLE_KEY="$STRIPE_PK"
    $STRIPE_SK = Read-Host "Enter Stripe Secret Key"
    heroku config:set STRIPE_SECRET_KEY="$STRIPE_SK"
}

Write-Host ""
Write-Host "🚀 Step 8: Deploy to Heroku" -ForegroundColor Yellow
git add .
git commit -m "feat: Heroku production deployment ready"
git push heroku main

Write-Host ""
Write-Host "📊 Step 9: Run Database Setup" -ForegroundColor Yellow
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput

Write-Host ""
Write-Host "⚡ Step 10: Scale Workers" -ForegroundColor Yellow
heroku ps:scale web=1
heroku ps:scale worker=1
heroku ps:scale beat=1

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host ""
Write-Host "Your Express Deals platform is now live at:" -ForegroundColor Cyan
heroku open
Write-Host ""
Write-Host "View logs with: heroku logs --tail" -ForegroundColor Yellow
Write-Host "Check status with: heroku ps" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 Next: Create superuser with: heroku run python manage.py createsuperuser" -ForegroundColor Magenta

Read-Host "Press Enter to continue..."
