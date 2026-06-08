# 💰 FinDjango

A personal finance tracker web application built with Django. Track your income and expenses, set monthly budgets, view spending breakdowns and generate monthly reports.

---

## 🚀 Live Demo

🔗 **https://findjango.onrender.com**

⚠️ Free tier — first load may take 30-60 seconds to wake up

---

## ✨ Features

### 👤 User Authentication
- Signup with username and password
- Login and Logout
- Account deletion with password confirmation

### 🧑 Profile System
- Upload profile picture
- Set monthly budget limit
- View joined date

### 💸 Transaction System
- Add income and expense transactions
- Choose from 12 categories (Salary, Food, Transport, Bills etc.)
- Add description and date to each transaction
- Delete any transaction

### 📊 Dashboard
- Total income, total expense and net balance
- Monthly income and expense summary
- Spending breakdown pie chart by category
- Budget usage percentage with warning when exceeded
- 5 most recent transactions at a glance

### 📈 Monthly Reports
- Filter by any month and year
- Income, expense and balance for selected month
- Category-wise expense breakdown
- Full transaction list for the month
- Doughnut chart for visual breakdown

### 🔍 Transaction Filtering
- Filter by type (income / expense)
- Filter by category
- Filter by month

### 📥 CSV Export
- Download all transactions as a CSV file
- Works great for spreadsheet analysis

### 🔐 Admin Panel
- Full Django admin panel for superuser
- Manage users, profiles and transactions from admin

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3 | Backend language |
| Django 6.0 | Web framework |
| SQLite | Database |
| HTML5 / CSS3 | Frontend |
| Chart.js | Pie / doughnut charts |
| Google Fonts | Typography (Syne + DM Sans) |
| Django Auth | Authentication system |
| Django Signals | Auto profile creation on signup |
| Whitenoise | Static file serving |
| Gunicorn | Production WSGI server |

---

## 📁 Project Structure

```
FinDjango/
├── tracker/
│   ├── templates/
│   │   └── tracker/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── dashboard.html
│   │       ├── transactions.html
│   │       ├── add_transaction.html
│   │       ├── monthly_report.html
│   │       ├── profile.html
│   │       ├── login.html
│   │       ├── signup.html
│   │       └── delete_account.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── apps.py
│   └── signals.py
├── findjango/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

---

## ⚙️ How to Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/sumitkumar98313/FinDjango.git
cd FinDjango
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 4 — Create superuser (optional)**
```bash
python manage.py createsuperuser
```

**Step 5 — Start the server**
```bash
python manage.py runserver
```

**Step 6 — Open in browser**
```
http://127.0.0.1:8000/
```

---

## 📌 Pages / URLs

| URL | Page |
|---|---|
| `/` | Home page |
| `/signup/` | Create new account |
| `/login/` | Login |
| `/logout/` | Logout |
| `/dashboard/` | Main dashboard with stats |
| `/transactions/` | All transactions with filters |
| `/transactions/add/` | Add new transaction |
| `/report/` | Monthly report |
| `/export/` | Download CSV |
| `/profile/` | Edit profile and budget |
| `/delete-account/` | Delete account |
| `/admin/` | Admin panel (superuser only) |

---

## 🗄️ Database Models

### Profile
- OneToOne relationship with User
- Profile picture (image, optional)
- Monthly budget (decimal, default 0)

### Transaction
- User (ForeignKey to User)
- Type (income or expense)
- Description (text)
- Amount (decimal)
- Category (choices — 12 options)
- Date (date field)
- Created at (timestamp)

---

## 🔒 Git & Project Hygiene
- `.gitignore` configured — `db.sqlite3`, `__pycache__`, `media/`, `.env` excluded
- Database file not tracked in version control
- Clean commit history

---

## 👨‍💻 Developer

**Sumit Kumar**

- 🎓 BCA Final Year — Chaudhary Charan Singh University, Meerut
- 💼 Python Full Stack Intern — Qspiders, Noida
- 🐙 GitHub: [sumitkumar98313](https://github.com/sumitkumar98313)
- 📧 Email: sumitkumar9867832@gmail.com
- 💼 LinkedIn: [sumit-kumar-97a142368](https://www.linkedin.com/in/sumit-kumar-97a142368)

---

## 📄 License

This project is open source and available for learning purposes.

---

⭐ If you found this project helpful, please give it a star on GitHub!
