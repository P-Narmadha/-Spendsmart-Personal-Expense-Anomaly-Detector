import streamlit as st
from database import create_table, add_expense, get_expenses
from anomaly_detector import detect_anomalies
st.set_page_config(
    page_title="SpendSmart AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 SpendSmart AI")
st.subheader("Personal Expense Anomaly Detector")
st.divider()

st.header("📊 Dashboard Overview")

expenses = get_expenses()

if not expenses.empty:
    total_spending = expenses["amount"].sum()
    total_transactions = len(expenses)

    anomaly_data = detect_anomalies(expenses.copy())

    anomaly_count = (
        anomaly_data["anomaly"] == "Anomaly ⚠️"
    ).sum()

    normal_count = (
        anomaly_data["anomaly"] == "Normal ✅"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Spending", f"₹{total_spending:,.2f}")
    col2.metric("🧾 Total Transactions", total_transactions)
    col3.metric("⚠️ Anomalies", int(anomaly_count))
    col4.metric("✅ Normal Expenses", int(normal_count))

else:
    st.info("Add expenses to view your dashboard.")

st.write("Track your expenses and identify unusual spending patterns.")

st.divider()

st.header("Add a New Expense")

with st.form("expense_form"):
    date = st.date_input("Expense Date")

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        value=100.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Shopping",
         "Education", "Entertainment", "Other"]
    )

    merchant = st.text_input("Merchant Name")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        st.success("Expense added successfully!")

        st.write("Date:", date)
        st.write("Amount: ₹", amount)
        st.write("Category:", category)
        st.write("Merchant:", merchant)


import streamlit as st
from database import create_table, add_expense, get_expenses
from analytics import (
    show_spending_analytics,
    show_daily_category_expenses,
    show_monthly_expenses
)
from anomaly_detector import detect_anomalies

# Configure the application
st.set_page_config(
    page_title="SpendSmart AI",
    page_icon="💰",
    layout="wide"
)

# Create database table
create_table()

# Application heading
st.title("💰 SpendSmart AI")
st.subheader("Personal Expense Anomaly Detector")

st.write(
    "Track your expenses and understand your spending behaviour."
)

st.divider()

# Expense entry form
st.header("➕ Add a New Expense")

with st.form("expense_form_new"):

    date = st.date_input("Expense Date")

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        value=100.0
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Education",
            "Entertainment",
            "Other"
        ]
    )

    merchant = st.text_input("Merchant Name")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if not merchant.strip():
            st.error("Please enter the merchant name.")

        else:
            add_expense(
                date,
                amount,
                category,
                merchant.strip()
            )

            st.success("Expense saved successfully!")
            st.rerun()

st.divider()

# Transaction history
st.header("📋 Transaction History")

expenses = get_expenses()

if not expenses.empty:

    st.dataframe(
        expenses,
        use_container_width=True,
        hide_index=True
    )

    total = expenses["amount"].sum()

    st.metric(
        "Total Spending",
        f"₹{total:,.2f}"
    )

else:
    st.info("No expenses recorded yet. Add your first expense!")
st.divider()

show_spending_analytics(get_expenses())    
st.divider()

st.header("🤖 AI Expense Anomaly Detection")

expenses = get_expenses()

if not expenses.empty:
    analyzed_expenses = detect_anomalies(expenses.copy())

    st.subheader("Expense Analysis")

    st.dataframe(
        analyzed_expenses,
        use_container_width=True,
        hide_index=True
    )

    if "Anomaly ⚠️" in analyzed_expenses["anomaly"].values:
        st.warning("Unusual expenses detected! Please review them.")
    elif "Not Enough Data" in analyzed_expenses["anomaly"].values:
        st.info("Add at least 5 expenses to start anomaly detection.")
    else:
        st.success("No unusual expenses detected!")
else:
    st.info("Add expenses to start AI analysis.")

st.divider()
st.header("📝 Spending Summary")

expenses = get_expenses()

if not expenses.empty:
    total_spending = expenses["amount"].sum()
    total_transactions = len(expenses)
    average_expense = expenses["amount"].mean()

    category_totals = expenses.groupby("category")["amount"].sum()
    highest_category = category_totals.idxmax()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Spending",
        f"₹{total_spending:,.2f}"
    )

    col2.metric(
        "🧾 Average Expense",
        f"₹{average_expense:,.2f}"
    )

    col3.metric(
        "🏆 Top Spending Category",
        highest_category
    )

    st.write(
        f"You have recorded {total_transactions} transactions."
    )

else:
    st.info("Add expenses to generate your spending summary.")  
st.divider()
show_daily_category_expenses(get_expenses())
st.divider()
show_monthly_expenses(get_expenses())