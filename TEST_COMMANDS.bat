@echo off
echo Testing basic commands...
echo Current directory: %CD%
dir
echo Git status:
git --version
echo Heroku version:
heroku --version
echo Python version:
python --version
pause
