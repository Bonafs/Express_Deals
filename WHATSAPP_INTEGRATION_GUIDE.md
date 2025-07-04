# EXPRESS DEALS - WHATSAPP INTEGRATION GUIDE

## 🚀 **WHATSAPP BUSINESS API INTEGRATION**

Express Deals now includes comprehensive WhatsApp integration using the Facebook WhatsApp Business API, enabling real-time notifications and interactive customer communication.

---

## 📋 **FEATURES ADDED**

### ✅ **WhatsApp Notifications**
- **Price Drop Alerts** - Instant notifications when prices fall below thresholds
- **Deal Notifications** - Weekly deal summaries and flash sale alerts  
- **Order Confirmations** - Automatic order status updates
- **Custom Messages** - Flexible text and media message support

### ✅ **Interactive WhatsApp Bot**
- **HELP Command** - Shows available commands and support information
- **DEALS Command** - Displays current top deals and offers
- **STOP Command** - Unsubscribe from WhatsApp notifications
- **Auto-responses** - Handles unknown messages with helpful guidance

### ✅ **Admin Management**
- **User Profile Management** - WhatsApp numbers and preferences
- **Bulk Operations** - Enable/disable notifications for multiple users
- **Template Management** - WhatsApp Business API message templates
- **Testing Tools** - Management command for testing functionality

---

## ⚙️ **SETUP CONFIGURATION**

### 1. **WhatsApp Business API Setup**

#### **Step 1: Create Facebook App**
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app and select "Business" type
3. Add "WhatsApp" product to your app
4. Note your App ID and App Secret

#### **Step 2: Get WhatsApp Business Account**
1. Verify your business with Facebook
2. Create or connect a WhatsApp Business Account
3. Add a phone number to your WhatsApp Business Account
4. Get your Phone Number ID and Business Account ID

#### **Step 3: Generate Access Token**
1. In your Facebook app, go to WhatsApp > Configuration
2. Generate a permanent access token
3. Save the access token securely

### 2. **Django Configuration**

#### **Update settings.py**
```python
# WhatsApp Configuration
WHATSAPP_API_URL = 'https://api.whatsapp.com/send'
WHATSAPP_BUSINESS_API_URL = 'https://graph.facebook.com/v17.0'
WHATSAPP_ACCESS_TOKEN = 'your_permanent_access_token_here'
WHATSAPP_PHONE_NUMBER_ID = 'your_phone_number_id_here'
WHATSAPP_VERIFY_TOKEN = 'express_deals_whatsapp_webhook'
```

#### **Environment Variables (Production)**
```env
WHATSAPP_ACCESS_TOKEN=your_permanent_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_custom_verify_token
```

### 3. **Webhook Configuration**

#### **Step 1: Configure Webhook URL**
1. In Facebook Developers, go to WhatsApp > Configuration
2. Set webhook URL: `https://yourdomain.com/alerts/whatsapp/webhook/`
3. Set verify token: `express_deals_whatsapp_webhook` (or your custom token)
4. Subscribe to these events:
   - `messages`
   - `message_deliveries`
   - `message_reads`

#### **Step 2: Test Webhook**
```bash
# Test webhook verification
curl -X GET "https://yourdomain.com/alerts/whatsapp/webhook/?hub.verify_token=express_deals_whatsapp_webhook&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe"
```

---

## 🔧 **USAGE INSTRUCTIONS**

### **For Administrators**

#### **1. User Profile Management**
1. Go to Admin → User Profiles
2. Add WhatsApp numbers for users
3. Enable WhatsApp notifications
4. Set user preferences

#### **2. Test WhatsApp Functionality**
```bash
# Test text message
python manage.py test_whatsapp "+1234567890" --message "Hello from Express Deals!"

# Test price alert
python manage.py test_whatsapp "+1234567890" --type price_alert

# Test deal alert
python manage.py test_whatsapp "+1234567890" --type deal_alert
```

#### **3. Bulk Operations**
1. Go to Admin → User Profiles
2. Select multiple users
3. Use bulk actions:
   - "Enable WhatsApp notifications"
   - "Disable WhatsApp notifications"

