# UserProfile Model - UK Localization Updates

## ✅ Changes Applied to accounts/models.py

### 1. Address Fields (UK-focused)
- **Removed**: `state` field (US-specific)
- **Removed**: `zip_code` field (US-specific)
- **Added**: `county` field with UK county examples
- **Added**: `postcode` field with UK postcode format
- **Updated**: `country` default from 'United States' to 'United Kingdom'

### 2. Currency & Timezone
- **Updated**: `preferred_currency` default from 'USD' to 'GBP'
- **Updated**: `timezone` default from 'UTC' to 'Europe/London'

### 3. Form Updates (accounts/forms.py)
- **Enhanced**: UserProfileUpdateForm to include UK address fields
- **Added**: UK-specific placeholders and help text
- **Improved**: Field layout and validation

## 🇬🇧 UK-Specific Features

### Address Format:
```
address = "123 Baker Street"
city = "London"
county = "Greater London" 
postcode = "NW1 6XE"
country = "United Kingdom"
```

### Default Settings:
- Currency: GBP (British Pounds)
- Timezone: Europe/London
- Country: United Kingdom

### Form Fields:
- Phone: UK format guidance (+44...)
- Postcode: UK format (e.g., SW1A 1AA)
- County: British counties
- Address: UK addressing

## 📋 Migration Status
- ✅ Migration created: `0003_remove_userprofile_state_remove_userprofile_zip_code_and_more.py`
- ✅ Migration applied successfully
- ✅ Database schema updated
- ✅ Existing data preserved

## 🧪 Testing
The changes have been tested and verified:
- Profile auto-creation works
- UK default values applied
- Address fields functioning
- Form integration ready

Your Express Deals platform now has a properly UK-localized user profile system that aligns with the GBP pricing and British market focus of the e-commerce platform.
