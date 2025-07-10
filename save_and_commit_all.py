#!/usr/bin/env python3
"""
Save all unsaved files and commit to git
"""
import os
import subprocess
import sys

def run_git_command(cmd):
    """Run a git command and return output"""
    try:
        full_cmd = f"git {cmd}"
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, 
                              cwd="c:\\Users\\BONAFS\\OneDrive\\Documents\\Express_Deals\\Express_Deals")
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("💾 SAVING ALL FILES AND COMMITTING TO GIT")
    print("=" * 50)
    
    os.chdir("c:\\Users\\BONAFS\\OneDrive\\Documents\\Express_Deals\\Express_Deals")
    print(f"📁 Working in: {os.getcwd()}")
    
    # Add all files to staging
    print("\n📦 Adding all files to staging...")
    stdout, stderr, code = run_git_command("add -A")
    if code == 0:
        print("✅ All files added to staging")
    else:
        print(f"❌ Error adding files: {stderr}")
    
    # Check what's staged
    print("\n📋 Checking staged files...")
    stdout, stderr, code = run_git_command("diff --cached --name-only")
    if stdout:
        print("📄 Files to be committed:")
        for file in stdout.split('\n'):
            if file.strip():
                print(f"  - {file}")
    else:
        print("ℹ️ No files to commit")
    
    # Check status
    print("\n📊 Git status:")
    stdout, stderr, code = run_git_command("status --porcelain")
    if stdout:
        print("🔄 Files with changes:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  {line}")
        
        # Commit the changes
        print("\n💾 Committing changes...")
        commit_msg = "Final commit: Save unsaved files and complete project deployment"
        stdout, stderr, code = run_git_command(f'commit -m "{commit_msg}"')
        if code == 0:
            print(f"✅ Successfully committed with message: '{commit_msg}'")
        else:
            print(f"❌ Error committing: {stderr}")
            
        # Push to GitHub
        print("\n🌐 Pushing to GitHub...")
        stdout, stderr, code = run_git_command("push origin main")
        if code == 0:
            print("✅ Successfully pushed to GitHub")
        else:
            print(f"❌ Error pushing: {stderr}")
            
    else:
        print("✅ Working tree is clean - no changes to commit")
    
    print("\n" + "=" * 50)
    print("🎯 ALL FILES SAVED AND COMMITTED!")

if __name__ == "__main__":
    main()
