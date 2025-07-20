#!/usr/bin/env python
"""
Express Deals Heroku Deployment Verification
Direct check of the transaction ID fix and deployment status
"""

import os
import sys
import subprocess
import requests
from datetime import datetime

# Configuration
HEROKU_APP_URL = "https://express-deals-16b6c1fa4311.herokuapp.com"
ADMIN_URL = f"{HEROKU_APP_URL}/admin/"

def run_command(command):
    """Run a shell command and return the output"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1

def check_app_accessibility():
    """Check if the Heroku app is accessible"""
    print("🌐 CHECKING APP ACCESSIBILITY...")
    try:
        response = requests.get(HEROKU_APP_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ App is accessible at {HEROKU_APP_URL}")
            return True
        else:
            print(f"⚠️  App returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ App is not accessible: {e}")
        return False

def check_admin_panel():
    """Check if admin panel is accessible"""
    print("🔐 CHECKING ADMIN PANEL...")
    try:
        response = requests.get(ADMIN_URL, timeout=10)
        if response.status_code in [200, 302]:  # 302 is redirect to login
            print("✅ Admin panel is accessible")
            return True
        else:
            print(f"⚠️  Admin panel returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Admin panel error: {e}")
        return False

def check_heroku_status():
    """Check Heroku deployment status"""
    print("🚀 CHECKING HEROKU DEPLOYMENT STATUS...")
    
    # Check dyno status
    stdout, stderr, returncode = run_command("heroku ps --app express-deals")
    if returncode == 0 and stdout:
        print("📊 DYNO STATUS:")
        print(stdout)
    else:
        print(f"⚠️  Could not get dyno status: {stderr}")
    
    # Check recent releases
    stdout, stderr, returncode = run_command("heroku releases --app express-deals -n 3")
    if returncode == 0 and stdout:
        print("📋 RECENT RELEASES:")
        print(stdout)
    else:
        print(f"⚠️  Could not get releases: {stderr}")

def fix_transaction_ids():
    """Run the transaction ID fix command on Heroku"""
    print("🔧 RUNNING TRANSACTION ID FIX...")
    
    stdout, stderr, returncode = run_command('heroku run "python manage.py fix_transaction_ids" --app express-deals')
    
    if returncode == 0:
        print("✅ Transaction ID fix completed successfully:")
        print(stdout)
        return True
    else:
        print(f"❌ Transaction ID fix failed: {stderr}")
        return False

def run_migrations():
    """Run Django migrations on Heroku"""
    print("📊 RUNNING MIGRATIONS...")
    
    stdout, stderr, returncode = run_command('heroku run "python manage.py migrate" --app express-deals')
    
    if returncode == 0:
        print("✅ Migrations completed successfully:")
        print(stdout)
        return True
    else:
        print(f"❌ Migrations failed: {stderr}")
        return False

def check_logs():
    """Check recent application logs"""
    print("📋 CHECKING RECENT LOGS...")
    
    stdout, stderr, returncode = run_command("heroku logs --app express-deals -n 10")
    
    if returncode == 0 and stdout:
        print("📝 RECENT LOGS:")
        print(stdout)
        
        # Look for specific error patterns
        if "IntegrityError" in stdout or "transaction_id" in stdout:
            print("⚠️  Transaction ID issues detected in logs")
            return False
        else:
            print("✅ No transaction ID errors in recent logs")
            return True
    else:
        print(f"⚠️  Could not retrieve logs: {stderr}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("🚀 EXPRESS DEALS HEROKU DEPLOYMENT VERIFICATION")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'app_accessible': False,
        'admin_accessible': False,
        'transaction_fix': False,
        'migrations': False,
        'logs_clean': False
    }
    
    # Step 1: Check app accessibility
    results['app_accessible'] = check_app_accessibility()
    print()
    
    # Step 2: Check admin panel
    results['admin_accessible'] = check_admin_panel()
    print()
    
    # Step 3: Check Heroku status
    check_heroku_status()
    print()
    
    # Step 4: Fix transaction IDs
    results['transaction_fix'] = fix_transaction_ids()
    print()
    
    # Step 5: Run migrations
    results['migrations'] = run_migrations()
    print()
    
    # Step 6: Check logs
    results['logs_clean'] = check_logs()
    print()
    
    # Summary
    print("=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    for check, status in results.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {check.replace('_', ' ').title()}: {'PASSED' if status else 'FAILED'}")
    
    passed_checks = sum(results.values())
    total_checks = len(results)
    
    print()
    print(f"🎯 OVERALL SCORE: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 ALL SYSTEMS OPERATIONAL - DEPLOYMENT SUCCESSFUL!")
        print("💰 Ready for production revenue generation!")
    elif passed_checks >= 3:
        print("⚠️  PARTIAL SUCCESS - Some issues detected but core functionality working")
    else:
        print("❌ CRITICAL ISSUES - Deployment needs attention")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
