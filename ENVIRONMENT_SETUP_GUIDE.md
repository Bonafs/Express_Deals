# 🔧 EXPRESS DEALS - ENVIRONMENT SETUP GUIDE

## Current Situation
Your Express Deals project has a virtual environment in the `env/` directory, but the system is looking for `.venv`. Let's fix this and ensure all packages are installed correctly.

## Step-by-Step Environment Setup

### 1. Open PowerShell as Administrator
```powershell
# Navigate to your project directory
cd "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
```

### 2. Activate the Existing Virtual Environment
```powershell
# Activate the environment in the 'env' folder
.\env\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Verify Environment is Active
```powershell
# Check Python version and location
python --version
where python

# Should show path like: C:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals\env\Scripts\python.exe
```

### 4. Upgrade Pip and Install Requirements
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify specific packages
pip show djangorestframework
pip show django
pip show celery
```

### 5. Test REST Framework Installation
```powershell
# Quick test
python -c "import rest_framework; print('REST Framework version:', rest_framework.VERSION)"

# Comprehensive test
python verify_environment.py
```

### 6. Run Django System Check
```powershell
# Check for any configuration issues
python manage.py check

# Check deployment readiness
python manage.py check --deploy
```

## Alternative: Create New Virtual Environment

If the existing environment has issues, create a fresh one:

```powershell
# Remove old environment (if needed)
Remove-Item -Recurse -Force env

# Create new virtual environment
python -m venv env

# Activate it
.\env\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

## Automated Setup Scripts

Run one of these automated setup scripts:

### PowerShell Script:
```powershell
.\setup_environment.ps1
```

### Batch Script:
```cmd
setup_environment.bat
```

## Verification Commands

After setup, run these to verify everything works:

```powershell
# 1. Environment verification
python verify_environment.py

# 2. Django REST Framework test
python -c "from rest_framework import serializers; print('REST Framework working!')"

# 3. Django system check
python manage.py check

# 4. Test imports
python -c "
import django
import rest_framework
import celery
import channels
import scrapy
print('All major packages imported successfully!')
"
```

## Expected Output

When everything is working correctly, you should see:

```
✅ Django X.X.X installed
✅ REST Framework X.X.X installed  
✅ Celery X.X.X installed
✅ Channels X.X.X installed
✅ Scrapy X.X.X installed
✅ Django REST Framework configured in settings
✅ Django configuration is valid
🚀 Express Deals environment is ready for production!
```

## Troubleshooting

### If you get "ModuleNotFoundError: No module named 'rest_framework'":
1. Make sure virtual environment is activated
2. Run: `pip install djangorestframework`
3. Verify with: `pip show djangorestframework`

### If virtual environment activation fails:
1. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
2. Try activating again: `.\env\Scripts\Activate.ps1`

### If packages won't install:
1. Upgrade pip: `python -m pip install --upgrade pip`
2. Try installing individually: `pip install djangorestframework django celery`

## Next Steps After Environment Setup

1. ✅ Verify all packages installed
2. ✅ Run Django system checks  
3. ✅ Test REST Framework import
4. 🚀 Commit all changes to git
5. 🌐 Push to GitHub
6. 🎯 Deploy to production

Your Express Deals platform will be production-ready once the environment is properly configured!
