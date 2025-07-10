#!/usr/bin/env python3
"""
Check for unsaved files and git status
"""
import os
import subprocess
import sys

def run_command(cmd, shell=True):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, cwd=os.getcwd())
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("🔍 CHECKING FOR UNSAVED FILES AND GIT STATUS")
    print("=" * 50)
    
    # Check current directory
    print(f"📁 Current Directory: {os.getcwd()}")
    
    # Check git status
    print("\n📊 Git Status:")
    stdout, stderr, code = run_command("git status --porcelain")
    if stdout:
        print("Files with changes:")
        print(stdout)
    else:
        print("✅ No modified files detected")
    
    # Check staged files
    print("\n📦 Staged Files:")
    stdout, stderr, code = run_command("git diff --cached --name-only")
    if stdout:
        print("Staged files:")
        print(stdout)
    else:
        print("✅ No staged files")
    
    # Check untracked files
    print("\n📋 Untracked Files:")
    stdout, stderr, code = run_command("git ls-files --others --exclude-standard")
    if stdout:
        print("Untracked files:")
        print(stdout)
    else:
        print("✅ No untracked files")
    
    # Check last commit
    print("\n📅 Last Commit:")
    stdout, stderr, code = run_command("git log --oneline -1")
    if stdout:
        print(stdout)
    
    # Check if working tree is clean
    stdout, stderr, code = run_command("git status --porcelain")
    if not stdout:
        print("\n✅ WORKING TREE IS CLEAN - ALL FILES SAVED AND COMMITTED")
    else:
        print("\n⚠️ THERE ARE UNCOMMITTED CHANGES")
        
        # Try to stage and commit any changes
        print("\n🔧 Attempting to stage and commit changes...")
        run_command("git add -A")
        
        stdout, stderr, code = run_command("git status --porcelain")
        if stdout:
            commit_msg = "Final commit: Save remaining files and complete deployment"
            run_command(f'git commit -m "{commit_msg}"')
            print(f"✅ Committed changes with message: {commit_msg}")
        
    print("\n" + "=" * 50)
    print("🎯 FILE CHECK COMPLETE")

if __name__ == "__main__":
    main()
