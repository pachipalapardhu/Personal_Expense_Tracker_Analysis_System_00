# Personal Expense Tracking and Analysis System

An academic, beginner-friendly web application designed to help individuals record personal expenses and gain clear, data-driven insights into their monthly spending patterns and category-wise expenditure.

---

## 📌 Project Overview

- **Project Objective:** Record personal expenses and help users understand monthly spending and category-wise expenditure.
- **Academic Scope:** Single-user learning project using fictional or voluntarily entered expense data. It is an educational tracking system, not a banking or financial-advice system.
- **Key Modules:**
  1. **Expense Management (CRUD):** Add, edit, delete, and list expenses with positive amount enforcement and decimal-safe handling.
  2. **Filtering Engine:** Filter records dynamically by date range (`start_date` to `end_date`), category, and description search. Totals automatically reflect the filtered view.
  3. **Data Analysis with Pandas & NumPy:**
     - **Pandas:** Grouping expenses by month and category, calculating expenditure percentages.
     - **NumPy:** Statistical measures including Mean, Median, Standard Deviation, Min, Max, and Daily Average.
  4. **Data Visualization with Matplotlib:** Category-wise donut/pie chart and month-wise bar chart rendered cleanly on the dashboard.
  5. **Monthly Reports:** Itemized monthly statements with printable/exportable views.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, Vanilla CSS3, Vanilla JavaScript | Responsive financial dashboard, modern dark sidebar, KPI summary cards, filter bars, modals |
| **Backend** | Python Flask (v3.x) | Web routing, form validation, request handling, JSON APIs |
| **Database** | MySQL (with SQLite Fallback) | Relational database storage with foreign key constraints |
| **Data Analysis** | Pandas & NumPy | Grouping by month/category, numerical summary statistics |
| **Data Visualization** | Matplotlib | High-DPI pie and bar chart image generation (rendered as Base64) |

---

## 📂 Project Directory Structure

```text
PersonalExpense tracker/
├── app.py                 # Flask web application entry point and routes
├── config.py              # Configuration loader for environment variables
├── database.py            # MySQL database connection, queries, and CRUD helpers
├── analytics.py           # Pandas, NumPy, and Matplotlib data analysis pipeline
├── init_db.py             # One-click database initialization & test script
├── schema.sql             # MySQL schema definitions + sample fictional data
├── requirements.txt       # Python dependencies list
├── .gitignore             # Git ignore file (keeps .env and caches untracked)
├── .env.example           # Example configuration template
├── README.md              # Project documentation and setup guide
├── static/
│   ├── css/
│   │   └── style.css      # Vanilla CSS styling with modern financial theme
│   └── js/
│       └── app.js         # Client-side validation, AJAX modals, print trigger
└── templates/
    ├── base.html          # Base layout with sidebar, navbar, and modals
    ├── index.html         # Dashboard overview (KPIs, charts, recent transactions)
    ├── expenses.html      # Expense ledger with date/category filters and CRUD
    ├── analytics.html     # Statistical analytics table (NumPy & Pandas)
    ├── reports.html       # Monthly expense report generator & printable view
    └── categories.html    # Category management view
```

---

## 🗄️ Database Schema

### Table 1: `categories`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `category_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique category identifier |
| `category_name` | VARCHAR(100) | NOT NULL, UNIQUE | Name of expense category |

### Table 2: `expenses`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `expense_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique expense identifier |
| `expense_date` | DATE | NOT NULL | Date when the expense occurred |
| `category_id` | INT | FOREIGN KEY (`category_id`) | Category classification reference |
| `amount` | DECIMAL(10, 2) | NOT NULL, CHECK (`amount` > 0) | Monetary amount spent |
| `description` | VARCHAR(255) | NOT NULL | Short note / purpose of expense |
| `payment_method` | VARCHAR(50) | NOT NULL | e.g. UPI, Cash, Credit Card, Debit Card |

---

## 🚀 Step-by-Step Setup Guide

### 1. Prerequisites
- **Python 3.9+** installed on your computer.
- **MySQL Server** (via MySQL Community Server, MySQL Workbench, or XAMPP / WampServer).

---

### 2. Install Python Dependencies
Open your terminal or command prompt inside the project folder:
```bash
cd "PersonalExpense tracker"
pip install -r requirements.txt
```

---

### 3. Configure Database Settings (`.env`)
Copy `.env.example` to `.env` (or edit the existing `.env`):
```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=expense_tracker_db

# Flask Application Secret Key
SECRET_KEY=your_secure_random_flask_secret_key_here
```
> **Security Note:** Never commit your `.env` file to version control. The included `.gitignore` file automatically ensures `.env` stays private on your local machine.

---

### 4. Initialize Database & Load Sample Data

#### Option A: One-click Python script (Recommended)
Simply run:
```bash
python init_db.py
```
This script will connect to your database, create the tables, and insert 30 fictional expense records across various categories and months.

#### Option B: Via MySQL Command Line or Workbench
You can also run the SQL commands directly from `schema.sql`:
```bash
mysql -u root -p < schema.sql
```

---

### 5. Run the Flask Web Application
Start the Flask development server:
```bash
python app.py
```

