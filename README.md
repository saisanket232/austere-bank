# 🏦 Austere Digital Banking System

A comprehensive Django-based digital banking platform that simulates real-world banking operations with role-based access control, secure transactions, and loan management capabilities.

---

## Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Modules Overview](#-modules-overview)
- [Usage Guide](#-usage-guide)
- [Technical Stack](#-technical-stack)
- [Database Schema](#-database-schema)
- [Security Features](#-security-features)
- [Demo Credentials](#-demo-credentials)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## Features

### Core Banking
- **Account Management**: Create, view, and manage customer bank accounts
- **Deposits & Withdrawals**: Process cash deposits and withdrawals with transaction history
- **Fund Transfers**: Secure peer-to-peer transfers with OTP verification
- **Mini Statements**: View transaction history with date and type filtering
- **Account Freeze/Unfreeze**: Freeze suspicious accounts to prevent unauthorized transactions

### Loan Management
- **Loan Application**: Submit loan applications with flexible loan types
- **EMI Calculator**: Calculate monthly EMI, total interest, and repayment tenure
- **Loan Review**: Employees and Admins review and approve/reject applications
- **Auto Disbursement**: Approved loans automatically credited to customer accounts
- **Loan Tracking**: View loan status, details, and payment information

### Security & Access Control
- **Role-Based Access Control (RBAC)**: Customer, Employee, and Admin roles
- **OTP Verification**: Two-factor authentication for sensitive transactions (Demo OTP: `123456`)
- **Session Management**: Secure login/logout with session timeout
- **Account Status Validation**: Prevents frozen accounts from participating in transactions
- **Transaction Audit Trail**: Complete history of all banking operations

---

## Prerequisites

- **Python** 3.8 or higher
- **Django** 3.2+
- **pip** (Python package manager)
- **SQLite3** (included with Python) or **MySQL** (optional)
- **Git** (for version control)

---

## Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd digital_bank
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Application
```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000`

---

## Project Structure

```
digital_bank/
│
├── accounts/                 # User authentication and profiles
│   ├── migrations/
│   ├── models.py            # User, Customer, OTP models
│   ├── views.py             # Registration, login, profile views
│   ├── forms.py             # User and registration forms
│   ├── urls.py              # Account routes
│   └── admin.py             # Admin panel configuration
│
├── banking/                 # Core banking operations
│   ├── migrations/
│   ├── models.py            # BankAccount, Transaction models
│   ├── views.py             # Transfer, deposit, withdrawal views
│   ├── forms.py             # Banking transaction forms
│   ├── urls.py              # Banking routes
│   └── admin.py             # Admin panel configuration
│
├── loans/                   # Loan management system
│   ├── migrations/
│   ├── models.py            # Loan, LoanApplication models
│   ├── views.py             # Loan application and review views
│   ├── forms.py             # Loan application forms
│   ├── urls.py              # Loan routes
│   └── admin.py             # Admin panel configuration
│
├── digital_bank/            # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL router
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Authentication templates
│   ├── banking/             # Banking templates
│   └── loans/               # Loan templates
│
├── static/                  # Static assets
│   ├── css/                 # Stylesheets (Bootstrap + custom)
│   ├── js/                  # JavaScript files
│   └── images/              # Images and icons
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── db.sqlite3              # SQLite database (development)
└── README.md               # This file
```

---

## Modules Overview

### 1. Accounts Module (Authentication)
**Purpose**: Manage user registration, authentication, and profile management.

**Key Features**:
- User registration with email verification
- Secure login with Django authentication
- OTP generation and validation for sensitive operations
- User profile management (customer details, contact info)
- Role assignment (Customer, Employee, Admin)

**Main Views**:
- `/accounts/register/` - User registration page
- `/accounts/login/` - User login page
- `/accounts/profile/` - View and edit user profile
- `/accounts/logout/` - User logout

---

### 2. Banking Module (Transaction Processing)
**Purpose**: Handle all core banking operations and transaction management.

**Key Features**:
- Account dashboard with balance overview
- Deposit processing (Employee only)
- Withdrawal processing (Employee only)
- Fund transfers with OTP verification (Customer)
- Account freeze/unfreeze functionality (Admin/Employee)
- Transaction history and mini-statements

**Main Views**:
- `/banking/dashboard/` - Account overview
- `/banking/transfer/` - Transfer funds
- `/banking/deposit/` - Process deposit
- `/banking/withdraw/` - Process withdrawal
- `/banking/mini-statement/` - View transaction history
- `/banking/freeze/` - Freeze account (Admin/Employee)

---

### 3. Loans Module (Loan Management)
**Purpose**: Manage the complete loan lifecycle from application to disbursement.

**Key Features**:
- Loan application submission
- EMI calculator for loan planning
- Loan application review dashboard (Employee/Admin)
- Approve or reject loan applications
- Auto-disbursement to customer accounts
- Loan status tracking and details

**Main Views**:
- `/loans/apply/` - Apply for new loan
- `/loans/emi-calculator/` - Calculate EMI
- `/loans/my-loans/` - View customer's loans
- `/loans/review/` - Review pending applications (Employee/Admin)
- `/loans/loan-detail/<id>/` - View loan details

---

## Usage Guide

### For Customers
1. **Register**: Create a new account at `/accounts/register/`
2. **Login**: Log in with credentials at `/accounts/login/`
3. **View Dashboard**: Access personal banking dashboard
4. **Manage Transfers**: Transfer funds to other accounts (requires OTP: `123456`)
5. **Apply for Loans**: Submit loan applications and track status
6. **View Statements**: Check transaction history

### For Employees
1. **Login**: Log in with employee credentials
2. **Customer Management**: Access all registered customers
3. **Process Deposits**: Credit funds to customer accounts
4. **Process Withdrawals**: Debit funds from customer accounts
5. **Freeze Accounts**: Freeze suspicious accounts
6. **Review Loans**: Approve or reject loan applications

### For Admins
1. **Login**: Log in with admin credentials
2. **System Overview**: View all users, accounts, and transactions
3. **Manage Users**: Create, edit, or delete user accounts
4. **Transaction Audit**: Review all system transactions
5. **Loan Management**: Approve/reject loans
6. **System Configuration**: Access Django admin panel

---

## Technical Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 3.2+ |
| **Python Version** | 3.8+ |
| **Database** | SQLite (Development) / MySQL (Production) |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Styling** | Bootstrap 5 + Custom CSS |
| **Authentication** | Django Auth + Custom OTP System |
| **ORM** | Django ORM |

---

## Database Schema

### Key Models

**User & Authentication**
- `User` - Django built-in user model
- `Customer` - Customer profile (extends User)
- `OTP` - One-time passwords for verification

**Banking**
- `BankAccount` - Customer bank accounts with balance tracking
- `Transaction` - Transaction records (deposits, withdrawals, transfers)

**Loans**
- `Loan` - Loan products (types and terms)
- `LoanApplication` - Customer loan applications and status
- `EMI` - EMI calculation and payment tracking

---

## Security Features

1. **Role-Based Access Control**
   - Customers can only access their own data
   - Employees have limited administrative access
   - Admins have full system access

2. **OTP Verification**
   - Two-factor authentication for transfers
   - Demo OTP: `123456`
   - Prevents unauthorized transactions

3. **Account Status Checks**
   - Frozen accounts blocked from transactions
   - Account validation before each operation
   - Transaction authorization verification

4. **Session Management**
   - Django session framework for secure sessions
   - Automatic session timeout
   - Secure logout mechanism

5. **Data Validation**
   - Input validation on all forms
   - SQL injection prevention via Django ORM
   - CSRF protection on all POST requests

---

## Demo Credentials

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| **Admin** | admin | (set during setup) | System administration |
| **Employee** | employee1 | (set during setup) | Customer service |
| **Customer** | customer1 | (register new) | Banking operations |

**Demo OTP**: `123456` (for all transfer operations)

---

## Troubleshooting

### Issue: Database migration error
```bash
# Solution: Reset migrations and start fresh
python manage.py migrate accounts zero
python manage.py migrate banking zero
python manage.py migrate loans zero
python manage.py migrate
```

### Issue: Static files not loading
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

### Issue: Port 8000 already in use
```bash
# Solution: Run on different port
python manage.py runserver 8001
```

### Issue: Module not found errors
```bash
# Solution: Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Python Official Documentation](https://docs.python.org/)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author & Support

For questions or support, please open an issue in the repository or contact the development team.

---

**Last Updated**: June 2026  
**Version**: 1.0.0
