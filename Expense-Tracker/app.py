from flask import Flask, render_template, request
from database import init_db
import sqlite3

app = Flask(__name__)

@app.route('/init')
def initialize():
    init_db()
    return "Database initialized."

@app.route('/')
def home():
    return "Expense Tracker Running"

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        category = request.form['category']
        amount = request.form['amount']

        conn = sqlite3.connect('expense.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO budgets (year, month, category_id, amount)
            VALUES (?, ?, (SELECT category_id FROM categories WHERE category_name = ?), ?)
        """, (year, month, category, amount))

        conn.commit()
        conn.close()
        return "Budget saved!"

    return render_template('budget_form.html')


@app.route('/expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']

        conn = sqlite3.connect('expense.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO expenses (date, category_id, amount)
            VALUES (?, (SELECT category_id FROM categories WHERE category_name = ?), ?)
        """, (date, category, amount))

        conn.commit()
        conn.close()
        return "Expense saved!"

    return render_template('expense_form.html')


@app.route('/report')
def report():
    year = request.args.get('year')
    month = request.args.get('month')

    conn = sqlite3.connect('expense.db')
    cur = conn.cursor()

    # Total Spending
    cur.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE strftime('%Y', date) = ?
          AND strftime('%m', date) = ?
    """, (year, month))
    total = cur.fetchone()[0]

    # Category Summary
    cur.execute("""
        SELECT 
            c.category_name,
            b.amount AS budget,
            IFNULL(SUM(e.amount), 0) AS spent,
            b.amount - IFNULL(SUM(e.amount), 0) AS remaining
        FROM budgets b
        JOIN categories c ON c.category_id = b.category_id
        LEFT JOIN expenses e 
           ON e.category_id = b.category_id
           AND strftime('%Y', e.date) = ?
           AND strftime('%m', e.date) = ?
        WHERE b.year = ?
          AND b.month = ?
        GROUP BY c.category_name, b.amount;
    """, (year, month, year, month))
    summary = cur.fetchall()

    # Over Budget
    cur.execute("""
        SELECT 
            c.category_name,
            b.amount AS budget,
            IFNULL(SUM(e.amount), 0) AS spent,
            b.amount - IFNULL(SUM(e.amount), 0) AS remaining
        FROM budgets b
        JOIN categories c ON c.category_id = b.category_id
        LEFT JOIN expenses e
            ON e.category_id = b.category_id
            AND strftime('%Y', e.date) = ?
            AND strftime('%m', e.date) = ?
        WHERE b.year = ?
          AND b.month = ?
        GROUP BY c.category_name, b.amount
        HAVING IFNULL(SUM(e.amount), 0) > b.amount;
    """, (year, month, year, month))
    over_budget = cur.fetchall()

    # Low Budget (10% Remaining)
    cur.execute("""
        SELECT 
            c.category_name,
            b.amount AS budget,
            IFNULL(SUM(e.amount), 0) AS spent,
            b.amount - IFNULL(SUM(e.amount), 0) AS remaining
        FROM budgets b
        JOIN categories c ON c.category_id = b.category_id
        LEFT JOIN expenses e
            ON e.category_id = b.category_id
            AND strftime('%Y', e.date) = ?
            AND strftime('%m', e.date) = ?
        WHERE b.year = ?
          AND b.month = ?
        GROUP BY c.category_name, b.amount
        HAVING IFNULL(SUM(e.amount), 0) >= 0.9 * b.amount;
    """, (year, month, year, month))
    low_budget = cur.fetchall()

    conn.close()

    return render_template("report.html",
                           total=total,
                           summary=summary,
                           over_budget=over_budget,
                           low_budget=low_budget)


if __name__ == '__main__':
    app.run(debug=True)
