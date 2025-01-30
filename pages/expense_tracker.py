import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime
import os

def load_expenses():
    if os.path.exists('expenses.json'):
        with open('expenses.json', 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open('expenses.json', 'w') as f:
        json.dump(expenses, f)

def main():
    st.set_page_config(page_title="Expense Tracker", page_icon="💵", layout="wide")
    
    st.title("💵 Expense Tracker & Budget Planner")
    st.write("Track your expenses and plan your budget")
    
    # Initialize session state for expenses if not exists
    if 'expenses' not in st.session_state:
        st.session_state.expenses = load_expenses()
    
    # Sidebar for budget planning
    st.sidebar.header("Monthly Budget Planning")
    categories = ["Housing", "Transportation", "Food", "Utilities", "Healthcare", 
                 "Entertainment", "Shopping", "Education", "Savings", "Other"]
    
    budget_data = {}
    total_budget = 0
    for category in categories:
        budget_data[category] = st.sidebar.number_input(f"{category} Budget (₹)", 
                                                      min_value=0, value=1000, step=100)
        total_budget += budget_data[category]
    
    st.sidebar.markdown(f"### Total Budget: ₹{total_budget:,.2f}")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Add Expense", "View Expenses", "Analysis"])
    
    # Add Expense Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount (₹)", min_value=0.0, value=0.0)
            category = st.selectbox("Category", categories)
            description = st.text_input("Description")
            date = st.date_input("Date")
            
            if st.button("Add Expense"):
                expense = {
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "date": date.strftime("%Y-%m-%d")
                }
                st.session_state.expenses.append(expense)
                save_expenses(st.session_state.expenses)
                st.success("Expense added successfully!")
    
    # View Expenses Tab
    with tab2:
        if st.session_state.expenses:
            df = pd.DataFrame(st.session_state.expenses)
            df['date'] = pd.to_datetime(df['date'])
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                selected_month = st.selectbox(
                    "Select Month",
                    options=sorted(df['date'].dt.strftime("%Y-%m").unique())
                )
            with col2:
                selected_category = st.multiselect(
                    "Select Categories",
                    options=categories,
                    default=categories
                )
            
            # Filter data
            mask = (df['date'].dt.strftime("%Y-%m") == selected_month) & \
                   (df['category'].isin(selected_category))
            filtered_df = df[mask]
            
            # Display expenses
            if not filtered_df.empty:
                st.dataframe(
                    filtered_df.sort_values('date', ascending=False)
                    .style.format({'amount': '₹{:,.2f}'})
                )
                
                total_expenses = filtered_df['amount'].sum()
                st.info(f"Total Expenses: ₹{total_expenses:,.2f}")
            else:
                st.write("No expenses found for the selected filters.")
    
    # Analysis Tab
    with tab3:
        if st.session_state.expenses:
            df = pd.DataFrame(st.session_state.expenses)
            df['date'] = pd.to_datetime(df['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Category-wise breakdown
                category_expenses = df.groupby('category')['amount'].sum()
                
                fig1 = go.Figure(data=[go.Pie(
                    labels=category_expenses.index,
                    values=category_expenses.values,
                    hole=.3
                )])
                fig1.update_layout(title="Expenses by Category")
                st.plotly_chart(fig1)
                
                # Compare with budget
                comparison_data = []
                for category in categories:
                    spent = category_expenses.get(category, 0)
                    budgeted = budget_data[category]
                    comparison_data.append({
                        'Category': category,
                        'Spent': spent,
                        'Budget': budgeted,
                        'Remaining': budgeted - spent
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                st.markdown("### Budget vs Actual Spending")
                st.dataframe(
                    comparison_df
                    .style.format({
                        'Spent': '₹{:,.2f}',
                        'Budget': '₹{:,.2f}',
                        'Remaining': '₹{:,.2f}'
                    })
                )
            
            with col2:
                # Trend over time
                daily_expenses = df.groupby('date')['amount'].sum().reset_index()
                fig2 = px.line(daily_expenses, x='date', y='amount',
                             title='Daily Expenses Trend')
                st.plotly_chart(fig2)
                
                # Spending insights
                st.markdown("### 💡 Spending Insights")
                total_spent = df['amount'].sum()
                st.info(f"Total Spent: ₹{total_spent:,.2f}")
                
                if total_spent > total_budget:
                    st.error(f"Over Budget by: ₹{total_spent - total_budget:,.2f}")
                else:
                    st.success(f"Under Budget by: ₹{total_budget - total_spent:,.2f}")
                
                # Category with highest spending
                highest_category = category_expenses.idxmax()
                st.warning(f"Highest spending in {highest_category}: ₹{category_expenses[highest_category]:,.2f}")
        else:
            st.write("Add some expenses to see the analysis!")

if __name__ == "__main__":
    main()
