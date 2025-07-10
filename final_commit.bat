@echo off
title Express Deals - Final Commit
color 0A
echo.
echo ========================================
echo   EXPRESS DEALS - FINAL COMMIT
echo ========================================
echo.

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
echo Current directory: %CD%
echo.

echo Adding all files to git...
git add -A

echo.
echo Current git status:
git status --short

echo.
echo Committing changes...
git commit -m "Final commit: Save unsaved files and complete deployment - Fixed HEROKU_PUSH_COMPLETE.md formatting - All Express Deals features complete"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo Final git status:
git status

echo.
echo ========================================
echo   COMMIT PROCESS COMPLETE!
echo ========================================
echo.
echo Express Deals is live at:
echo https://express-deals.herokuapp.com
echo.
echo Dashboard available at:
echo https://express-deals.herokuapp.com/alerts/
echo.
pause
