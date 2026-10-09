def detect_anomalies(expenses):
    expenses = expenses.copy()

    expenses["category"] = expenses["category"].astype(str)
    expenses["anomaly"] = "Normal ✅"
    expenses["reason"] = "Amount is within your usual spending range."

    if len(expenses) < 5:
        expenses["anomaly"] = "Not Enough Data"
        expenses["reason"] = "Add at least 5 expenses for analysis."
        return expenses

    average = expenses["amount"].mean()
    std = expenses["amount"].std()

    for index, row in expenses.iterrows():
        amount = row["amount"]

        if std > 0 and abs(amount - average) > 2 * std:
            expenses.at[index, "anomaly"] = "Anomaly ⚠️"

            if amount > average:
                expenses.at[index, "reason"] = (
                    f"Amount ₹{amount:.2f} is unusually high "
                    f"compared with overall average ₹{average:.2f}."
                )
            else:
                expenses.at[index, "reason"] = (
                    f"Amount ₹{amount:.2f} is unusually low "
                    f"compared with overall average ₹{average:.2f}."
                )

    for category in expenses["category"].unique():
        category_mask = expenses["category"] == category
        category_data = expenses.loc[category_mask, "amount"]

        if len(category_data) < 5:
            continue

        category_average = category_data.mean()
        category_std = category_data.std()

        if category_std == 0:
            continue

        for index in expenses.index[category_mask]:
            amount = expenses.at[index, "amount"]

            if abs(amount - category_average) > 2 * category_std:
                expenses.at[index, "anomaly"] = "Anomaly ⚠️"
                expenses.at[index, "reason"] = (
                    f"Unusual amount for {category}: "
                    f"₹{amount:.2f}; category average is "
                    f"₹{category_average:.2f}."
                )

    return expenses