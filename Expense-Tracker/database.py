import sqlite3

def init_db():
    conn = sqlite3.connect('expense.db')
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id INTEGER PRIMARY KEY,
            year INTEGER,
            month INTEGER CHECK(month BETWEEN 1 AND 12),
            category_id INTEGER REFERENCES categories(category_id),
            amount NUMERIC(10,2),
            UNIQUE(year, month, category_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            category_id INTEGER REFERENCES categories(category_id),
            amount NUMERIC(10,2)
        );
    """)

    conn.commit()
    conn.close()
