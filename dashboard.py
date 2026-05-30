import tkinter as tk

from database import get_summary
from expense_manager import open_expense_manager
from analytics import show_pie_chart
from analytics import show_monthly_chart
from reports import open_reports


# Colors
BG_COLOR = "#1E1E2F"
BTN_COLOR = "#4CAF50"
TEXT_COLOR = "white"


def open_dashboard(user_id):

    root = tk.Toplevel()

    root.title(
        "Dashboard"
    )

    root.geometry(
        "400x450"
    )

    root.configure(
        bg=BG_COLOR
    )

    income, expense, balance = get_summary(
        user_id
    )

    def logout():

        root.destroy()

        from login import login_screen

        login_screen()

    # Heading
    tk.Label(

        root,

        text="Expense Tracker Dashboard",

        bg=BG_COLOR,

        fg=TEXT_COLOR,

        font=("Arial", 16, "bold")

    ).pack(
        pady=15
    )

    # Summary labels
    tk.Label(

        root,

        text=f"Income : ₹{income}",

        bg=BG_COLOR,

        fg="lightgreen",

        font=("Arial", 12, "bold")

    ).pack(
        pady=8
    )

    tk.Label(

        root,

        text=f"Expense : ₹{expense}",

        bg=BG_COLOR,

        fg="#FF7070",

        font=("Arial", 12, "bold")

    ).pack(
        pady=8
    )

    tk.Label(

        root,

        text=f"Balance : ₹{balance}",

        bg=BG_COLOR,

        fg="cyan",

        font=("Arial", 12, "bold")

    ).pack(
        pady=8
    )

    # Buttons
    button_style = {

        "bg": BTN_COLOR,

        "fg": "white",

        "font": ("Arial", 10, "bold"),

        "width": 20
    }

    tk.Button(

        root,

        text="Expense Manager",

        command=lambda:
        open_expense_manager(user_id),

        **button_style

    ).pack(
        pady=8
    )

    tk.Button(

        root,

        text="Category Chart",

        command=lambda:
        show_pie_chart(user_id),

        **button_style

    ).pack(
        pady=8
    )

    tk.Button(

        root,

        text="Monthly Graph",

        command=lambda:
        show_monthly_chart(user_id),

        **button_style

    ).pack(
        pady=8
    )

    tk.Button(

        root,

        text="Reports",

        command=lambda:
        open_reports(user_id),

        **button_style

    ).pack(
        pady=8
    )

    tk.Button(

        root,

        text="Logout",

        command=logout,

        bg="#D9534F",

        fg="white",

        width=20,

        font=("Arial", 10, "bold")

    ).pack(
        pady=15
    )