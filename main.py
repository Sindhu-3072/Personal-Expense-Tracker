# from database import *

# create_tables()

# print("Database and tables created successfully")

# result = register_user(
#     "park",
#     "1234"
# )

# print("Registration Result:", result)

# user = login_user(
#     "park",
#     "1234"
# )

# print("Login Result:", user)
#---------------------------------------------
from database import create_tables
from login import login_screen

create_tables()

login_screen()
#---------------------------------------------
# from database import create_tables
# from expense_manager import open_expense_manager

# create_tables()

# open_expense_manager(user_id)
#----------------------------------------------
# from database import *

# create_tables()

# conn = connect_db()

# cursor = conn.cursor()

# cursor.execute(
#     "DELETE FROM transactions"
# )

# cursor.execute(
#     "DELETE FROM sqlite_sequence WHERE name='transactions'"
# )

# conn.commit()

# conn.close()

# print("Reset complete")
