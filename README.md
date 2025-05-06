# Grocery Store Website 🛒

A full-featured grocery store web application built using HTML, CSS, JavaScript, Bootstrap (frontend), and Django (backend), including secure payment integration.

## 🔧 Tech Stack

### Frontend:
- HTML5
- CSS3
- JavaScript (Vanilla)
- Bootstrap 5

### Backend:
- Python 3.x
- Django Framework
- SQLite / PostgreSQL (configurable)

### Features:
- 🛍️ User-friendly UI for browsing grocery items
- 🔍 Product search and filtering
- 🛒 Add to cart and checkout functionality
- 🔐 User authentication (Sign up / Login / Logout)
- 🧾 Order history and invoice generation
- 💳 Payment gateway integration (Paytm/Stripe/etc.)
- 🧑‍💼 Admin panel for product & order management

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gaurav4045/websiteproject.git
   cd websiteproject
2.Create a virtual environment
python -m venv env
3.Activate the virtual environment

On Windows:
env\Scripts\activate

On MacOS/Linux:
source env/bin/activate

4.Install required dependencies
pip install -r requirements.txt

5.Run migrations
python manage.py makemigrations && python manage.py migrate

6.Start the development server
