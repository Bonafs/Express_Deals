# 🔐 Express Deals - Security & Credentials Guide

## ⚠️ SECURITY CRITICAL

This guide explains how to manage sensitive credentials securely for the Express Deals application.

## 🚨 NEVER COMMIT THESE FILES TO VERSION CONTROL:

- `credentials.py` - Contains all sensitive credentials
- `local_settings.py` - Local development settings with secrets
- `.env.local` - Environment variables for local development
- Any file ending with `_credentials.py` or `_secrets.py`

## 📁 Setup Instructions

### 1. Copy the Template File

```bash
cp credentials.template.py credentials.py
```

### 2. Edit Your Credentials

Open `credentials.py` and replace all placeholder values with your actual credentials:

```python
# Example:
SUPERUSER_USERNAME = 'your_admin_username'
SUPERUSER_EMAIL = 'your_admin@yoursite.com'
SUPERUSER_PASSWORD = 'your_very_secure_password'
```

### 3. Secure Your File

**Important:** The `credentials.py` file is automatically ignored by Git (see `.gitignore`).

## 🔑 Environment Variables (Production)

For production deployment, set these environment variables in your hosting platform:

### Heroku Example:
```bash
heroku config:set SUPERUSER_USERNAME=your_admin_username --app your-app
heroku config:set SUPERUSER_EMAIL=your_admin@yoursite.com --app your-app
heroku config:set SUPERUSER_PASSWORD=your_secure_password --app your-app
```

## 🛠️ Using Secure Scripts

### Create Superuser Securely:
```bash
python create_secure_superuser.py
```

### Create Sample Users Securely:
```bash
python create_secure_sample_users.py
```

These scripts will:
1. Try environment variables first (production)
2. Fall back to `credentials.py` file (development)
3. Prompt for input if neither is available

## 🔒 Security Best Practices

### For Development:
- Use `credentials.py` file
- Never commit it to version control
- Use different passwords than production

### For Production:
- Use environment variables
- Use strong, unique passwords
- Enable 2FA where possible
- Regularly rotate credentials

### For Team Development:
- Each developer has their own `credentials.py`
- Share the template file only
- Document required environment variables

## 📝 Credential Checklist

- [ ] Copied `credentials.template.py` to `credentials.py`
- [ ] Updated all placeholder values
- [ ] Verified `credentials.py` is in `.gitignore`
- [ ] Tested secure scripts work
- [ ] Set up production environment variables
- [ ] Documented team setup process

## 🚫 What NOT to Do

- ❌ Don't commit `credentials.py` to Git
- ❌ Don't share credentials in chat/email
- ❌ Don't use the same passwords for dev/prod
- ❌ Don't hardcode credentials in scripts
- ❌ Don't store credentials in public notes

## 🆘 If Credentials Are Compromised

1. **Immediately** change all affected passwords
2. Rotate API keys and tokens
3. Check access logs for unauthorized activity
4. Update environment variables in production
5. Inform team members if needed

## 📞 Support

If you need help with credential setup, contact the development team through secure channels only.

---

**Remember:** Security is everyone's responsibility! 🛡️
