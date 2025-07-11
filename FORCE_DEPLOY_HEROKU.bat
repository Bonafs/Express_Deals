@echo off
echo "=== EXPRESS DEALS FORCE DEPLOYMENT TO HEROKU ==="
echo "Changing to project directory..."
cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

echo "Activating virtual environment..."
call .venv\Scripts\activate.bat

echo "Checking current directory..."
dir

echo "Checking git status..."
git status

echo "Adding all files..."
git add -A

echo "Committing changes..."
git commit -m "FORCE DEPLOYMENT: Express Deals with all fixes - %date% %time%"

echo "Pushing to GitHub main..."
git push origin main

echo "Setting Heroku remote..."
heroku git:remote -a express-deals

echo "FORCE PUSHING TO HEROKU MAIN..."
git push heroku main --force

echo "Running Heroku migrations..."
heroku run python manage.py migrate --app express-deals

echo "Collecting static files..."
heroku run python manage.py collectstatic --noinput --app express-deals

echo "Checking Heroku app status..."
heroku ps --app express-deals

echo "Testing live site..."
curl -I https://express-deals-16b6c1fa4311.herokuapp.com/

echo "=== DEPLOYMENT COMPLETE ==="
pause
