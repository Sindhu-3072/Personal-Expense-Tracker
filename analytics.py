import matplotlib.pyplot as plt

from database import *

#Pie Chart Function
def show_pie_chart(user_id):

    data = category_summary(
        user_id
    )

    if not data:

        print("No data")

        return

    labels = []

    values = []

    for row in data:

        labels.append(
            row[0]
        )

        values.append(
            row[1]
        )

    plt.figure(
        figsize=(6,6)
    )

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    plt.title(
        "Expense Categories"
    )

    plt.show()

#Monthly Bar Graph
def show_monthly_chart(user_id):

    data = monthly_summary(
        user_id
    )

    if not data:

        print("No data")

        return

    months = []

    amounts = []

    for row in data:

        months.append(
            row[0]
        )

        amounts.append(
            row[1]
        )

    plt.figure(
        figsize=(7,5)
    )

    plt.bar(
        months,
        amounts
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Expense"
    )

    plt.title(
        "Monthly Expenses"
    )

    plt.show()