You should see output similar to:
```text
[*] Starting Personal Expense Tracking and Analysis System on http://127.0.0.1:5000 ...
 * Running on http://127.0.0.1:5000
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Testing Acceptance Criteria

1. **Add an Expense:** Click `+ Add Expense` in the top bar. Try entering a negative number or `0` — notice the client and server validation stops it and enforces positive values. Enter a valid expense (e.g. `250.00`) and verify it appears in the ledger.
2. **Edit & Delete:** In the Expenses Ledger, click the pencil icon to edit an expense via the pop-up modal. Click the trash icon to test deletion with a confirmation prompt.
3. **Date & Category Filters:** Go to **Expenses Ledger**, select a date range (e.g. from `2026-09-01` to `2026-09-30`) or pick `Food & Dining`. Click **Apply Filters**. Verify the **Filtered Total** and matching records update accurately.
4. **Data Analytics:** Navigate to **Data Analytics** to inspect the **NumPy** statistics table (`np.mean`, `np.median`, `np.std`, `np.min`, `np.max`) and the **Pandas** category breakdown table.
5. **Matplotlib Visualizations:** Review the Category Donut/Pie Chart and Monthly Bar Chart on both the Dashboard and the Data Analytics tab.
6. **Monthly Reports:** Click **Monthly Reports**, pick a month (e.g. `2026-10`), and inspect the itemized ledger and category breakdown. Click **Print / Export Statement** to open a print-ready view.
7. **Empty Data Handling:** If all expenses are deleted or no records match a filter, clean, graceful empty state cards appear instead of server errors.

---

## ☁️ Cloud Deployment (TiDB Cloud + Vercel)

This application is ready for serverless deployment on **Vercel** with **TiDB Cloud** (MySQL-compatible managed database).

### 1. Database Configuration (TiDB Cloud)
TiDB Cloud enforces TLS 1.2+ encryption. The application automatically detects remote database hosts and configures TLS/SSL certificate verification using `certifi`.

### 2. Setting Environment Variables in Vercel
When importing your repository into Vercel, navigate to **Project Settings &rarr; Environment Variables** and add:

| Environment Variable | Description / Value |
| :--- | :--- |
| `MYSQL_HOST` | TiDB host (e.g. `gateway01.ap-northeast-1.prod.aws.tidbcloud.com`) |
| `MYSQL_PORT` | `4000` |
| `MYSQL_USER` | TiDB username (e.g. `your_user.root`) |
| `MYSQL_PASSWORD` | Your TiDB Cloud database password |
| `MYSQL_DB` | `expense_tracker_db` |
| `SECRET_KEY` | Random secure string (e.g. 32-character hexadecimal key) |

---

## 📚 Academic Submission Notes
- **Independent Project:** Developed strictly within academic scope without third-party payment gateways, banking APIs, or authentication overhead.
- **Data Integrity:** Strict decimal formatting (`DECIMAL(10,2)` in MySQL, `float` rounded to 2 places in Python) guarantees no fractional currency drift.
- **Code Readability:** Every file contains clear docstrings and comments explaining how backend routes interact with the analytical libraries.



## New account and landing-page features
- Public Home, About, Features and Contact pages.
- Registration, password login, and 6-digit email OTP verification.
- OTP email delivery uses SMTP environment variables documented in `.env.example`. If SMTP is not configured, a development-only OTP is printed to the server log; configure SMTP before public deployment.
- Dashboard pages require a signed-in session and show a time-based greeting.
- Dashboard category donut chart is interactive: click a slice to highlight it and display its value and percentage.
- Playful Neo-Brutalist coral/lime/off-white styling with responsive layouts and motion.

### Important deployment notes
Set a strong random `SECRET_KEY` and configure `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, and `SMTP_FROM` as Render environment variables. The SQLite authentication database (`auth.sqlite3`) must live on a persistent Render disk or be migrated to a managed database; ephemeral filesystems can reset it on redeploy. The existing MySQL expense/category tables are retained as-is. In this iteration, expense/category records remain in the existing shared MySQL schema and are not yet partitioned by account, so do not use this build for multiple users with private financial records until a `user_id` ownership migration is applied.

Contact page currently contains a placeholder. Add your preferred public email address and mobile number when ready.


## Gmail email OTP setup

The registration flow sends a six-digit OTP through Gmail SMTP. Set these variables in your deployment environment:

- `SMTP_HOST=smtp.gmail.com`
- `SMTP_PORT=587`
- `SMTP_USER=25102a04009@gmail.com`
- `SMTP_FROM=25102a04009@gmail.com`
- `SMTP_PASSWORD` = the Gmail App Password you generated (secret; never commit it)
- `SECRET_KEY` = a long, random Flask session secret

For Render, open your service **Environment** settings and add `SMTP_PASSWORD` there. The `render.yaml` intentionally marks it `sync: false`, so the secret is not included in this ZIP or Git repository.

The OTP expires after 10 minutes and allows at most five attempts. Passwords are stored as secure password hashes, not plain text.

### Before real multi-user production use

The existing expense and category database is currently shared by the original project. Registration and login now verify individual accounts, but the existing MySQL expense/category queries have not yet been changed to filter by account owner. Do not use this version for real multi-user private financial data until per-user ownership has been added throughout the database layer.

The account/OTP database is SQLite. On Render, ensure `/var/data` is a mounted persistent disk path; otherwise account records can be lost when the service filesystem is replaced.

## Multi-user data separation

Each verified account has a unique account ID in the authentication database. Every MySQL category and expense row is stored with that account ID (`user_id`). Dashboard totals, charts, analytics, reports, category lists, expense edits, deletes, and the expense JSON endpoint all query by the logged-in account ID. Category ownership is checked before an expense can be added or edited, and record IDs cannot be used to read or modify another account's rows.

Run `python init_db.py` after configuring MySQL. It creates the database if needed and migrates `categories` and `expenses` to include `user_id`. Existing legacy rows are retained with a NULL owner and are deliberately not displayed to any account; they are not automatically assigned to the first person who registers. If you need to preserve old shared records, back up the database and explicitly assign them to the correct account before using the new multi-user version.

The account/authentication database is SQLite by default at `instance/accounts.sqlite3` (configurable with `AUTH_DB_PATH`), while financial records remain in MySQL. On Render or another ephemeral host, configure persistent storage for the SQLite account database as well as MySQL connectivity.
