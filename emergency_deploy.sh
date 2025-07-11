#!/bin/bash
# Express Deals Emergency Deployment Script
echo "=== EXPRESS DEALS EMERGENCY DEPLOYMENT ==="

# Navigate to project directory
cd "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"

# Activate virtual environment
source .venv/Scripts/activate

# Check current status
echo "Current directory: $(pwd)"
echo "Git status:"
git status

# Stage all changes
echo "Staging all changes..."
git add -A

# Commit with timestamp
echo "Committing changes..."
git commit -m "EMERGENCY DEPLOYMENT: Express Deals fixes - $(date)"

# Push to origin
echo "Pushing to GitHub..."
git push origin main

# Setup Heroku remote
echo "Setting up Heroku remote..."
heroku git:remote -a express-deals

# Force push to Heroku
echo "FORCE PUSHING TO HEROKU..."
git push heroku main --force

# Run migrations
echo "Running migrations..."
heroku run python manage.py migrate --app express-deals

# Collect static files
echo "Collecting static files..."
heroku run python manage.py collectstatic --noinput --app express-deals

# Check status
echo "Checking deployment status..."
heroku ps --app express-deals

echo "=== DEPLOYMENT COMPLETE ==="
echo "Check your site at: https://express-deals-16b6c1fa4311.herokuapp.com/"
