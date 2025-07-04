# EXPRESS DEALS - WHATSAPP INTEGRATION SETUP GUIDE

## 🎯 **WHATSAPP CONFIGURATION WITHOUT .ENV FILES**

Express Deals uses hardcoded configuration in `settings.py` instead of `.env` files for WhatsApp integration.

---

## 📱 **WHATSAPP BUSINESS API SETUP**

### **Step 1: Facebook Developer Account Setup**

1. **Create Facebook Developer Account**
   - Go to: https://developers.facebook.com/
   - Sign up or login with your Facebook account
   - Verify your account with phone number

2. **Create New App**
   - Click "Create App"
   - Choose "Business" as app type
   - Enter app name: "Express Deals WhatsApp"
   - Enter contact email
   - Click "Create App"

3. **Add WhatsApp Product**
   - In app dashboard, click "Add Product"
   - Find "WhatsApp" and click "Set Up"
   - Follow the setup wizard

### **Step 2: WhatsApp Business Account**

1. **Business Verification**
   - Provide business information
   - Upload business documents
   - Wait for verification (can take 24-48 hours)

2. **Phone Number Setup**
   - Add and verify your business phone number
   - This will be your WhatsApp sender number
   - Note the Phone Number ID

3. **Get Access Token**
   - Generate permanent access token
   - Copy the access token (starts with "EAA...")
   - Keep this secure - it's your API key

---

## ⚙️ **EXPRESS DEALS CONFIGURATION**

### **Step 3: Update Django Settings**

Edit `express_deals/settings.py` directly (no .env file needed):

```python
# WhatsApp Configuration (Production - update with your values)
WHATSAPP_API_URL = 'https://api.whatsapp.com/send'
WHATSAPP_BUSINESS_API_URL = 'https://graph.facebook.com/v17.0'
WHATSAPP_ACCESS_TOKEN = 'EAAYourLongAccessTokenHere'  # Your actual token
WHATSAPP_PHONE_NUMBER_ID = '1234567890123456'  # Your phone number ID
WHATSAPP_VERIFY_TOKEN = 'express_deals_production_webhook'  # Custom token

# Enable WhatsApp functionality
WHATSAPP_ENABLED = True  # Set to True when configured

# WhatsApp Rate Limiting
WHATSAPP_RATE_LIMIT = 30  # Seconds between messages
WHATSAPP_MAX_RETRIES = 3  # Retry attempts for failed messages
```

### **Step 4: Template Configuration**

WhatsApp requires pre-approved message templates:

```python
# WhatsApp Template Configuration (Update with approved templates)
WHATSAPP_TEMPLATES = {
    'price_alert': {
        'name': 'express_deals_price_alert',  # Your approved template name
        'language': 'en',
        'category': 'MARKETING'
    },
    'deal_notification': {
        'name': 'express_deals_deal_notification',  # Your approved template name
        'language': 'en',
        'category': 'MARKETING'
    },
    'order_confirmation': {
        'name': 'express_deals_order_confirmation',  # Your approved template name
        'language': 'en', 
        'category': 'TRANSACTIONAL'
    }
}
```

---

## 🔧 **WEBHOOK SETUP**

### **Step 5: Configure Webhook URL**

1. **Set Webhook URL in Facebook Console**
   ```
   Webhook URL: https://yourdomain.com/alerts/whatsapp/webhook/
   Verify Token: express_deals_production_webhook
   ```

2. **Subscribe to Events**
   - messages
   - message_deliveries
   - message_reads
   - message_reactions

### **Step 6: Test Webhook**

```bash
# Test webhook verification
curl -X GET "https://yourdomain.com/alerts/whatsapp/webhook/?hub.mode=subscribe&hub.challenge=CHALLENGE_ACCEPTED&hub.verify_token=express_deals_production_webhook"

# Expected response: CHALLENGE_ACCEPTED
```

---

## 📋 **MESSAGE TEMPLATE CREATION**

### **Step 7: Create Message Templates**

**Price Alert Template:**
```
Template Name: express_deals_price_alert
Category: MARKETING
Language: English

Header: 🔥 Price Alert!
Body: Great news! {{1}} is now only ${{2}} (was ${{3}}). Get it now before the price goes back up!
Footer: Express Deals - Your Deal Discovery Platform
```

**Deal Notification Template:**
```
Template Name: express_deals_deal_notification
Category: MARKETING  
Language: English

Header: 🛍️ New Deals Available!
Body: We found {{1}} amazing deals for you! Check them out now and save big on your favorite products.
Footer: Express Deals - Never Miss a Deal
```

