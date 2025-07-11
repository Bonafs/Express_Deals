@echo off
title Express Deals Emergency Deployment
echo.
echo ============================================
echo    EXPRESS DEALS EMERGENCY DEPLOYMENT
echo ============================================
echo.

REM Change to project directory
cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
echo Current directory: %CD%

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Show Python version
echo Python version:
python --version

REM Check git status
echo.
echo Checking git status...
git status

REM Add all files
echo.
echo Adding all files...
git add -A

REM Commit changes
echo.
echo Committing changes...
git commit -m "EMERGENCY DEPLOYMENT: Express Deals fixes with template fix - %date% %time%"

REM Push to GitHub
echo.
echo Pushing to GitHub main...
git push origin main

REM Set Heroku remote
echo.
echo Setting Heroku remote...
heroku git:remote -a express-deals

REM Force push to Heroku
echo.
echo FORCE PUSHING TO HEROKU MAIN...
git push heroku main --force

REM Run migrations
echo.
echo Running migrations...
heroku run python manage.py migrate --app express-deals

REM Collect static files
echo.
echo Collecting static files...
heroku run python manage.py collectstatic --noinput --app express-deals

REM Check status
echo.
echo Checking app status...
heroku ps --app express-deals

echo.
echo ============================================
echo        DEPLOYMENT COMPLETE!
echo ============================================
echo Your site: https://express-deals-16b6c1fa4311.herokuapp.com/
echo.
pause
