import sqlite3
import hashlib
from config import DB_NAME


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def connect_db():

    return sqlite3.connect(
        DB_NAME
    )


def create_tables():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            amount REAL,

            category TEXT,

            transaction_type TEXT,

            description TEXT,

            date TEXT,

            user_id INTEGER,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
        """
    )

    conn.commit()

    conn.close()


def register_user(username, password):

    conn = connect_db()

    cursor = conn.cursor()

    try:

        hashed = hash_password(
            password
        )

        cursor.execute(

            """
            INSERT INTO users(
                username,
                password
            )

            VALUES (?,?)
            """,

            (
                username,
                hashed
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = connect_db()

    cursor = conn.cursor()

    hashed = hash_password(
        password
    )

    cursor.execute(

        """
        SELECT *

        FROM users

        WHERE username=?

        AND password=?
        """,

        (
            username,
            hashed
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_transaction(
    amount,
    category,
    transaction_type,
    description,
    date,
    user_id
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO transactions(

            amount,
            category,
            transaction_type,
            description,
            date,
            user_id

        )

        VALUES (?,?,?,?,?,?)
        """,

        (
            amount,
            category,
            transaction_type,
            description,
            date,
            user_id
        )
    )

    conn.commit()

    conn.close()


def get_transactions(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

            id,

            amount,

            category,

            transaction_type,

            description,

            date

        FROM transactions

        WHERE user_id=?
        """,

        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def delete_transaction(transaction_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        DELETE FROM transactions

        WHERE id=?
        """,

        (transaction_id,)
    )

    conn.commit()

    conn.close()


def update_transaction(

    transaction_id,

    amount,

    category,

    transaction_type,

    description,

    date
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE transactions

        SET

            amount=?,

            category=?,

            transaction_type=?,

            description=?,

            date=?

        WHERE id=?
        """,

        (
            amount,
            category,
            transaction_type,
            description,
            date,
            transaction_id
        )
    )

    conn.commit()

    conn.close()


def get_summary(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

            transaction_type,

            SUM(amount)

        FROM transactions

        WHERE user_id=?

        GROUP BY transaction_type
        """,

        (user_id,)
    )

    results = cursor.fetchall()

    conn.close()

    income = 0

    expense = 0

    for row in results:

        if row[0] == "Income":

            income = row[1] or 0

        elif row[0] == "Expense":

            expense = row[1] or 0

    balance = income - expense

    return income, expense, balance


def category_summary(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

            category,

            SUM(amount)

        FROM transactions

        WHERE user_id=?

        AND transaction_type='Expense'

        GROUP BY category
        """,

        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def monthly_summary(user_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

            substr(date,1,7),

            SUM(amount)

        FROM transactions

        WHERE user_id=?

        AND transaction_type='Expense'

        GROUP BY substr(date,1,7)
        """,

        (user_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def filter_transactions(
    user_id,
    category
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

            id,

            amount,

            category,

            transaction_type,

            description,

            date

        FROM transactions

        WHERE user_id=?

        AND category=?
        """,

        (
            user_id,
            category
        )
    )

    data = cursor.fetchall()

    conn.close()

    return data


def filter_date(
    user_id,
    date
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT *

        FROM transactions

        WHERE user_id=?

        AND date=?
        """,

        (
            user_id,
            date
        )
    )

    data = cursor.fetchall()

    conn.close()

    return data


def search_transactions(
    user_id,
    keyword
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT

            id,

            amount,

            category,

            transaction_type,

            description,

            date

        FROM transactions

        WHERE user_id=?

        AND (

            category LIKE ?

            OR description LIKE ?

            OR date LIKE ?

        )
        """,

        (
            user_id,

            f"%{keyword}%",

            f"%{keyword}%",

            f"%{keyword}%"
        )
    )

    data = cursor.fetchall()

    conn.close()

    return data