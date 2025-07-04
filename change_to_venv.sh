#!/bin/bash
# Script to change virtual environment from 'env' to '.venv'

echo "🔄 Changing virtual environment from 'env' to '.venv'"
echo "================================================"

# Create new virtual environment with .venv name
echo "📦 Creating new .venv virtual environment..."
python -m venv .venv

echo "✅ New .venv virtual environment created"

# Activate the new environment and install requirements
echo "🔄 Activating .venv and installing requirements..."
source .venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Requirements installed in .venv"

# Update .gitignore to include .venv
echo "📝 Updating .gitignore..."
if ! grep -q ".venv" .gitignore 2>/dev/null; then
    echo ".venv/" >> .gitignore
    echo "# Virtual environment" >> .gitignore
fi

echo "✅ .gitignore updated"

echo "🎉 Virtual environment successfully changed to .venv!"
echo ""
echo "💡 Next steps:"
echo "1. Delete the old 'env' directory: rm -rf env"
echo "2. Update any IDE/editor settings to use .venv"
echo "3. Use: .venv/Scripts/activate.ps1 (Windows) or source .venv/bin/activate (Linux/Mac)"
