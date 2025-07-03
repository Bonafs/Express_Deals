# 🎯 EXPRESS DEALS - STEP-BY-STEP ENVIRONMENT SETUP GUIDE

## 📋 **COMPLETE WALKTHROUGH - FOLLOW THESE EXACT STEPS**

### 🚀 **STEP 1: Open PowerShell as Administrator**

1. **Press `Windows + X`** and select **"Windows PowerShell (Admin)"**
2. **OR** Press `Windows + R`, type `powershell`, then press `Ctrl + Shift + Enter`

### 🚀 **STEP 2: Navigate to Your Project**

```powershell
cd "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
```

**Expected Output:** You should see your prompt change to the project directory.

### 🚀 **STEP 3: Check if Virtual Environment Exists**

```powershell
ls env
```

**Expected Output:** You should see folders like `Scripts`, `Lib`, `Include`, etc.

### 🚀 **STEP 4: Set Execution Policy (if needed)**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**When prompted, type `Y` and press Enter.**

### 🚀 **STEP 5: Activate Virtual Environment**

```powershell
.\env\Scripts\Activate.ps1
```

**Expected Output:** Your prompt should change to show `(env)` at the beginning.

### 🚀 **STEP 6: Verify Python Location**

```powershell
python --version
where python
```

**Expected Output:**
```
Python 3.x.x
C:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals\env\Scripts\python.exe
```

### 🚀 **STEP 7: Upgrade Pip**

```powershell
python -m pip install --upgrade pip
```

**Expected Output:** Pip upgrade messages and "Successfully installed pip-x.x.x"

### 🚀 **STEP 8: Install All Requirements**

```powershell
pip install -r requirements.txt
```

**Expected Output:** Long list of package installations ending with "Successfully installed..."

### 🚀 **STEP 9: Verify Key Packages**

**Test Django:**
```powershell
python -c "import django; print('Django version:', django.get_version())"
```

**Test REST Framework:**
```powershell
python -c "import rest_framework; print('REST Framework version:', rest_framework.VERSION)"
```

**Test Celery:**
```powershell
python -c "import celery; print('Celery version:', celery.__version__)"
```

**Test Channels:**
```powershell
python -c "import channels; print('Channels version:', channels.__version__)"
```

**Expected Output for each:** Version numbers without errors.

### 🚀 **STEP 10: Run Comprehensive Environment Check**

```powershell
python verify_environment.py
```

**Expected Output:**
```
🚀 Express Deals - Environment Verification
==================================================
🐍 Python Version: 3.x.x
📍 Python Executable: C:\Users\BONAFS\...\env\Scripts\python.exe

🔍 Checking Required Packages:
✅ django: X.X.X
✅ rest_framework: X.X.X
✅ celery: X.X.X
✅ channels: X.X.X
... (more packages)

🎉 All required packages are installed!
🚀 Express Deals environment is ready for production!
```

### 🚀 **STEP 11: Run Django System Check**

```powershell
python manage.py check
```

**Expected Output:**
```
System check identified no issues (0 silenced).
```

### 🚀 **STEP 12: Test Django REST Framework Import**

```powershell
python -c "from rest_framework import serializers; print('✅ REST Framework working perfectly!')"
```

**Expected Output:**
```
✅ REST Framework working perfectly!
```

### 🚀 **STEP 13: Run the Server (Optional Test)**

```powershell
python manage.py runserver
```

**Expected Output:** Development server starting without errors. Press `Ctrl+C` to stop.

## 🎯 **ALTERNATIVE: Run Automated Scripts**

If you prefer automated setup, run these scripts:

### **PowerShell Automated Setup:**
```powershell
.\setup_environment.ps1
```

### **Batch File Setup:**
```cmd
setup_environment.bat
```

## ✅ **SUCCESS INDICATORS**

You'll know everything is working when you see:

1. ✅ Virtual environment activated (shows `(env)` in prompt)
2. ✅ Python location points to your project's `env\Scripts\python.exe`
3. ✅ All package imports work without errors
4. ✅ Django system check passes
5. ✅ REST Framework imports successfully
6. ✅ Development server starts without issues

## ❌ **TROUBLESHOOTING COMMON ISSUES**

### **Issue: "execution of scripts is disabled"**
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Issue: "ModuleNotFoundError: No module named 'rest_framework'"**
**Solution:**
1. Ensure virtual environment is activated (see `(env)` in prompt)
2. Run: `pip install djangorestframework`
3. Verify: `pip show djangorestframework`

### **Issue: "pip command not found"**
**Solution:**
```powershell
python -m pip install --upgrade pip
```

### **Issue: Virtual environment won't activate**
**Solution:**
1. Delete `env` folder: `Remove-Item -Recurse -Force env`
2. Create new: `python -m venv env`
3. Activate: `.\env\Scripts\Activate.ps1`
4. Install: `pip install -r requirements.txt`

## 🎉 **FINAL VERIFICATION COMMAND**

Run this single command to verify everything:

```powershell
python -c "
import django, rest_framework, celery, channels, scrapy
print('🎉 SUCCESS: All major packages imported!')
print(f'Django: {django.get_version()}')
print(f'REST Framework: {rest_framework.VERSION}')
print(f'Celery: {celery.__version__}')
print('🚀 Express Deals is ready for production!')
"
```

## 📞 **NEXT STEPS AFTER SUCCESSFUL SETUP**

Once all steps complete successfully:

1. **Commit your changes:**
   ```powershell
   git add .
   git commit -m "feat: Environment setup and production upgrade complete"
   git push origin main
   ```

2. **Start development server:**
   ```powershell
   python manage.py runserver
   ```

3. **Access your Express Deals platform:**
   - Main site: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`
   - Alerts: `http://127.0.0.1:8000/alerts/`

**🎯 Follow these steps exactly, and your Express Deals platform will be fully operational with all automation features!**
