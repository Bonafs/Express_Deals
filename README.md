# Express Deals

Express Deals is a Django-based web application for managing products, orders, payments, and scraping deals from various sources. It is designed for fast deployment and easy management of e-commerce operations.

## Features
- User authentication and profile management
- Product catalog with categories and images
- Order management and payment processing
- Real-time updates and notifications
- Scraping tools for collecting deals
- Admin dashboard for managing users, products, and orders

## Project Structure
- `accounts/` - User authentication, registration, and profile management
- `products/` - Product models, views, and admin
- `orders/` - Order processing and management
- `payments/` - Payment integration and management
- `scraping/` - Scraping utilities and deal collection
- `realtime/` - Real-time features (e.g., notifications)
- `express_deals/` - Project settings and configuration

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd Express_Deals
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `credentials.template.py` to `credentials.py` and update with your credentials.
5. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
6. **Create a superuser:**
   ```sh
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## Deployment
- The project includes a `Procfile` for deployment on Heroku.
- Update `production_settings.py` and `heroku_settings.py` as needed for your environment.

## License
This project is licensed under the MIT License.