### **For Customers**

#### **1. Enable WhatsApp Notifications**
1. Log into your account
2. Go to Profile Settings
3. Add your WhatsApp number
4. Enable WhatsApp notifications
5. Save preferences

#### **2. WhatsApp Bot Commands**
- Send **HELP** - Get list of available commands
- Send **DEALS** - View current top deals
- Send **STOP** - Unsubscribe from notifications

#### **3. Automatic Notifications**
- **Price Alerts** - When watched products drop in price
- **Deal Alerts** - Weekly summary of best deals
- **Order Updates** - Confirmation and shipping notifications

---

## 📱 **MESSAGE TEMPLATES**

### **Price Alert Template**
```
🔥 Price Alert! [Product Name] is now only $[New Price] (was $[Old Price]). Get it now before the price goes back up! 🛍️

Express Deals - Your Deal Discovery Platform
```

### **Deal Notification Template**
```
🔥 New Deals Alert!

We found [Count] amazing deals for you! Check them out now and save big on your favorite products. 💰

Express Deals - Never Miss a Deal
```

### **Order Confirmation Template**
```
✅ Order Confirmed

Your order #[Order Number] for $[Total] has been confirmed! We'll send you updates as it ships. Thank you for shopping with Express Deals! 📦

Express Deals - Fast & Reliable
```

---

## 🛠️ **TROUBLESHOOTING**

### **Common Issues**

#### **Webhook Not Working**
1. Check webhook URL is publicly accessible
2. Verify SSL certificate is valid
3. Ensure verify token matches settings
4. Check Django logs for errors

#### **Messages Not Sending**
1. Verify access token is valid and not expired
2. Check phone number ID is correct
3. Ensure recipient number is properly formatted
4. Verify WhatsApp Business Account status

#### **Bot Commands Not Responding**
1. Check webhook is receiving messages
2. Verify message processing logic
3. Check for exceptions in Django logs
4. Test with simple text messages first

### **Testing Commands**

#### **Test Webhook Locally (ngrok)**
```bash
# Install ngrok
ngrok http 8000

# Use ngrok URL for webhook
https://abc123.ngrok.io/alerts/whatsapp/webhook/
```

#### **Test API Connection**
```bash
curl -X POST \
  https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "messaging_product": "whatsapp",
    "to": "RECIPIENT_PHONE_NUMBER",
    "type": "text",
    "text": {
      "body": "Test message from Express Deals!"
    }
  }'
```

---

## 📊 **ANALYTICS & MONITORING**

### **WhatsApp Metrics**
- Message delivery rates
- User engagement with bot commands
- Unsubscribe rates
- Most popular commands

### **Django Logging**
```python
# Add to settings.py LOGGING configuration
'whatsapp': {
    'handlers': ['file', 'console'],
    'level': 'INFO',
    'propagate': False,
},
```

### **Monitoring Dashboard**
- Track WhatsApp API usage
- Monitor webhook health
- User preference analytics
- Message template performance

---

## 🔐 **SECURITY CONSIDERATIONS**

### **API Security**
- Use permanent access tokens (not temporary)
- Rotate access tokens regularly
- Restrict webhook endpoints to Facebook IPs
- Validate webhook signatures

### **User Privacy**
- Store WhatsApp numbers securely
- Respect user unsubscribe requests
- Comply with WhatsApp Business Policy
- Implement data retention policies

### **Rate Limiting**
- WhatsApp API has message limits
- Implement exponential backoff
- Queue messages during high traffic
- Monitor API usage quotas

---

## 📞 **SUPPORT & RESOURCES**

### **Facebook Documentation**
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Message Templates](https://developers.facebook.com/docs/whatsapp/message-templates)
- [Webhooks](https://developers.facebook.com/docs/whatsapp/webhooks)

### **Express Deals Support**
- Check Django logs: `/logs/django.log`
- Test management commands: `python manage.py test_whatsapp`
- Admin interface: `/admin/accounts/userprofile/`

---

**WhatsApp integration is now fully functional and ready for production use!** 🚀
