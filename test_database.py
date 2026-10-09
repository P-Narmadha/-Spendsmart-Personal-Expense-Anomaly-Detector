from database import create_table, add_expense, get_expenses

create_table()
print("Database table created successfully!")

add_expense("2026-10-09", 250, "Food", "Restaurant")
print("Expense added successfully!")

expenses = get_expenses()

print("\nSaved Expenses:")
print(expenses)