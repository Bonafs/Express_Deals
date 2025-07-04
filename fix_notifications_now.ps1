Write-Host "🚨 URGENT NOTIFICATION MODULE FIX" -ForegroundColor Red
Write-Host "================================"

Write-Host "`n1️⃣ Checking virtual environments..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "✅ .venv directory found" -ForegroundColor Green
} else {
    Write-Host "❌ .venv not found - creating it now..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ .venv created" -ForegroundColor Green
}

Write-Host "`n2️⃣ Activating .venv..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

Write-Host "`n3️⃣ Installing django-notifications-hq..." -ForegroundColor Yellow
pip install django-notifications-hq==1.8.3

Write-Host "`n4️⃣ Installing all requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n5️⃣ Testing notification import..." -ForegroundColor Yellow
$notificationTest = python -c "
try:
    import notifications
    print('✅ notifications module working')
    print('Version:', notifications.__version__)
except Exception as e:
    print('❌ Import failed:', str(e))
    exit(1)
" 2>&1

Write-Host $notificationTest

Write-Host "`n6️⃣ Testing Django setup..." -ForegroundColor Yellow
$djangoTest = python -c "
try:
    import os, django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
    django.setup()
    from scraping.notifications import NotificationService
    print('✅ NotificationService imported successfully')
    service = NotificationService()
    print('✅ NotificationService initialized successfully')
except Exception as e:
    print('❌ Django test failed:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)
" 2>&1

Write-Host $djangoTest

Write-Host "`n7️⃣ Running migrations..." -ForegroundColor Yellow
python manage.py makemigrations 2>&1
python manage.py migrate 2>&1

Write-Host "`n🎉 NOTIFICATION MODULE FIX COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "To test, run:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python manage.py shell" -ForegroundColor White
Write-Host "  from scraping.notifications import NotificationService" -ForegroundColor White

Write-Host "`nPress any key to continue..." -ForegroundColor Yellow
Read-Host
