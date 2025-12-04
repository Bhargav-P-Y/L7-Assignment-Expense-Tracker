### Expense Tracker:

This project is a Flask + SQLite web application that allows users to:

Log daily expenses
Set monthly budgets per category
View monthly spending reports

Receive alerts if:
A category exceeds its budget
Only 10% of the budget remains


## Steps to Run the Application
# Install dependencies
pip install -r requirements.txt

Initialize the database

Start the Flask app:
python app.py


Then visit:
http://127.0.0.1:5000/init


This creates all required tables.
Add Budgets

Visit: http://127.0.0.1:5000/budget

Enter the data

Add Expenses

Visit: http://127.0.0.1:5000/expense


Enter the data

View Monthly Report

Visit: http://127.0.0.1:5000/report?year=2025&month=3


This shows:
Total spending
Per-category budget vs spending
Over-budget alerts
10% remaining alerts