**Order Confirmation Template:**
```
Template Name: express_deals_order_confirmation
Category: TRANSACTIONAL
Language: English

Header: ✅ Order Confirmed
Body: Your order #{{1}} for ${{2}} has been confirmed! We'll send you updates as it ships. Thank you for shopping with Express Deals!
Footer: Express Deals - Fast & Reliable
```

### **Step 8: Submit Templates for Approval**

1. **Submit each template** in Facebook Business Manager
2. **Wait for approval** (usually 24-48 hours)
3. **Update template names** in settings.py once approved

---

## 🧪 **TESTING WHATSAPP FUNCTIONALITY**

### **Step 9: Test WhatsApp Integration**

```bash
# Activate virtual environment (.venv)
.\\.venv\\Scripts\\Activate.ps1

# Test WhatsApp functionality
python manage.py test_whatsapp +1234567890 --type text --message "Test message from Express Deals!"

# Test price alert
python manage.py test_whatsapp +1234567890 --type price_alert

# Test deal alert  
python manage.py test_whatsapp +1234567890 --type deal_alert
```

### **Step 10: User Profile Setup**

Add WhatsApp number to user profiles:

1. **Admin Panel**
   ```
   http://yourdomain.com/admin/accounts/userprofile/
   ```

2. **Add WhatsApp Number**
   - Edit user profile
   - Enter WhatsApp number: +1234567890
   - Enable WhatsApp notifications: ✓
   - Save changes

3. **Test User Notifications**
   - Create price alert for user
   - Trigger alert manually
   - Verify WhatsApp message delivery

---

## 🔒 **SECURITY AND COMPLIANCE**

### **Important Security Notes:**

1. **Access Token Security**
   - Never commit access tokens to version control
   - Rotate tokens regularly (every 90 days)
   - Use different tokens for development and production

2. **Rate Limiting**
   - WhatsApp enforces strict rate limits
   - Current settings: 30 seconds between messages
   - Respect user preferences and opt-outs

3. **GDPR Compliance**
   - Obtain explicit consent for WhatsApp notifications
   - Provide easy unsubscribe mechanism
   - Honor user data deletion requests

4. **Template Compliance**
   - Only use approved message templates
   - Don't modify template content dynamically
   - Follow WhatsApp's messaging policies

---

## 📊 **MONITORING AND ANALYTICS**

### **WhatsApp Message Monitoring:**

```python
# Check WhatsApp message logs
python manage.py shell

>>> from scraping.notifications import NotificationService
>>> service = NotificationService()
>>> service.whatsapp_enabled
True

# View recent WhatsApp activities in admin
Admin Panel → Scraping → WhatsApp Messages
```

### **Performance Metrics:**

- **Message delivery rates**
- **Template approval status**
- **User engagement rates**
- **Opt-out rates**
- **Error rates and causes**

---

## 🎯 **PRODUCTION DEPLOYMENT**

### **Final Production Checklist:**

- [ ] **Facebook Business Account verified**
- [ ] **WhatsApp Business API approved**
- [ ] **All message templates approved**
- [ ] **Access tokens configured in settings.py**
- [ ] **Webhook URL configured and tested**
- [ ] **WHATSAPP_ENABLED = True in settings**
- [ ] **SSL certificate installed on domain**
- [ ] **Rate limiting configured appropriately**
- [ ] **User consent mechanisms implemented**
- [ ] **Monitoring and logging active**

### **Production Settings Example:**

```python
# Production WhatsApp Configuration
WHATSAPP_ENABLED = True
WHATSAPP_ACCESS_TOKEN = 'EAAYourProductionTokenHere'
WHATSAPP_PHONE_NUMBER_ID = 'YourProductionPhoneNumberID'
WHATSAPP_VERIFY_TOKEN = 'your_secure_production_verify_token'

# Production Rate Limits (more conservative)
WHATSAPP_RATE_LIMIT = 60  # 1 minute between messages
WHATSAPP_MAX_RETRIES = 2  # Fewer retries in production
```

---

## ✅ **VERIFICATION CHECKLIST**

After setup, verify these work:

- [ ] **Send test WhatsApp message**
- [ ] **Receive WhatsApp price alert**
- [ ] **Receive order confirmation via WhatsApp**
- [ ] **Webhook receives and processes incoming messages**
- [ ] **User can unsubscribe via WhatsApp**
- [ ] **Admin can view WhatsApp activity logs**
- [ ] **Rate limiting prevents message spam**
- [ ] **Error handling works for failed messages**

**WhatsApp integration is now complete and ready for production use!** 🎉

---

*Configuration completed without any .env files - all settings are hardcoded in Django settings.py*
