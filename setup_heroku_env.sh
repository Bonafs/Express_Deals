#!/bin/bash
# Heroku Environment Variables Setup Script
# Run this script to set up your production environment variables on Heroku

echo "🚀 Setting up Heroku Environment Variables for Express Deals"
echo "==========================================================="

# Note: Replace the placeholder values with your actual credentials before running

echo "Setting Django configuration..."
heroku config:set SECRET_KEY="REPLACE_WITH_YOUR_DJANGO_SECRET_KEY" --app express-deals-16b6c1fa4311
heroku config:set DEBUG=False --app express-deals-16b6c1fa4311

echo "Setting Email configuration..."
heroku config:set EMAIL_HOST_USER="REPLACE_WITH_YOUR_EMAIL" --app express-deals-16b6c1fa4311
heroku config:set EMAIL_HOST_PASSWORD="REPLACE_WITH_YOUR_EMAIL_PASSWORD" --app express-deals-16b6c1fa4311
heroku config:set DEFAULT_FROM_EMAIL="Express Deals <REPLACE_WITH_YOUR_EMAIL>" --app express-deals-16b6c1fa4311

echo "Setting Twilio SMS configuration..."
heroku config:set TWILIO_ACCOUNT_SID="REPLACE_WITH_YOUR_TWILIO_SID" --app express-deals-16b6c1fa4311
heroku config:set TWILIO_AUTH_TOKEN="REPLACE_WITH_YOUR_TWILIO_TOKEN" --app express-deals-16b6c1fa4311
heroku config:set TWILIO_PHONE_NUMBER="REPLACE_WITH_YOUR_TWILIO_PHONE" --app express-deals-16b6c1fa4311

echo "Setting WhatsApp configuration..."
heroku config:set WHATSAPP_ACCESS_TOKEN="REPLACE_WITH_YOUR_WHATSAPP_TOKEN" --app express-deals-16b6c1fa4311
heroku config:set WHATSAPP_PHONE_NUMBER_ID="REPLACE_WITH_YOUR_WHATSAPP_PHONE_ID" --app express-deals-16b6c1fa4311
heroku config:set WHATSAPP_VERIFY_TOKEN="REPLACE_WITH_YOUR_WHATSAPP_VERIFY_TOKEN" --app express-deals-16b6c1fa4311

echo "✅ Environment variables setup complete!"
echo "🔄 Your app will automatically restart with the new configuration."
echo ""
echo "To verify the configuration, run:"
echo "heroku config --app express-deals-16b6c1fa4311"
