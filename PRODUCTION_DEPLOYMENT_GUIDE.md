# 🚀 EXPRESS DEALS - HEROKU PRODUCTION DEPLOYMENT GUIDE

## 📋 **COMPLETE HEROKU DEPLOYMENT WALKTHROUGH**

**Last Updated:** July 7, 2025  
**Status:** Production Ready  
**Deployment Method:** Heroku Cloud Platform

---

## 🎯 **HEROKU DEPLOYMENT - STEP BY STEP**

### **✅ REQUIREMENTS CHECKLIST**

Before starting, ensure you have:
- [ ] **Heroku Account** - [signup.heroku.com](https://signup.heroku.com)
- [ ] **Stripe Account** - [dashboard.stripe.com](https://dashboard.stripe.com)
- [ ] **SendGrid Account** - [sendgrid.com](https://sendgrid.com) (for emails)
- [ ] **Git** installed and configured
- [ ] **Heroku CLI** installed

---

## 🚀 **STEP 1: Install Heroku CLI**

**Download and Install:**
1. Go to [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Download the installer for Windows
3. Run the installer as Administrator
4. Restart PowerShell after installation

**Verify Installation:**
```powershell
heroku --version
# Should show: heroku/x.x.x win32-x64 node-vx.x.x
```

---

## 🚀 **STEP 2: Login to Heroku**

```powershell
heroku login
```
This will open your browser for authentication.

---

## 🚀 **STEP 3: Create Heroku Application**

```powershell
# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create express-deals-production

# Set up Git remote
heroku git:remote -a express-deals-production
```

**Note:** Heroku app names must be globally unique. If 'express-deals-production' is taken, try:
- `express-deals-[your-name]`
- `express-deals-2025`
- `[your-name]-express-deals`

---

## 🚀 **STEP 4: Add Heroku Add-ons**

```powershell
# Add PostgreSQL database
heroku addons:create heroku-postgresql:essential-0

# Add Redis for Celery
heroku addons:create heroku-redis:essential-0

# Verify add-ons
heroku addons
```

---

## 🚀 **STEP 5: Set Environment Variables**

**Generate a Secure Secret Key:**
```powershell
python -c "
import secrets
print('DJANGO_SECRET_KEY=' + secrets.token_urlsafe(50))
"
```

**Set Required Environment Variables:**
```powershell
# Django Settings
heroku config:set SECRET_KEY="your-generated-secret-key-here"
heroku config:set DJANGO_SETTINGS_MODULE="express_deals.heroku_settings"

# Email Configuration (SendGrid)
heroku config:set SENDGRID_API_KEY="your-sendgrid-api-key"
heroku config:set DEFAULT_FROM_EMAIL="noreply@your-domain.com"

# Payment Configuration (Stripe)
heroku config:set STRIPE_PUBLISHABLE_KEY="pk_live_your-stripe-key"
heroku config:set STRIPE_SECRET_KEY="sk_live_your-stripe-secret"

# Twilio Configuration (optional)
heroku config:set TWILIO_ACCOUNT_SID="your-twilio-sid"
heroku config:set TWILIO_AUTH_TOKEN="your-twilio-token"
heroku config:set TWILIO_PHONE_NUMBER="+1234567890"

# Monitoring (optional)
heroku config:set SENTRY_DSN="your-sentry-dsn"
```

**Verify Configuration:**
```powershell
heroku config
```

---

## 🚀 **STEP 6: Prepare Files for Deployment**

**Files Already Created:**
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Updated with gunicorn
- ✅ `express_deals/heroku_settings.py` - Production settings

**Verify Files Exist:**
```powershell
# Check that these files exist
ls Procfile
ls runtime.txt
ls express_deals/heroku_settings.py
```

---

## 🚀 **STEP 7: Deploy to Heroku**

**Initial Deployment:**
```powershell
# Add all files to git
git add .
git commit -m "feat: Heroku production deployment configuration"

# Deploy to Heroku
git push heroku main
```

**Expected Output:** You should see build logs showing:
- Python installation
- Dependency installation
- Static file collection
- "Build succeeded" message

---

## 🚀 **STEP 8: Run Database Migrations**

```powershell
# Run database migrations
heroku run python manage.py migrate

# Create a superuser
heroku run python manage.py createsuperuser

# Collect static files (if needed)
heroku run python manage.py collectstatic --noinput
```

---

## 🚀 **STEP 9: Scale Workers**

```powershell
# Scale web processes
heroku ps:scale web=1

# Scale Celery workers (for background tasks)
heroku ps:scale worker=1

# Scale Celery beat (for scheduled tasks)
heroku ps:scale beat=1
```

---

## 🚀 **STEP 10: Verify Deployment**

**Check Application Status:**
```powershell
# View app status
heroku ps

# View recent logs
heroku logs --tail

# Open your application
heroku open
```

**Test Key Functionality:**
1. **Main Site:** Visit your Heroku URL
2. **Admin Panel:** `/admin/` - Login with superuser
3. **API Endpoints:** Test REST API endpoints
4. **Background Tasks:** Verify Celery is working

---

## 🔒 **SECURITY CONFIGURATION**

### **SSL/HTTPS Setup**
Heroku automatically provides SSL for `.herokuapp.com` domains. For custom domains:

```powershell
# Add custom domain
heroku domains:add www.your-domain.com

# Enable Automated Certificate Management
heroku certs:auto:enable
```

### **Security Headers**
Already configured in `heroku_settings.py`:
- ✅ SECURE_SSL_REDIRECT
- ✅ SESSION_COOKIE_SECURE  
- ✅ CSRF_COOKIE_SECURE
- ✅ SECURE_HSTS_SECONDS

---

## 📊 **MONITORING & LOGS**

### **View Application Logs**
```powershell
# Real-time logs
heroku logs --tail

# Recent logs
heroku logs --num=200

# Filter by component
heroku logs --source=app
heroku logs --source=heroku
```

### **Monitor Resource Usage**
```powershell
# Check dyno status
heroku ps

# View app metrics
heroku run top
```

---

## 🔄 **ONGOING DEPLOYMENT**

### **Deploy Updates**
```powershell
# After making changes
git add .
git commit -m "feat: your update description"
git push heroku main

# Run migrations if needed
heroku run python manage.py migrate
```

### **Environment Variables Updates**
```powershell
# Update a config variable
heroku config:set VARIABLE_NAME="new_value"

# Remove a config variable
heroku config:unset VARIABLE_NAME
```

---

## 🎯 **CUSTOM DOMAIN SETUP**

### **Add Your Domain**
```powershell
# Add custom domain
heroku domains:add your-domain.com
heroku domains:add www.your-domain.com

# View DNS targets
heroku domains
```

### **Configure DNS**
In your domain registrar's DNS settings:
```
Type: CNAME
Host: www
Value: your-app-name.herokuapp.com

Type: ANAME/ALIAS (or A record)
Host: @
Value: your-dns-target-from-heroku
```

---

## ⚡ **PERFORMANCE OPTIMIZATION**

### **Enable Caching**
Already configured in production settings:
- Redis for sessions and cache
- WhiteNoise for static files
- Database connection pooling

### **Scale Resources**
```powershell
# Scale web dynos
heroku ps:scale web=2

# Upgrade database plan
heroku addons:upgrade heroku-postgresql:standard-0

# Upgrade Redis plan  
heroku addons:upgrade heroku-redis:standard-0
```

---

## 🛠️ **TROUBLESHOOTING**

### **Common Issues & Solutions**

**1. Build Failures**
```powershell
# Check build logs
heroku logs --source=app

# Common fixes:
# - Verify requirements.txt format
# - Check runtime.txt Python version
# - Ensure all files are committed to git
```

**2. Application Errors**
```powershell
# Check application logs
heroku logs --tail

# Run Django check
heroku run python manage.py check --deploy

# Check environment variables
heroku config
```

**3. Database Issues**
```powershell
# Check database connection
heroku pg:info

# Run migrations
heroku run python manage.py migrate

# Access database shell
heroku pg:psql
```

**4. Static Files Issues**
```powershell
# Collect static files
heroku run python manage.py collectstatic --noinput

# Check WhiteNoise configuration
heroku run python manage.py check --deploy
```

### **Debug Mode for Troubleshooting**
```powershell
# Temporarily enable debug (remove after fixing)
heroku config:set DEBUG=True
heroku config:unset DEBUG  # Remove when done
```

---

## 📞 **POST-DEPLOYMENT CHECKLIST**

### **✅ Verify Everything Works**
- [ ] **Main website loads** - `https://your-app.herokuapp.com`
- [ ] **Admin panel accessible** - `/admin/`
- [ ] **User registration/login** works
- [ ] **Payment processing** (test mode)
- [ ] **Email notifications** working
- [ ] **Price alerts** functioning
- [ ] **Background tasks** running
- [ ] **WebSocket features** active
- [ ] **SSL certificate** valid
- [ ] **Mobile responsive** design

### **✅ Security Verification**
- [ ] **DEBUG = False** in production
- [ ] **Secure SECRET_KEY** set
- [ ] **HTTPS enforced**
- [ ] **Security headers** active
- [ ] **Admin panel secured**

### **✅ Performance Checks**
- [ ] **Page load times** < 3 seconds
- [ ] **Database queries** optimized
- [ ] **Static files** serving correctly
- [ ] **Caching** working
- [ ] **Background tasks** processing

---

## 🎉 **SUCCESS! YOUR EXPRESS DEALS PLATFORM IS LIVE**

**Your application is now running at:**
`https://your-app-name.herokuapp.com`

**Admin Panel:**
`https://your-app-name.herokuapp.com/admin/`

**API Documentation:**
`https://your-app-name.herokuapp.com/api/`

---

## 📈 **NEXT STEPS**

1. **Set up monitoring** with Sentry or New Relic
2. **Configure backup strategy** for database
3. **Set up CI/CD pipeline** with GitHub Actions
4. **Add custom domain** and professional email
5. **Configure advanced analytics**
6. **Set up staging environment**

**🎯 Your Express Deals platform is now production-ready and serving customers worldwide!**
New-Item -Path "express_deals\production_settings.py" -ItemType File
```

**Add Production Configuration:**
```python
# express_deals/production_settings.py
from .settings import *
import os

# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database - PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'express_deals_prod'),
        'USER': os.environ.get('DB_USER', 'your_db_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_db_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static Files for Production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Headers
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Email Settings for Production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Stripe Production Keys
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'production.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### **🚀 STEP 2: Update Requirements for Production**

```powershell
# Add production dependencies
pip install gunicorn psycopg2-binary whitenoise
pip freeze > requirements.txt
```

### **🚀 STEP 3: Create Production Runtime Files**

**Create Procfile:**
```powershell
New-Item -Path "Procfile" -ItemType File
```

**Add to Procfile:**
```
web: gunicorn express_deals.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A express_deals worker --loglevel=info
beat: celery -A express_deals beat --loglevel=info
```

**Create runtime.txt:**
```powershell
New-Item -Path "runtime.txt" -ItemType File
```

**Add to runtime.txt:**
```
python-3.13.2
```

### **🚀 STEP 4: Environment Variables Setup**

**Create .env.production (for reference only):**
```bash
# Database
DB_NAME=express_deals_prod
DB_USER=your_production_db_user
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host
DB_PORT=5432

# Email
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password

# Stripe
STRIPE_PUBLIC_KEY=pk_live_your_live_public_key
STRIPE_SECRET_KEY=sk_live_your_live_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_live_webhook_secret

# Security
SECRET_KEY=your_very_long_and_secure_production_secret_key
```

### **🚀 STEP 5: Database Migration & Static Files**

```powershell
# Set production environment
$env:DJANGO_SETTINGS_MODULE = "express_deals.production_settings"

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### **🚀 STEP 6: Production Testing**

```powershell
# Test production settings locally
python manage.py check --settings=express_deals.production_settings

# Test with production server
gunicorn express_deals.wsgi:application --bind 127.0.0.1:8000
```

---

## 🟣 **HEROKU DEPLOYMENT**

### **🚀 STEP 1: Install Heroku CLI**

**Download and Install:**
1. Go to [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Download for Windows
3. Install and restart PowerShell

**Verify Installation:**
```powershell
heroku --version
```

### **🚀 STEP 2: Login to Heroku**

```powershell
heroku login
```

**Expected:** Browser opens for Heroku login

### **🚀 STEP 3: Create Heroku App**

```powershell
# Create new Heroku app
heroku create your-express-deals-app

# OR if you want to specify name
heroku create express-deals-production
```

**Expected Output:**
```
Creating app... done, ⬢ express-deals-production
https://express-deals-production.herokuapp.com/ | https://git.heroku.com/express-deals-production.git
```

### **🚀 STEP 4: Configure Heroku Environment Variables**

```powershell
# Set Django settings module
heroku config:set DJANGO_SETTINGS_MODULE=express_deals.production_settings

# Set secret key (generate a new one for production)
heroku config:set SECRET_KEY="your-very-long-and-secure-production-secret-key"

# Set debug to false
heroku config:set DEBUG=False

# Set allowed hosts
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"

# Email configuration
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-specific-password"

# Stripe configuration (LIVE KEYS for production)
heroku config:set STRIPE_PUBLIC_KEY="pk_live_your_live_public_key"
heroku config:set STRIPE_SECRET_KEY="sk_live_your_live_secret_key"
heroku config:set STRIPE_WEBHOOK_SECRET="whsec_your_live_webhook_secret"
```

### **🚀 STEP 5: Add Heroku PostgreSQL**

```powershell
# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Get database URL
heroku config:get DATABASE_URL
```

### **🚀 STEP 6: Add Redis for Background Tasks**

```powershell
# Add Redis for Celery
heroku addons:create heroku-redis:mini

# Get Redis URL
heroku config:get REDIS_URL
```

### **🚀 STEP 7: Update Settings for Heroku**

**Create heroku_settings.py:**
```python
# express_deals/heroku_settings.py
from .production_settings import *
import dj_database_url

# Database from Heroku
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Redis from Heroku
REDIS_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Allowed hosts for Heroku
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', 'localhost')]
```

**Update Heroku config:**
```powershell
heroku config:set DJANGO_SETTINGS_MODULE=express_deals.heroku_settings
```

### **🚀 STEP 8: Deploy to Heroku**

```powershell
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial production deployment"

# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy to Heroku
git push heroku main
```

### **🚀 STEP 9: Run Database Migrations on Heroku**

```powershell
# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput
```

### **🚀 STEP 10: Open Your Live App**

```powershell
# Open your live application
heroku open

# View logs
heroku logs --tail
```

---

## 🔧 **POST-DEPLOYMENT CONFIGURATION**

### **🚀 SSL Certificate Setup**

**For Heroku:**
```powershell
# Heroku provides SSL automatically
heroku certs:auto:enable
```

**For Custom Domain:**
```powershell
# Add custom domain
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com

# Get DNS target
heroku domains
```

### **🚀 Stripe Webhook Configuration**

1. **Go to [Stripe Dashboard](https://dashboard.stripe.com)**
2. **Navigate to Webhooks**
3. **Add endpoint:** `https://your-app.herokuapp.com/payments/webhook/`
4. **Select events:** `payment_intent.succeeded`, `payment_intent.payment_failed`
5. **Get webhook secret and update:**
   ```powershell
   heroku config:set STRIPE_WEBHOOK_SECRET="whsec_your_new_webhook_secret"
   ```

### **🚀 Email Service Configuration**

**Gmail Setup:**
1. **Enable 2-Factor Authentication**
2. **Generate App Password**
3. **Update Heroku config:**
   ```powershell
   heroku config:set EMAIL_HOST_PASSWORD="your-16-character-app-password"
   ```

**Or SendGrid Setup:**
```powershell
# Add SendGrid addon
heroku addons:create sendgrid:starter

# Get SendGrid credentials
heroku config:get SENDGRID_API_KEY
```

---

## 🧪 **PRODUCTION TESTING CHECKLIST**

### **✅ Functionality Tests**

1. **Basic Site Functions:**
   - [ ] Homepage loads
   - [ ] Product pages display
   - [ ] Shopping cart works
   - [ ] User registration/login
   - [ ] Admin panel accessible

2. **Payment Processing:**
   - [ ] Stripe test payments work
   - [ ] Webhook receives events
   - [ ] Order confirmation emails sent

3. **Notification System:**
   ```powershell
   # Test notifications remotely
   heroku run python notification_status.py
   ```

4. **Performance Tests:**
   - [ ] Page load times < 3 seconds
   - [ ] Database queries optimized
   - [ ] Static files loading fast

### **✅ Security Verification**

```powershell
# Run Django deployment check
heroku run python manage.py check --deploy

# Verify HTTPS redirect
curl -I https://your-app.herokuapp.com
```

---

## 🔍 **MONITORING & MAINTENANCE**

### **📊 Heroku Monitoring**

```powershell
# View application metrics
heroku logs --tail

# Monitor database
heroku pg:info

# Check dyno status
heroku ps

# Scale dynos if needed
heroku ps:scale web=2 worker=1
```

### **📈 Performance Monitoring**

**Add New Relic (Free tier):**
```powershell
heroku addons:create newrelic:wayne
```

**Check application health:**
```powershell
# View app info
heroku apps:info

# Check add-ons
heroku addons
```

---

## ❌ **TROUBLESHOOTING COMMON ISSUES**

### **Issue: Application Error (H10)**
**Solution:**
```powershell
# Check logs
heroku logs --tail

# Verify Procfile
cat Procfile

# Restart dynos
heroku restart
```

### **Issue: Database Connection Error**
**Solution:**
```powershell
# Check database
heroku pg:info

# Reset database (WARNING: Deletes all data)
heroku pg:reset DATABASE_URL --confirm your-app-name
heroku run python manage.py migrate
```

### **Issue: Static Files Not Loading**
**Solution:**
```powershell
# Collect static files
heroku run python manage.py collectstatic --noinput

# Check WhiteNoise configuration
heroku config:get DEBUG
```

### **Issue: Environment Variables Not Set**
**Solution:**
```powershell
# List all config vars
heroku config

# Set missing variables
heroku config:set VARIABLE_NAME="value"
```

---

## 🎯 **FINAL VERIFICATION COMMANDS**

**Complete Production Health Check:**
```powershell
# 1. Check Heroku app status
heroku ps

# 2. View recent logs
heroku logs --tail --num=50

# 3. Test database connection
heroku run python manage.py dbshell

# 4. Verify migrations
heroku run python manage.py showmigrations

# 5. Test admin access
heroku open admin/

# 6. Run system check
heroku run python manage.py check --deploy
```

---

## 📞 **NEXT STEPS AFTER SUCCESSFUL DEPLOYMENT**

1. **Set up monitoring and alerts**
2. **Configure regular database backups**
3. **Set up CI/CD pipeline for updates**
4. **Monitor performance and scale as needed**
5. **Set up domain name and custom DNS**

---

## 🎉 **SUCCESS INDICATORS**

You'll know your production deployment is successful when:

- ✅ **Site loads at your Heroku URL**
- ✅ **HTTPS works (green lock icon)**
- ✅ **Database queries execute**
- ✅ **Admin panel accessible**
- ✅ **Payments process correctly**
- ✅ **Emails send successfully**
- ✅ **No application errors in logs**

**🚀 Congratulations! Your Express Deals platform is now live in production!**

---

*Ready to guide you through each step! Let me know when you want to start and which deployment option you prefer!* 🚀✨
