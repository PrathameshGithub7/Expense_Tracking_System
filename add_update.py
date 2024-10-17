import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    st.subheader("Add or Update Expenses")
    selected_date = st.date_input("Select Date", datetime(2024, 8, 1))
    
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        existing_expenses = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve expenses: {e}")
        st.error("Please ensure the FastAPI server is running and accessible.")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        st.write("Enter Expenses")
        col1, col2, col3 = st.columns(3)
        col1.write("Amount")
        col2.write("Category")
        col3.write("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            amount_input = col1.number_input("Amount", min_value=0.0, step=1.0, value=float(amount), key=f"amount_{i}", label_visibility="collapsed")
            category_input = col2.selectbox("Category", options=categories, index=categories.index(category), key=f"category_{i}", label_visibility="collapsed")
            notes_input = col3.text_input("Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Update Expenses")
        
    if submit_button:
        filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

        try:
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            response.raise_for_status()
            st.success("Expenses updated successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to update expenses: {e}")
            st.error("Please ensure the FastAPI server is running and accessible.")

    # Display current expenses
    if existing_expenses:
        st.subheader("Current Expenses")
        for expense in existing_expenses:
            st.write(f"Amount: ${expense['amount']:.2f}, Category: {expense['category']}, Notes: {expense['notes']}")
    else:
        st.info("No existing expenses for this date.")
