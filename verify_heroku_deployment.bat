@echo off
REM Heroku Deployment Verification Script
echo ============================================
echo EXPRESS DEALS HEROKU DEPLOYMENT VERIFICATION
echo ============================================

echo.
echo 1. CHECKING HEROKU APP STATUS...
heroku ps --app express-deals

echo.
echo 2. CHECKING LATEST RELEASES...
heroku releases --app express-deals -n 5

echo.
echo 3. CHECKING CONFIG VARIABLES...
heroku config --app express-deals

echo.
echo 4. RUNNING TRANSACTION ID FIX...
heroku run "python manage.py fix_transaction_ids" --app express-deals

echo.
echo 5. RUNNING MIGRATIONS...
heroku run "python manage.py migrate" --app express-deals

echo.
echo 6. CHECKING APP LOGS...
heroku logs --tail -n 20 --app express-deals

echo.
echo ============================================
echo VERIFICATION COMPLETE
echo ============================================
pause
