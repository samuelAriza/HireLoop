# HireLoop

> A comprehensive freelancing platform connecting clients with talented freelancers through projects, microservices, and mentorship sessions.

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project Overview

HireLoop is a modern freelancing platform built with Django that facilitates seamless connections between clients and freelancers. The platform supports multiple engagement models including fixed-price microservices, custom project collaborations, and one-on-one mentorship sessions.

### Key Features

- Multi-Profile System: Users can maintain both freelancer and client profiles  
- Microservices Marketplace: Browse and purchase fixed-price services with categorization  
- Project Management: Collaborative project system with applications, assignments, and status tracking  
- Mentorship Platform: Schedule and manage learning sessions between mentors and mentees  
- Smart Cart System: Unified shopping cart supporting multiple product types using Generic Foreign Keys  
- Analytics Dashboard: Real-time market insights with interactive Plotly Dash integration  
- Payment Processing: Secure payments through Stripe API integration  
- Portfolio Management: Comprehensive portfolio system for freelancers to showcase work  
- Advanced Search: Multi-field search and filtering across all content types  

## Tech Stack

### Backend
- Django 5.2.6
- Python 3.11+
- SQLite3 (development)
- django-taggit
- Stripe API

### Frontend
- Bootstrap 5
- Font Awesome 6
- JavaScript

### Analytics & Visualization
- Plotly Dash 2.18.2
- Pandas 2.3.2
- django-plotly-dash

### Development Tools
- Factory Boy 3.3.3
- Faker 37.8.0
- Black 25.9.0
- Flake8 6.1.0
- python-dotenv

### File Storage
- Local filesystem (configurable for cloud storage)
- Pillow

## Folder Structure
```
hireloop_project/
├── analytics/ # Analytics dashboard with Plotly Dash
│ ├── dash_apps/ # Dash application components
│ ├── repositories/ # Data access layer for analytics
│ └── services/ # Business logic for analytics
├── cart/ # Shopping cart and wishlist system
│ ├── factory_boy/ # Test data factories
│ ├── repositories/ # Cart data access
│ ├── services/ # Cart business logic
│ └── signals/ # Cart event handlers
├── core/ # User authentication and profiles
│ ├── factory_boy/
│ ├── forms/
│ ├── management/commands/
│ ├── mixins/
│ ├── repositories/
│ ├── services/
│ ├── templates/core/
│ └── views/
├── docs/ # Project documentation
├── mentorship_session/ # Mentorship booking system
├── microservices/ # Freelancer services marketplace
│ ├── factory_boy/
│ ├── repositories/
│ ├── services/
│ ├── templates/
│ └── views/
├── payments/ # Payment processing with Stripe
├── projects/ # Project management system
├── static/ # Static assets
├── staticfiles/ # Collected static files
├── templates/ # Global Django templates
├── media/ # User uploaded files
├── hireloop/ # Django project configuration
├── requirements.txt # Python dependencies
├── manage.py
├── .env # Environment variables
└── db.sqlite3 # SQLite database file
```

## Prerequisites

### Required
- Python 3.11+
- pip
- Git

### Recommended
- virtualenv or venv
- VS Code or PyCharm

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hireloop_project.git
cd hireloop_project
```
2. Create Virtual Environment
```bash
python -m venv venv
# Activate (Linux/Mac)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Environment Configuration
Create a .env file in the project root:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
# DATABASE_URL=postgresql://user:password@localhost:5432/hireloop

# Stripe
STRIPE_PUBLIC_KEY=pk_test_key
STRIPE_SECRET_KEY=sk_test_key

```

5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```
```bash
python manage.py runserver
```

Access at:

http://localhost:8000

http://localhost:8000/admin/

http://localhost:8000/analytics/

# Management Commands

```bash
# Database
python manage.py makemigrations
python manage.py migrate

# Users
python manage.py createsuperuser

# Static files
python manage.py collectstatic

# Custom commands
python manage.py populate_db --users 10 --freelancers 5 --clients 5 --microservices 20

```
# Testing

```bash
# Run all tests
python manage.py test

# Specific app
python manage.py test core
```

# Code quality
```bash
black .
flake8 .
isort .
```

# Contributing
1. Fork the repository

2. Create feature branch (git checkout -b feature/new-feature)

3. Commit changes (git commit -m "feat: add new feature")

4. Push to branch (git push origin feature/new-feature)

5. Open a Pull Request

# Branch conventions:

```bash
feature/* new features
bugfix/* bug fixes
docs/* documentation updates
```