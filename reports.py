import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

from database import *
from config import CATEGORIES


# Colors
BG_COLOR = "#1E1E2F"
BTN_COLOR = "#4CAF50"
TEXT_COLOR = "white"
ENTRY_COLOR = "#F5F5F5"


def open_reports(user_id):

    root = tk.Toplevel()

    root.title(
        "Reports"
    )

    root.geometry(
        "850x550"
    )

    root.configure(
        bg=BG_COLOR
    )

    # Table styling
    style = ttk.Style()

    style.theme_use(
        "clam"
    )

    style.configure(

        "Treeview",

        rowheight=28,

        font=("Arial", 10)

    )

    style.configure(

        "Treeview.Heading",

        font=("Arial", 10, "bold")

    )

    # Title
    tk.Label(

        root,

        text="Reports & Export",

        bg=BG_COLOR,

        fg=TEXT_COLOR,

        font=("Arial", 16, "bold")

    ).pack(
        pady=15
    )

    # Category label
    tk.Label(

        root,

        text="Select Category",

        bg=BG_COLOR,

        fg=TEXT_COLOR,

        font=("Arial", 11)

    ).pack()

    category_box = ttk.Combobox(

        root,

        values=CATEGORIES,

        width=25

    )

    category_box.pack(
        pady=10
    )

    columns = (

        "ID",

        "Amount",

        "Category",

        "Type",

        "Description",

        "Date"
    )

    tree = ttk.Treeview(

        root,

        columns=columns,

        show="headings",

        height=15
    )

    for col in columns:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            width=120
        )

    tree.pack(

        fill="both",

        expand=True,

        padx=20,

        pady=20
    )

    def apply_filter():

        category = category_box.get()

        data = filter_transactions(

            user_id,

            category
        )

        for row in tree.get_children():

            tree.delete(row)

        for row in data:

            tree.insert(

                "",

                tk.END,

                values=row
            )

    def export_csv():

        data = get_transactions(
            user_id
        )

        df = pd.DataFrame(

            data,

            columns=[

                "ID",

                "Amount",

                "Category",

                "Type",

                "Description",

                "Date"
            ]
        )

        df.to_csv(

            "transactions.csv",

            index=False
        )

        messagebox.showinfo(

            "Success",

            "CSV Exported Successfully"
        )

    button_style = {

        "bg": BTN_COLOR,

        "fg": "white",

        "font": ("Arial", 10, "bold"),

        "width": 15
    }

    tk.Button(

        root,

        text="Filter",

        command=apply_filter,

        **button_style

    ).pack(
        pady=5
    )

    tk.Button(

        root,

        text="Export CSV",

        command=export_csv,

        bg="#2196F3",

        fg="white",

        width=15,

        font=("Arial", 10, "bold")

    ).pack(
        pady=10
    )