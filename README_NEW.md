# Express Deals - E-commerce Platform

![Express Deals Logo](https://img.shields.io/badge/Express-Deals-blue?style=for-the-badge&logo=shopping-cart)

A modern, full-featured e-commerce platform built with Django, featuring a complete shopping experience with cart management, secure payments, and responsive design.

## 🌟 Features

### 🛍️ Core E-commerce Features
- **Product Catalog**: Comprehensive product listings with categories, images, and detailed descriptions
- **Advanced Search & Filtering**: Search by name, filter by category, price range, and sorting options
- **Shopping Cart**: Full cart management with add/remove items, quantity updates, and real-time totals
- **User Authentication**: Complete user registration, login, and profile management
- **Checkout Process**: Streamlined checkout with shipping information collection
- **Order Management**: Order history, detailed order views, and order tracking

### 💳 Payment Integration
- **Stripe Integration**: Secure payment processing with Stripe
- **Multiple Payment Methods**: Credit cards, debit cards
- **Payment Security**: PCI-compliant payment handling
- **Order Confirmation**: Automated order confirmation and email notifications

### 🎨 User Experience
- **Responsive Design**: Mobile-first design that works on all devices
- **Modern UI**: Clean, intuitive interface with Bootstrap 5
- **AJAX Functionality**: Smooth user interactions without page reloads
- **Real-time Updates**: Live cart updates and instant feedback

### 🔒 Security & Performance
- **Security Headers**: Comprehensive security headers for production
- **CSRF Protection**: Cross-Site Request Forgery protection
- **Input Validation**: Robust form validation and sanitization
- **Database Security**: Parameterized queries and ORM security
- **Static Files Optimization**: WhiteNoise for efficient static file serving

### 🛠️ Admin & Management
- **Django Admin**: Full admin interface for content management
- **Product Management**: Add, edit, and manage products and categories
- **Order Management**: View and manage customer orders
- **User Management**: Manage customer accounts and permissions

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- Stripe account (for payments)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/express-deals.git
   cd express-deals
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run setup script**
   ```bash
   python setup_django.py
   ```

6. **Start the development server**
   ```bash
   python start_server.py
   ```

Visit `http://localhost:8000` to see your Express Deals store!

## 📋 Project Structure

```
express_deals/
├── express_deals/          # Main Django project
│   ├── settings.py         # Django settings
│   ├── production_settings.py  # Production configuration
│   ├── urls.py            # URL routing
│   └── context_processors.py   # Template context processors
├── products/              # Product management app
│   ├── models.py          # Product, Category models
│   ├── views.py           # Product views
│   ├── forms.py           # Search and filter forms
│   └── urls.py            # Product URLs
├── orders/                # Order and cart management
│   ├── models.py          # Cart, Order models
│   ├── views.py           # Cart and checkout views
│   └── urls.py            # Order URLs
├── payments/              # Payment processing
│   ├── models.py          # Payment models
│   ├── views.py           # Payment views
│   └── urls.py            # Payment URLs
├── accounts/              # User management
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── products/          # Product templates
│   ├── orders/            # Cart and checkout templates
│   └── payments/          # Payment templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── logs/                  # Application logs
├── scripts/               # Utility scripts
│   ├── setup_django.py    # Initial setup
│   ├── populate_data.py   # Sample data
│   ├── deploy_production.py  # Deployment script
│   └── final_project_report.py  # Project evaluation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
└── DEPLOYMENT.md         # Deployment guide
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_comprehensive.py
```

Run specific functionality tests:
```bash
python test_cart_functionality.py
```

Check project status:
```bash
python check_project_status.py
```

## 🚀 Deployment

### Quick Deployment
1. **Prepare for deployment**
   ```bash
   python deploy_production.py
   ```

2. **Set up production environment variables**
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=your-production-database-url
   STRIPE_PUBLISHABLE_KEY=pk_live_your_key
   STRIPE_SECRET_KEY=sk_live_your_key
   ```

3. **Deploy to your preferred platform**
   - Heroku
   - Railway
   - DigitalOcean
   - AWS
   - Google Cloud Platform

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Project Status

Generate a comprehensive project report:
```bash
python final_project_report.py
```

## 🛡️ Security

Express Deals implements comprehensive security measures:

- **HTTPS Enforcement**: All traffic redirected to HTTPS in production
- **Security Headers**: HSTS, CSP, X-Frame-Options, etc.
- **Input Validation**: All user inputs validated and sanitized
- **CSRF Protection**: Cross-site request forgery protection
- **XSS Protection**: Cross-site scripting prevention
- **SQL Injection Prevention**: ORM-based queries with parameterization

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (False in production) | Yes |
| `ALLOWED_HOSTS` | Allowed host domains | Yes |
| `DATABASE_URL` | Database connection string | Production |
| `STRIPE_PUBLISHABLE_KEY` | Stripe public key | Yes |
| `STRIPE_SECRET_KEY` | Stripe secret key | Yes |
| `EMAIL_HOST` | SMTP host for emails | Optional |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 | Optional |

### Database Configuration

**Development**: SQLite (default)
**Production**: PostgreSQL (recommended)

### Payment Configuration

1. Create a Stripe account
2. Get your API keys from the Stripe dashboard
3. Set up webhooks for order confirmations
4. Configure payment methods and currencies

## 📱 Responsive Design

Express Deals is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile phones
- All screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
- Review the comprehensive test results
- Check the logs/ directory for error messages
- Ensure all environment variables are configured

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- Django framework for the robust backend
- Bootstrap for the responsive frontend
- Stripe for secure payment processing
- All the open-source libraries that made this project possible

---

**Express Deals** - *Your one-stop e-commerce solution*

Built with ❤️ using Django and modern web technologies.
