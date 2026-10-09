import sqlite3
import pandas as pd

DB_NAME = "expenses.db"


def create_table():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            merchant TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_expense(date, amount, category, merchant):
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        INSERT INTO expenses (date, amount, category, merchant)
        VALUES (?, ?, ?, ?)
    """, (str(date), amount, category, merchant))

    connection.commit()
    connection.close()


def get_expenses():
    connection = sqlite3.connect(DB_NAME)

    data = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY date DESC",
        connection
    )

    connection.close()

    return data
def clear_expenses():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("DELETE FROM expenses")

    connection.commit()
    connection.close()    