import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import *
from config import CATEGORIES


# Colors
BG_COLOR = "#1E1E2F"
BTN_COLOR = "#4CAF50"
TEXT_COLOR = "white"
ENTRY_COLOR = "#F5F5F5"

selected_transaction = None


def select_row(event):

    global selected_transaction

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(
        selected,
        "values"
    )

    selected_transaction = values[0]

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, str(values[1]))

    category_box.set(values[2])

    type_box.set(values[3])

    desc_entry.delete(0, tk.END)
    desc_entry.insert(0, str(values[4]))

    date_entry.delete(0, tk.END)
    date_entry.insert(0, str(values[5]))


def validate_inputs():

    if amount_entry.get() == "":

        messagebox.showerror(
            "Error",
            "Amount required"
        )

        return False

    try:

        float(amount_entry.get())

    except:

        messagebox.showerror(
            "Error",
            "Enter valid amount"
        )

        return False

    if desc_entry.get() == "":

        messagebox.showerror(
            "Error",
            "Description required"
        )

        return False

    if len(date_entry.get()) != 10:

        messagebox.showerror(
            "Error",
            "Use YYYY-MM-DD"
        )

        return False

    return True


def save_transaction(user_id):

    if not validate_inputs():
        return

    add_transaction(

        float(amount_entry.get()),

        category_box.get(),

        type_box.get(),

        desc_entry.get(),

        date_entry.get(),

        user_id
    )

    load_transactions(user_id)


def load_transactions(user_id):

    for row in tree.get_children():

        tree.delete(row)

    data = get_transactions(user_id)

    for record in data:

        tree.insert(
            "",
            tk.END,
            values=record
        )


def delete_selected(user_id):

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(
        selected,
        "values"
    )

    delete_transaction(values[0])

    load_transactions(user_id)


def update_selected(user_id):

    global selected_transaction

    if selected_transaction is None:

        messagebox.showerror(
            "Error",
            "Select transaction first"
        )

        return

    if not validate_inputs():
        return

    update_transaction(

        selected_transaction,

        float(amount_entry.get()),

        category_box.get(),

        type_box.get(),

        desc_entry.get(),

        date_entry.get()
    )

    load_transactions(user_id)


def search_data(user_id):

    keyword = search_entry.get()

    results = search_transactions(
        user_id,
        keyword
    )

    for row in tree.get_children():

        tree.delete(row)

    for row in results:

        tree.insert(
            "",
            tk.END,
            values=row
        )


def open_expense_manager(user_id):

    global amount_entry
    global category_box
    global type_box
    global desc_entry
    global date_entry
    global tree
    global search_entry

    root = tk.Toplevel()

    root.title(
        "Expense Manager"
    )

    root.geometry(
        "950x650"
    )

    root.configure(
        bg=BG_COLOR
    )

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

    labels = [
        #"S,No",

        "Amount",

        "Category",

        "Type",

        "Description",

        "Date"
    ]

    for i, text in enumerate(labels):

        tk.Label(

            root,

            text=text,

            bg=BG_COLOR,

            fg=TEXT_COLOR,

            font=("Arial", 11)

        ).grid(

            row=i,

            column=0,

            padx=10,

            pady=10,

            sticky="w"
        )

    amount_entry = tk.Entry(

        root,

        width=25,

        bg=ENTRY_COLOR
    )

    amount_entry.grid(row=0, column=1)

    category_box = ttk.Combobox(

        root,

        values=CATEGORIES,

        width=22
    )

    category_box.grid(row=1, column=1)

    type_box = ttk.Combobox(

        root,

        values=["Income", "Expense"],

        width=22
    )

    type_box.grid(row=2, column=1)

    desc_entry = tk.Entry(

        root,

        width=25,

        bg=ENTRY_COLOR
    )

    desc_entry.grid(row=3, column=1)

    date_entry = tk.Entry(

        root,

        width=25,

        bg=ENTRY_COLOR
    )

    date_entry.grid(row=4, column=1)

    button_style = {

        "bg": BTN_COLOR,

        "fg": "white",

        "font": ("Arial", 10, "bold"),

        "width": 12
    }

    tk.Button(

        root,

        text="Save",

        command=lambda:
        save_transaction(user_id),

        **button_style

    ).grid(row=5, column=0, pady=10)

    tk.Button(

        root,

        text="Delete",

        command=lambda:
        delete_selected(user_id),

        bg="#D9534F",

        fg="white",

        width=12

    ).grid(row=5, column=1)

    tk.Button(

        root,

        text="Update",

        command=lambda:
        update_selected(user_id),

        **button_style

    ).grid(row=5, column=2)

    search_entry = tk.Entry(

        root,

        width=25
    )

    search_entry.grid(
        row=6,
        column=0,
        pady=15
    )

    tk.Button(

        root,

        text="Search",

        command=lambda:
        search_data(user_id),

        **button_style

    ).grid(
        row=6,
        column=1
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
            width=130
        )

    tree.grid(

        row=7,

        column=0,

        columnspan=4,

        padx=20,

        pady=20,

        sticky="nsew"
    )

    tree.bind(
        "<<TreeviewSelect>>",
        select_row
    )

    load_transactions(user_id)

    root.mainloop()