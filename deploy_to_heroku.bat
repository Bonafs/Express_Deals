@echo off
echo 🚀 EXPRESS DEALS - HEROKU DEPLOYMENT AUTOMATION
echo ================================================

echo.
echo 🔑 Step 1: Login to Heroku
heroku login

echo.
echo 🏗️ Step 2: Create Heroku Application
set /p APP_NAME=Enter your app name (e.g., express-deals-yourname): 
heroku create %APP_NAME%
heroku git:remote -a %APP_NAME%

echo.
echo 📦 Step 3: Add Required Add-ons
heroku addons:create heroku-postgresql:essential-0
heroku addons:create heroku-redis:essential-0

echo.
echo 🔐 Step 4: Generate Secret Key
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))" > temp_secret.txt
echo Copy this secret key and use it in the next step:
type temp_secret.txt
del temp_secret.txt

echo.
echo ⚙️ Step 5: Set Environment Variables
set /p SECRET_KEY=Enter the secret key from above: 
heroku config:set SECRET_KEY="%SECRET_KEY%"
heroku config:set DJANGO_SETTINGS_MODULE="express_deals.heroku_settings"

echo.
echo 📧 Step 6: Email Configuration (SendGrid)
set /p SENDGRID_KEY=Enter SendGrid API key (or press Enter to skip): 
if not "%SENDGRID_KEY%"=="" (
    heroku config:set SENDGRID_API_KEY="%SENDGRID_KEY%"
    heroku config:set DEFAULT_FROM_EMAIL="noreply@%APP_NAME%.herokuapp.com"
)

echo.
echo 💳 Step 7: Payment Configuration (Stripe)
set /p STRIPE_PK=Enter Stripe Publishable Key (or press Enter to skip): 
if not "%STRIPE_PK%"=="" (
    heroku config:set STRIPE_PUBLISHABLE_KEY="%STRIPE_PK%"
    set /p STRIPE_SK=Enter Stripe Secret Key: 
    heroku config:set STRIPE_SECRET_KEY="%STRIPE_SK%"
)

echo.
echo 🚀 Step 8: Deploy to Heroku
git add .
git commit -m "feat: Heroku production deployment ready"
git push heroku main

echo.
echo 📊 Step 9: Run Database Setup
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput

echo.
echo ⚡ Step 10: Scale Workers
heroku ps:scale web=1
heroku ps:scale worker=1
heroku ps:scale beat=1

echo.
echo 🎉 DEPLOYMENT COMPLETE!
echo ==================
echo.
echo Your Express Deals platform is now live at:
heroku open
echo.
echo View logs with: heroku logs --tail
echo Check status with: heroku ps
echo.
echo 🎯 Next: Create superuser with: heroku run python manage.py createsuperuser

pause
