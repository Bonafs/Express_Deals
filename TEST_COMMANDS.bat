@echo off
REM Express Deals Deployment Commands - PowerShell Compatible
echo ======================================================
echo Express Deals - Correct PowerShell Deployment Commands
echo ======================================================

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM CORRECT: Use separate commands instead of && operators
echo.
echo Step 1: Check git status
git status

echo.
echo Step 2: Add all files
git add -A

echo.
echo Step 3: Commit changes
git commit -m "Production deployment - Fixed template errors and DEBUG settings"

echo.
echo Step 4: Push to GitHub main branch
git push origin main

echo.
echo Step 5: Deploy to Heroku main branch
git push heroku main

echo.
echo Step 6: Check Heroku app status
heroku ps --app express-deals

echo.
echo Step 7: View recent logs
heroku logs --app express-deals -n 10

echo.
echo Step 8: Open live website
heroku open --app express-deals

echo.
echo ======================================================
echo DEPLOYMENT COMPLETE!
echo Website is live at: https://express-deals-16b6c1fa4311.herokuapp.com/
echo ======================================================
pause
