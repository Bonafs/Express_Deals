#!/usr/bin/env python3
"""
Update all Heroku URLs in documentation files
"""
import os
import re
import glob

# Set working directory
project_dir = r"c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
os.chdir(project_dir)

print("🔄 UPDATING HEROKU URLS IN ALL DOCUMENTATION FILES")
print("=" * 60)

# Old and new URLs
old_url = "https://express-deals.herokuapp.com"
new_url = "https://express-deals-16b6c1fa4311.herokuapp.com"

# Find all markdown files
md_files = glob.glob("**/*.md", recursive=True)

updated_files = []

for file_path in md_files:
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if old URL exists in file
        if old_url in content:
            # Replace all instances
            updated_content = content.replace(old_url, new_url)
            
            # Write updated content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            updated_files.append(file_path)
            print(f"✅ Updated: {file_path}")
    
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")

print(f"\n📊 SUMMARY:")
print(f"Files updated: {len(updated_files)}")
print(f"Old URL: {old_url}")
print(f"New URL: {new_url}")

if updated_files:
    print(f"\n📄 Updated files:")
    for file in updated_files:
        print(f"  - {file}")

print(f"\n🎯 All Heroku URLs updated successfully!")
