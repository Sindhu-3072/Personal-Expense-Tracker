import tkinter as tk
from tkinter import messagebox

from database import register_user
from database import login_user
from dashboard import open_dashboard


# Colors
BG_COLOR = "#1E1E2F"
BTN_COLOR = "#4CAF50"
TEXT_COLOR = "white"
ENTRY_COLOR = "#F5F5F5"


def register():

    username = username_entry.get()

    password = password_entry.get()

    if username == "" or password == "":

        messagebox.showerror(

            "Error",

            "Fields cannot be empty"

        )

        return

    success = register_user(

        username,

        password
    )

    if success:

        messagebox.showinfo(

            "Success",

            "Registration successful"

        )

    else:

        messagebox.showerror(

            "Error",

            "Username already exists"

        )


def login():

    username = username_entry.get()

    password = password_entry.get()

    user = login_user(

        username,

        password
    )

    if user:

        messagebox.showinfo(

            "Success",

            "Login successful"

        )

        root.withdraw()

        open_dashboard(
            user[0]
        )

    else:

        messagebox.showerror(

            "Error",

            "Invalid credentials"

        )


def login_screen():

    global username_entry
    global password_entry
    global root

    root = tk.Tk()

    root.title(
        "Expense Tracker Login"
    )

    root.geometry(
        "400x320"
    )

    root.configure(
        bg=BG_COLOR
    )

    # Heading
    tk.Label(

        root,

        text="Expense Tracker",

        bg=BG_COLOR,

        fg=TEXT_COLOR,

        font=("Arial", 18, "bold")

    ).pack(
        pady=20
    )

    tk.Label(

        root,

        text="Username",

        bg=BG_COLOR,

        fg=TEXT_COLOR,

        font=("Arial", 11)

    ).pack(
        pady=5
    )

    username_entry = tk.Entry(

        root,

        width=30,

        bg=ENTRY_COLOR,

        font=("Arial", 10)

    )

    username_entry.pack(
        pady=5
    )

    tk.Label(

        root,

        text="Password",

        bg=BG_COLOR,

        fg=TEXT_COLOR,

        font=("Arial", 11)

    ).pack(
        pady=5
    )

    password_entry = tk.Entry(

        root,

        show="*",

        width=30,

        bg=ENTRY_COLOR,

        font=("Arial", 10)

    )

    password_entry.pack(
        pady=5
    )

    tk.Button(

        root,

        text="Register",

        command=register,

        bg=BTN_COLOR,

        fg="white",

        width=18,

        font=("Arial", 10, "bold")

    ).pack(
        pady=12
    )

    tk.Button(

        root,

        text="Login",

        command=login,

        bg="#2196F3",

        fg="white",

        width=18,

        font=("Arial", 10, "bold")

    ).pack(
        pady=5
    )

    root.mainloop()