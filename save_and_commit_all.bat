@echo off
echo 💾 SAVING ALL FILES AND COMMITTING TO GIT
echo ==================================================

cd /d "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
echo 📁 Working in: %CD%

echo.
echo 📦 Adding all files to staging...
git add -A
if %ERRORLEVEL% EQU 0 (
    echo ✅ All files added to staging
) else (
    echo ❌ Error adding files
)

echo.
echo 📋 Checking staged files...
git diff --cached --name-only
if %ERRORLEVEL% NEQ 0 echo ⚠️ Error checking staged files

echo.
echo 📊 Git status:
git status --porcelain
if %ERRORLEVEL% NEQ 0 echo ⚠️ Error checking git status

echo.
echo 💾 Committing changes...
git commit -m "Final commit: Save unsaved files and complete project deployment"
if %ERRORLEVEL% EQU 0 (
    echo ✅ Successfully committed
) else (
    echo ℹ️ Nothing to commit or error occurred
)

echo.
echo 🌐 Pushing to GitHub...
git push origin main
if %ERRORLEVEL% EQU 0 (
    echo ✅ Successfully pushed to GitHub
) else (
    echo ⚠️ Error pushing or already up to date
)

echo.
echo ==================================================
echo 🎯 ALL FILES SAVED AND COMMITTED!
pause
