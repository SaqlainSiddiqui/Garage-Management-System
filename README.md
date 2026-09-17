# Garage Management System

A desktop-based Garage / Vehicle Service Management System built with **Python, CustomTkinter, and MongoDB**.

The application helps manage customers, vehicles, services, spare-parts inventory, invoices, service history, reports, and user settings through a desktop GUI.

## Features

- User login and authentication
- Customer management
- Vehicle management
- Customer → Vehicle → Service History navigation
- Vehicle service management
- Service status tracking
- Spare-parts inventory management
- Automatic stock deduction when parts are used in a service
- Inventory transaction history
- Billing and invoice generation
- Automatic invoice item generation from service labour and spare parts
- Tax calculation
- PDF reports/invoices
- Reports and analytics
- Dashboard statistics
- Charts and visual analytics
- Service search and filtering
- Low-stock reporting
- Dark / Light / System theme
- User profile management
- Password change
- MongoDB connection test
- MongoDB indexes for commonly searched fields

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.13+ |
| GUI | CustomTkinter |
| Database | MongoDB |
| Database Driver | PyMongo |
| Charts | Matplotlib |
| PDF Generation | ReportLab |
| Calendar Widget | tkcalendar |
| Password Hashing | bcrypt |
| Configuration | python-dotenv |

## Project Structure

```text
Garage Management System/
│
├── config/
│   ├── database.py
│   ├── indexes.py
│   └── theme.py
│
├── models/
│   ├── customer.py
│   ├── inventory_transaction.py
│   ├── invoice.py
│   ├── reports.py
│   ├── service.py
│   ├── spare_part.py
│   ├── user.py
│   └── vehicle.py
│
├── views/
│   ├── billing.py
│   ├── customer.py
│   ├── dashboard.py
│   ├── login.py
│   ├── reports.py
│   ├── service.py
│   ├── settings.py
│   ├── spare_parts.py
│   └── vehicle.py
│
├── reports/
│   └── PDF/report-generation files
│
├── .env
├── create_test_user.py
├── diagnose_project.py
├── requirements.txt
└── app.py
```

## Requirements

- Windows 10/11
- Python 3.13 or compatible Python version
- MongoDB server or MongoDB Atlas
- Git
- Internet connection for installing Python packages

> MongoDB Compass is optional. It is useful for viewing and managing the database, but the application connects directly to MongoDB.

## 1. Clone the Repository

After the project has been uploaded to GitHub:

```bash
git clone https://github.com/YOUR-USERNAME/garage-management-system.git
cd garage-management-system
```

Replace `YOUR-USERNAME` with your GitHub username.

## 2. Create a Virtual Environment

### Git Bash

```bash
python -m venv venv
source venv/Scripts/activate
```

You should see:

```text
(venv)
```

at the beginning of your terminal prompt.

### PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If `requirements.txt` is not present yet, install the packages manually:

```bash
python -m pip install pymongo customtkinter python-dotenv pillow matplotlib reportlab tkcalendar bcrypt
```

## 4. Configure MongoDB

Create a `.env` file in the project root.

Example:

```env
MONGODB_URI=mongodb://localhost:27017/
```

For MongoDB Atlas, use your Atlas connection string:

```env
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/
```

Do **not** commit your real `.env` file to GitHub if it contains credentials.

Add `.env` to `.gitignore`.

## 5. Create the Database Indexes

With the virtual environment activated:

```bash
python -m config.indexes
```

The application uses the `garage_management` database.

## 6. Create a Test/Admin User

If the project includes the test-user script:

```bash
python create_test_user.py
```

The development test account is:

```text
Email: admin@garage.com
Password: Admin@123
```

For production use, create a new secure password instead of using the development credentials.

## 7. Run Diagnostics

Before starting the application:

```bash
python diagnose_project.py
```

A successful result should look like:

```text
PROJECT DIAGNOSTICS: PASSED
All project Python files passed syntax parsing and integration checks.
```

## 8. Run the Application

Use:

```bash
python -m views.login
```

This is the main entry point for the desktop application.

Do **not** use:

```bash
python app.py
```

unless the project is specifically changed to use `app.py` as its entry point.

## 9. Typical Development Workflow

Every time you open a new terminal:

```bash
cd "/c/Users/YOUR-USERNAME/path/to/Garage Management System"
source venv/Scripts/activate
python -m views.login
```

To install a new package:

```bash
python -m pip install PACKAGE_NAME
```

Then update the dependency list:

```bash
python -m pip freeze > requirements.txt
```

## MongoDB Database

Database:

```text
garage_management
```

Main collections:

```text
users
customers
vehicles
services
spare_parts
invoices
inventory_transactions
```

## Security Notes

- Passwords are hashed using bcrypt.
- Keep MongoDB credentials outside the source code.
- Do not upload `.env` to a public GitHub repository.
- Do not upload the `venv/` directory.
- Do not upload Python cache files such as `__pycache__/`.
- Change development/test credentials before real-world use.

## GitHub Setup

Initialize Git in the project directory:

```bash
git init
```

Add the GitHub repository as the remote:

```bash
git remote add origin https://github.com/YOUR-USERNAME/garage-management-system.git
```

Check the remote:

```bash
git remote -v
```

Create a `.gitignore` file before adding files.

Recommended `.gitignore`:

```gitignore
# Virtual environment
venv/
.venv/

# Environment variables / secrets
.env
.env.*

# Python cache
__pycache__/
*.py[cod]
*$py.class

# IDE
.vscode/
.idea/

# Build files
build/
dist/
*.spec

# Generated files
*.log

# OS files
.DS_Store
Thumbs.db
```

Then check what Git will include:

```bash
git status
```

Add the project:

```bash
git add .
```

Create the first commit:

```bash
git commit -m "Initial commit - Garage Management System"
```

Set the main branch:

```bash
git branch -M main
```

Push to GitHub:

```bash
git push -u origin main
```

## Updating the GitHub Repository

After making changes:

```bash
git status
git add .
git commit -m "Describe your changes"
git push
```

## Important

Never commit:

```text
.env
venv/
__pycache__/
```

Especially do not commit a MongoDB connection string containing a username and password.

## License

This project is intended for academic and educational use.
