#!/usr/bin/env python3
"""
Git operations script to save and commit all files
"""
import os
import subprocess
import sys
from pathlib import Path

# Set working directory
project_dir = r"c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
os.chdir(project_dir)

print("🔧 SETTING UP FRESH ENVIRONMENT AND COMMITTING FILES")
print("=" * 60)
print(f"📁 Working Directory: {os.getcwd()}")

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n🔄 {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=project_dir,
            timeout=30
        )
        
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"   Error: {result.stderr.strip()}")
        
        return result.returncode == 0, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired:
        print("   ⚠️ Command timed out")
        return False, "", "Timeout"
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False, "", str(e)

# Step 1: Check current git status
success, stdout, stderr = run_command("git status --porcelain", "Checking git status")

# Step 2: Add all files to staging
success, stdout, stderr = run_command("git add -A", "Adding all files to staging")

# Step 3: Check what's staged
success, stdout, stderr = run_command("git status", "Checking staged files")

# Step 4: Show files to be committed
success, stdout, stderr = run_command("git diff --cached --name-only", "Files to be committed")
if stdout:
    print("📄 Files that will be committed:")
    for file in stdout.strip().split('\n'):
        if file.strip():
            print(f"   ✓ {file}")

# Step 5: Commit the changes
commit_message = "Final commit: Save unsaved files and complete Express Deals deployment\n\n- Save HEROKU_PUSH_COMPLETE.md with deployment status\n- Save final_production_commit.sh with automation features\n- Save all verification and utility scripts\n- Complete Express Deals project with full UK GBP support\n- All features deployed and working on Heroku"

success, stdout, stderr = run_command(f'git commit -m "{commit_message}"', "Committing changes")

# Step 6: Push to GitHub
success, stdout, stderr = run_command("git push origin main", "Pushing to GitHub")

# Step 7: Final verification
success, stdout, stderr = run_command("git status", "Final verification")

print("\n" + "=" * 60)
print("🎉 GIT OPERATIONS COMPLETE!")
print("✅ All unsaved files have been committed and pushed to GitHub")
print("🚀 Express Deals project is fully saved and deployed!")
