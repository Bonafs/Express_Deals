# Express Deals Environment Variables for PowerShell
# This file sets environment variables for local development

# Cloudinary Configuration
$env:CLOUDINARY_CLOUD_NAME = "dzecfjfju"
$env:CLOUDINARY_API_KEY = "853483899852935"
$env:CLOUDINARY_API_SECRET = "tFJ6Rb9xofDzV2Y1YrBZWaIZkhs"

# Django Configuration
$env:DEBUG = "True"
$env:SECRET_KEY = "your_secret_key_here"

Write-Host "Express Deals environment variables loaded" -ForegroundColor Green
