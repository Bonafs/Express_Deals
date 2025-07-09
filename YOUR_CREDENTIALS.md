# 🔐 EXPRESS DEALS - YOUR SECURE ACCESS GUIDE

## 🏛️ ADMIN ACCESS (Django Administration)

**Access URL:** http://localhost:8000/admin/

**Administrator Account:**
- **Username:** `admin`
- **Password:** `SecureAdmin2024!@#$`
- **Email:** `admin@expressdeals.local`

**What you can do:**
- Manage all products and categories
- View and process all orders
- Manage user accounts
- Configure site settings
- Monitor system activity

---

## 👥 CUSTOMER TEST ACCOUNTS

**Login URL:** http://localhost:8000/accounts/login/

### Customer 1: Emma Watson
- **Username:** `customer1`
- **Password:** `TestUser2024!`
- **Email:** `customer1@expressdeals.local`
- **Location:** London, Greater London
- **Address:** 123 Baker Street, NW1 6XE
- **Phone:** +44 20 7946 0958

### Customer 2: James Smith
- **Username:** `customer2`
- **Password:** `TestUser2024!`
- **Email:** `customer2@expressdeals.local`
- **Location:** Manchester, Greater Manchester
- **Address:** 456 Oxford Road, M1 5GD
- **Phone:** +44 161 123 4567

### Staff Member: Sarah Johnson
- **Username:** `manager`
- **Password:** `TestUser2024!`
- **Email:** `manager@expressdeals.local`
- **Location:** London, Greater London
- **Address:** 789 Regent Street, W1B 4LB
- **Phone:** +44 20 7123 4567
- **Role:** Staff Member (can access staff areas)

---

## 🚀 QUICK START GUIDE

### 1. Start Your Development Server
```bash
cd "c:\Users\BONAFS\OneDrive\Documents\Express_Deals\Express_Deals"
python manage.py runserver
```

### 2. Access Your Site
- **Main Website:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin/
- **User Login:** http://localhost:8000/accounts/login/
- **User Registration:** http://localhost:8000/accounts/register/

### 3. Test the Platform
1. **As Admin:** Login to admin panel and manage products/orders
2. **As Customer:** Register new account or login with test accounts
3. **Shopping:** Browse products, add to cart, and complete checkout
4. **UK Features:** All prices in GBP, UK addresses supported

---

## 🛡️ SECURITY NOTES

### ✅ What's Secure:
- All sensitive credentials are in `credentials.py` (excluded from Git)
- Passwords are randomly generated and complex
- Local development uses SQLite (no external database required)
- All sample data uses UK formatting and GBP currency

### ⚠️ Important Reminders:
- These are **LOCAL DEVELOPMENT** credentials only
- Never commit `credentials.py` to version control
- For production, use environment variables
- Store these credentials in a secure password manager

### 🔄 Production Deployment:
- Use Heroku environment variables for production
- Database, Redis, and other services configured separately
- All production credentials should be different from these

---

## 📋 QUICK REFERENCE

| Function | URL | Credentials |
|----------|-----|-------------|
| Admin Panel | `/admin/` | admin / SecureAdmin2024!@#$ |
| Customer Login | `/accounts/login/` | customer1 / TestUser2024! |
| Staff Access | `/accounts/login/` | manager / TestUser2024! |
| Registration | `/accounts/register/` | Create new account |

---

## 🔧 Next Steps

1. **Test the Platform:**
   - Start the server: `python manage.py runserver`
   - Login as admin and explore the admin panel
   - Login as customer and test shopping features

2. **Customize Your Site:**
   - Add your own products via admin panel
   - Update site branding and styling
   - Configure payment settings (Stripe keys in credentials.py)

3. **Production Deployment:**
   - Your Heroku app is already configured
   - Environment variables are set for production
   - Follow HEROKU_UPGRADE_COMPLETE.md for final steps

**🎉 Your Express Deals platform is ready for development and testing!**
