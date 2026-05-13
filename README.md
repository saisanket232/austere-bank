# Austere Digital Banking System
**Advanced Django Full-Stack Banking Application**

Austere is a premium digital banking management system designed for seamless financial operations. It features a robust role-based access control system for Admins, Employees, and Customers, ensuring secure and efficient banking processes.

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Navigate to project directory
cd digital_bank

# Install dependencies (ensure you have mysqlclient installed)
pip install django mysqlclient
```

### 2. Database & Server
```bash
# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

**Visit:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Demo Credentials

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Full system control |
| **Employee** | `employee1` | `pass123` | Operational tasks (Deposit, Withdraw, Freeze) |
| **Customer** | `sai@13` | *(Register to create)* | Personal banking (Transfer, Loans, History) |

---

## 🏗️ Project Structure
```
digital_bank/
├── accounts/       # User Auth, Profiles, Role Management, OTP Simulation
├── banking/        # Core Banking: Accounts, Transfers, Deposits, Withdrawals
├── loans/          # Credit Services: Applications, EMI Calc, Disbursements
├── static/         # Custom CSS (Glassmorphism design) & Assets
└── templates/      # Responsive Django Templates (Bootstrap 5)
```

---

## ✨ Features Implemented

### 🏦 Banking Operations
- **Real-time Account Creation**: Savings accounts are automatically generated upon registration.
- **Deposit & Withdraw Cash**: Bank Employees can perform manual cash operations for customers.
- **Fund Transfers**: Secure customer-to-customer transfers with **OTP Verification** (Demo OTP: `123456`).
- **Account Freeze**: Employees/Admins can freeze accounts to block all transactions instantly.
- **Transaction History**: Comprehensive ledger with status-based filtering and mini-statements.

### 💰 Loan Management
- **Smart Loan Applications**: 5 distinct loan types (Personal, Home, Car, Education, Business).
- **Automated Disbursement**: Approved loans are credited to the customer's balance immediately.
- **EMI Calculator**: Advanced financial tool with total payable and interest breakdown.

### 🛡️ Security & UX
- **Role-Based Access Control (RBAC)**: Distinct dashboards tailored to User, Employee, and Admin.
- **Transaction Security**: Strict status checks (Active/Frozen) enforced across all fund movements.
- **Premium Aesthetics**: Dark-themed "Austere" UI featuring glassmorphism and modern typography.
- **UUID Security**: Uses UUIDs for account and transaction identification.

---

## 🛠️ Technology Stack
- **Backend**: Django (Python)
- **Database**: MySQL (supports SQLite for local dev)
- **Frontend**: Bootstrap 5, FontAwesome 6, Custom CSS3
- **Authentication**: Django Auth System + Custom UserProfile
