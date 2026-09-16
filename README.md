# Personal Expense Tracker

## Project Description
A desktop-based Personal Expense Tracker built using Python, Tkinter, and SQLite, now converted to a Web App using Streamlit. This application allows users to manage expenses, generate reports, and visualize spending patterns from anywhere via browser and mobile.

Live Web App: https://personal-expense-tracker-egj9qjgxsqc7fwqctmt75v.streamlit.app
GitHub Repository: https://github.com/Sindhu-3072/Personal-Expense-Tracker

## Features

- User Registration and Login
- Secure Password Hashing
- Add Transactions
- Update Transactions
- Delete Transactions
- Search Transactions
- Category-wise Filtering
- CSV Export
- Monthly Expense Graph
- Pie Chart Analytics
- Reports Window
- Multi-user Support
- Logout System
- Web & Mobile Responsive (Streamlit Cloud Deployment)

  
## Technologies Used

- Python
- Tkinter (Original Desktop Version)
- Streamlit (Web Version)
- SQLite
- Pandas
- Matplotlib


## Project Structure

Personal-Expense-Tracker/
│
├── app.py                # Streamlit Web App (Converted from Tkinter)
├── main.py               # Original Tkinter Main App
├── login.py
├── dashboard.py
├── expense_manager.py
├── reports.py
├── database.py           # Contains add_transaction(), get_transactions(), update_transaction(), delete_transaction(), search_transactions(), get_summary(), category_summary(), monthly_summary()
├── analytics.py
├── config.py
├── expense.db            # SQLite Database
├── requirements.txt
└── README.md


## How To Run

Install dependencies:
```bash
pip install -r requirements.txt
