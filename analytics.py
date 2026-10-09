import plotly.express as px
import streamlit as st
import pandas as pd


def show_spending_analytics(expenses):
    st.header("📊 Category-wise Spending Analytics")

    if expenses.empty:
        st.info("Add expenses to view your spending analytics.")
        return

    category_totals = (
        expenses.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    fig = px.bar(
        category_totals,
        x="category",
        y="amount",
        color="category",
        title="Spending by Category",
        labels={
            "category": "Expense Category",
            "amount": "Total Spending (₹)"
        },
        text_auto=True
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Expense Category",
        yaxis_title="Total Spending (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Category-wise Spending Details")

    category_totals.columns = ["Category", "Total Spending (₹)"]

    st.dataframe(
        category_totals,
        use_container_width=True,
        hide_index=True
    )


def show_daily_category_expenses(expenses):
    st.header("📅 Daily Category-wise Spending")

    if expenses.empty:
        st.info("Add expenses to view daily spending.")
        return

    daily_data = expenses.copy()
    daily_data["date"] = pd.to_datetime(
        daily_data["date"]
    ).dt.date

    available_dates = sorted(
        daily_data["date"].unique(),
        reverse=True
    )

    selected_date = st.selectbox(
        "Select a date",
        available_dates,
        format_func=lambda d: d.strftime("%d %b %Y")
    )

    selected_data = daily_data[
        daily_data["date"] == selected_date
    ]

    category_totals = (
        selected_data.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    total = category_totals["amount"].sum()

    st.metric(
        "💰 Total Spending on Selected Day",
        f"₹{total:,.2f}"
    )

    if not category_totals.empty:
        fig = px.bar(
            category_totals,
            x="category",
            y="amount",
            color="category",
            title=f"Category-wise Expenses on {selected_date}",
            labels={
                "category": "Category",
                "amount": "Amount (₹)"
            },
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            category_totals,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No expenses recorded for this date.")
def show_monthly_expenses(expenses):
    st.header("🗓️ Monthly Spending Analysis")

    if expenses.empty:
        st.info("Add expenses to view monthly spending.")
        return
    monthly_data = expenses.copy()

    monthly_data["date"] = pd.to_datetime(
        monthly_data["date"]
    )

    monthly_data["month"] = (
        monthly_data["date"].dt.to_period("M").astype(str)
    )

    available_months = sorted(
        monthly_data["month"].unique(),
        reverse=True
    )

    selected_month = st.selectbox(
        "Select a month",
        available_months,
        key="monthly_expense_selector"
    )

    selected_data = monthly_data[
        monthly_data["month"] == selected_month
    ]

    category_totals = (
        selected_data.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    total = category_totals["amount"].sum()

    st.metric(
        "💰 Total Spending This Month",
        f"₹{total:,.2f}"
    )

    fig = px.pie(
        category_totals,
        names="category",
        values="amount",
        title=f"Category-wise Spending — {selected_month}",
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}<br>Amount: ₹%{value:,.2f}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Monthly Category Breakdown")

    category_totals.columns = ["Category", "Total Spending (₹)"]

    st.dataframe(
        category_totals,
        use_container_width=True,
        hide_index=True
    )    