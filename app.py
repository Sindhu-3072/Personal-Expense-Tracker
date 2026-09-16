import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import *
from config import CATEGORIES

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Create tables (your function)
create_tables()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""
    st.session_state.selected_id = None

# ========== LOGIN ==========
if not st.session_state.logged_in:
    st.title("💰 Personal Expense Tracker")
    st.caption("Web version of your Tkinter app")

    t1, t2 = st.tabs(["Login", "Register"])
    with t1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login", type="primary"):
            user = login_user(u, p)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong username or password")

    with t2:
        nu = st.text_input("New Username", key="nu")
        np = st.text_input("New Password", type="password", key="np")
        if st.button("Create Account"):
            if register_user(nu, np):
                st.success("Account created! Now go to Login tab.")
            else:
                st.error("Username already exists")

# ========== DASHBOARD ==========
else:
    st.sidebar.success(f"Logged in: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(f"Welcome {st.session_state.username}")

    # Summary like your analytics.py
    income, expense, balance = get_summary(st.session_state.user_id)
    m1, m2, m3 = st.columns(3)
    m1.metric("💵 Total Income", f"₹ {income}")
    m2.metric("💸 Total Expense", f"₹ {expense}")
    m3.metric("💰 Balance", f"₹ {balance}")

    st.divider()

    # Add Form - SAME AS YOUR Tkinter form
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount", min_value=0.01)
        category = st.selectbox("Category", CATEGORIES)
        t_type = st.selectbox("Type", ["Income", "Expense"])
    with col2:
        desc = st.text_input("Description")
        date = st.text_input("Date YYYY-MM-DD", value="2025-05-13")
        keyword = st.text_input("Search (category/desc/date)")

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("💾 Save", use_container_width=True):
            if desc == "" or date == "":
                st.error("Description & Date required")
            else:
                add_transaction(amount, category, t_type, desc, date, st.session_state.user_id)
                st.success("Saved!")
                st.rerun()
    with b2:
        if st.button("✏️ Update Selected", use_container_width=True):
            if st.session_state.selected_id is None:
                st.error("Select a row from table below first")
            else:
                update_transaction(st.session_state.selected_id, amount, category, t_type, desc, date)
                st.success(f"Updated ID {st.session_state.selected_id}")
                st.rerun()
    with b3:
        if st.button("🗑️ Delete Selected", use_container_width=True):
            if st.session_state.selected_id is None:
                st.error("Select a row first")
            else:
                delete_transaction(st.session_state.selected_id)
                st.session_state.selected_id = None
                st.success("Deleted")
                st.rerun()
    with b4:
        if st.button("🔍 Search", use_container_width=True):
            res = search_transactions(st.session_state.user_id, keyword)
            if res:
                st.dataframe(pd.DataFrame(res, columns=["ID","Amount","Category","Type","Description","Date"]), use_container_width=True)
            else:
                st.warning("No results")

    st.divider()
    # Transaction Table - SAME AS treeview
    data = get_transactions(st.session_state.user_id)
    if not data:
        st.info("No transactions yet")
    else:
        df = pd.DataFrame(data, columns=["ID","Amount","Category","Type","Description","Date"])
        st.subheader(f"Your Transactions - Total {len(df)}")
        st.caption("Click a row to select it for Update/Delete")

        event = st.dataframe(df, use_container_width=True, on_select="rerun", selection_mode="single-row")

        if len(event.selection.rows) > 0:
            idx = event.selection.rows[0]
            row = df.iloc[idx]
            st.session_state.selected_id = int(row["ID"])
            st.info(f"✅ Selected ID {row['ID']} | {row['Amount']} | {row['Category']} | {row['Description']}")

        # Analytics - from your category_summary and monthly_summary
        st.divider()
        st.subheader("📊 Analytics")
        c1, c2 = st.columns(2)
        with c1:
            cat_data = category_summary(st.session_state.user_id)
            if cat_data:
                cat_df = pd.DataFrame(cat_data, columns=["Category","Total"])
                fig, ax = plt.subplots()
                ax.pie(cat_df["Total"], labels=cat_df["Category"], autopct='%1.1f%%')
                ax.set_title("Expense by Category")
                st.pyplot(fig)
                st.dataframe(cat_df, use_container_width=True)
            else:
                st.write("No expense data for chart")

        with c2:
            mon_data = monthly_summary(st.session_state.user_id)
            if mon_data:
                mon_df = pd.DataFrame(mon_data, columns=["Month","Total"])
                st.bar_chart(mon_df.set_index("Month"))
                st.dataframe(mon_df, use_container_width=True)
