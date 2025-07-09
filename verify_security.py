#!/usr/bin/env python
"""
Express Deals - Security Verification Script
Verify that credentials are properly secured and not exposed
"""

import os
import glob


def check_credential_security():
    """Check for potential credential security issues"""
    print("🔍 Express Deals - Security Verification")
    print("=" * 50)
    
    # Check for sensitive files that should be gitignored
    sensitive_patterns = [
        'credentials.py',
        '*_credentials.py',
        '*_secrets.py',
        '.env.local',
        'local_settings.py'
    ]
    
    found_sensitive = []
    for pattern in sensitive_patterns:
        files = glob.glob(pattern)
        if files:
            found_sensitive.extend(files)
    
    if found_sensitive:
        print("⚠️  Found sensitive files (should be in .gitignore):")
        for file in found_sensitive:
            print(f"   📁 {file}")
    else:
        print("✅ No sensitive credential files found in root directory")
    
    # Check if template file exists
    if os.path.exists('credentials.template.py'):
        print("✅ credentials.template.py found (safe for sharing)")
    else:
        print("❌ credentials.template.py missing")
    
    # Check if security documentation exists
    if os.path.exists('SECURITY.md'):
        print("✅ SECURITY.md documentation found")
    else:
        print("❌ SECURITY.md documentation missing")
    
    # Check if .gitignore contains security entries
    try:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            
        security_entries = [
            'credentials.py',
            '*_credentials.py',
            '*_secrets.py'
        ]
        
        missing_entries = []
        for entry in security_entries:
            if entry not in gitignore_content:
                missing_entries.append(entry)
        
        if missing_entries:
            print("⚠️  Missing .gitignore entries:")
            for entry in missing_entries:
                print(f"   📝 {entry}")
        else:
            print("✅ .gitignore properly configured for security")
            
    except FileNotFoundError:
        print("❌ .gitignore file not found")
    
    # Check for old insecure scripts
    old_scripts = [
        'create_superuser.py',
        'create_sample_users.py'
    ]
    
    found_old = []
    for script in old_scripts:
        if os.path.exists(script):
            found_old.append(script)
    
    if found_old:
        print("⚠️  Found old insecure scripts (should be removed):")
        for script in found_old:
            print(f"   📜 {script}")
    else:
        print("✅ Old insecure scripts properly removed")
    
    # Check for new secure scripts
    secure_scripts = [
        'create_secure_superuser.py',
        'create_secure_sample_users.py'
    ]
    
    missing_secure = []
    for script in secure_scripts:
        if not os.path.exists(script):
            missing_secure.append(script)
    
    if missing_secure:
        print("❌ Missing secure scripts:")
        for script in missing_secure:
            print(f"   📜 {script}")
    else:
        print("✅ Secure user creation scripts available")
    
    print("\n🛡️ Security Status Summary:")
    print("=" * 50)
    
    all_good = (
        not found_sensitive and
        not missing_entries and
        not found_old and
        not missing_secure and
        os.path.exists('credentials.template.py') and
        os.path.exists('SECURITY.md')
    )
    
    if all_good:
        print("🎉 All security checks passed!")
        print("✅ Credentials are properly secured")
        print("✅ No sensitive data exposed to version control")
        print("✅ Secure user creation system implemented")
    else:
        print("⚠️  Some security issues found - please review above")
    
    print(f"\n📚 Read SECURITY.md for detailed setup instructions")
    
    return all_good


if __name__ == '__main__':
    check_credential_security()
