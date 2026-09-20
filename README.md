# DigiLala 🛒

### E-commerce Web Application

A practical e-commerce web application built with **Django** and **PostgreSQL**, developed as a backend-focused portfolio project.

**Django** • **PostgreSQL** • **Authentication** • **Shopping Cart** • **Checkout** • **Order Management**

**Project Status:** 🚧 In Active Development

**Repository:** https://github.com/AmirPR0/django-ecommerce

---

## 📖 About the Project

DigiLala is an e-commerce web application built with Django and PostgreSQL.

The project is being developed as a practical portfolio project with a focus on backend development, database-driven product management, authentication, shopping cart functionality, checkout, and order management.

The main purpose of the project is to demonstrate practical backend development concepts through a real-world application rather than a simple tutorial-based project.

---

## 🚀 Features

### Product & Category Management

* Manage products and categories through the database
* Upload product images
* Add full and short product descriptions
* Manage product prices and stock
* Manage product availability
* Browse products by category

### 🛒 Shopping Cart

* Session-based shopping cart
* Add products to the cart
* Increase and decrease product quantities
* Remove products from the cart
* Calculate cart quantity and total price
* Validate stock before adding products
* Validate stock during checkout

### 📦 Checkout & Orders

* Checkout process
* Create orders
* Store order items
* Calculate order totals
* Automatically decrease product stock after a successful checkout
* View order history
* View order details

### 🔎 Search & UI

* Product search
* Bootstrap-based user interface
* Navigation for products and categories
* Responsive navigation bar
* Empty cart state
* Toast feedback messages for success and error states
* Custom CSS styling
* Bootstrap Icons
* Vazir font for the Persian user interface

### 🔐 Authentication

The authentication system is implemented using `django-allauth`.

Current authentication features include:

* Email signup
* Email login
* Logout
* Email verification
* Password reset
* Password change
* User management through Django Admin
* Authentication redirects

During development, emails are displayed directly in the terminal using Django's console email backend.

---

## 🛠️ Tech Stack

| Technology      | Purpose                            |
| --------------- | ---------------------------------- |
| Python          | Backend programming                |
| Django          | Main web framework                 |
| PostgreSQL      | Database                           |
| Django ORM      | Database interaction               |
| django-allauth  | Authentication system              |
| django-environ  | Environment variable management    |
| Bootstrap       | Frontend framework                 |
| HTML5           | Page structure                     |
| CSS3            | Styling                            |
| JavaScript      | Client-side interactions           |
| Bootstrap Icons | UI icons                           |
| Vazir           | Persian font                       |
| Git             | Version control                    |
| GitHub          | Code hosting and remote repository |

---

## 📁 Project Structure

DigiLala/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
│   ├── categories/
│   └── products/
│
├── shop/
│   ├── migrations/
│   ├── static/
│   │   └── shop/
│   │       ├── css/
│   │       └── images/
│   ├── templates/
│   │   └── shop/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/
│   ├── bootstrap/
│   ├── css/
│   │   └── fonts/
│   └── icons/
│
├── templates/
│   ├── base.html
│   └── include/
│       ├── header.html
│       └── footer.html
│
├── .env
├── .gitignore
├── manage.py
└── requirements.txt

---

## 🔐 Authentication

DigiLala uses `django-allauth` for its authentication system.

The current configuration uses email-based authentication instead of username-based authentication.

Current features include:

* Signup
* Login
* Logout
* Email verification
* Password reset
* Password change

Authentication routes are available under the `/accounts/` URL.

For example:

/accounts/login/
/accounts/signup/
/accounts/logout/
/accounts/password/reset/

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```cmd
git clone https://github.com/AmirPR0/django-ecommerce.git
cd django-ecommerce

### 2. Create a Virtual Environment

python -m venv venv

### 3. Activate the Virtual Environment

On Windows:

venv\Scripts\activate

### 4. Install Dependencies

pip install -r requirements.txt

---

## 🔑 Environment Variables

Sensitive project configuration is managed through environment variables instead of being stored directly in the source code.

Create a `.env` file in the project root:

SECRET_KEY=your-secret-key

DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

---

## 🗄️ Database Setup

The project uses PostgreSQL as its database.

After configuring PostgreSQL and the required environment variables, run the migrations:

python manage.py migrate

Create a Django superuser:

python manage.py createsuperuser

---

## ▶️ Running the Project

Start the Django development server:

python manage.py runserver

The application will be available at:

http://127.0.0.1:8000/

Django Admin:

http://127.0.0.1:8000/admin/

---

## 📧 Development Email

During development, the project uses Django's console email backend.

This means emails related to account verification and password recovery are displayed directly in the terminal instead of being sent through a real SMTP service.

This approach makes it possible to test the authentication system without configuring an external email service during development.

---

## 🔄 Git Workflow

The project is developed incrementally using Git.

Features are organized into separate commits to keep the development history clear and traceable.

Examples of project commits:

feat: add email authentication with allauth
feat: add toast feedback messages
feat: complete navbar and add product search
feat: improve home page and footer UI

The `main` branch contains the latest stable version of the project.

---

## 🧪 Development Status

### Completed

* [x] PostgreSQL integration
* [x] Product management
* [x] Category management
* [x] Product image uploads
* [x] Stock management
* [x] Shopping cart
* [x] Checkout process
* [x] Order management
* [x] Order history
* [x] Order details
* [x] Product search
* [x] Responsive navigation bar
* [x] Home page
* [x] Footer
* [x] Empty cart state
* [x] Toast feedback messages
* [x] Email-based authentication
* [x] Email verification
* [x] Password reset
* [x] Password change
* [x] Django Admin integration
* [x] Environment variable management

### Planned

* [ ] Google reCAPTCHA
* [ ] Custom user and signup fields
* [ ] Order ownership and user-specific order access
* [ ] Custom authentication templates
* [ ] Authentication and application tests
* [ ] Final responsive UI improvements
* [ ] Django REST Framework API
* [ ] Docker and Docker Compose
* [ ] CI/CD
* [ ] Production deployment

---

## 🎯 Project Goals

The main goal of DigiLala is to build a practical Django project that demonstrates important backend development concepts through a real-world application.

Key concepts demonstrated in the project include:

* Database design
* Django models and relationships
* Django ORM
* Authentication and authorization
* Session management
* Form handling
* Business logic
* Transaction handling
* Stock validation
* Order processing
* Environment configuration
* Version control with Git

The project is continuously being improved as part of the developer's backend learning and development journey.

---

## 📌 Current Version

The `main` branch contains the latest implemented version of the project, including email-based authentication with `django-allauth`.

---

## 👤 Author

**Amirhossein Rahimi Moghaddam**

Currently developing skills in:

* **Python**
* **Django**
* **PostgreSQL**
* **Networking**
* **HTML5**
* **CSS3**
* **Bootstrap**
* **JavaScript (Beginner)**

---

## 📄 License

This project is currently developed as a personal educational portfolio project.
