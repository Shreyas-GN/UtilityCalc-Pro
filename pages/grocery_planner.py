import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime, timedelta

def load_grocery_data():
    if os.path.exists('grocery_data.json'):
        with open('grocery_data.json', 'r') as f:
            return json.load(f)
    return {"items": [], "meals": [], "shopping_lists": []}

def save_grocery_data(data):
    with open('grocery_data.json', 'w') as f:
        json.dump(data, f)

# Common grocery categories and items
GROCERY_CATEGORIES = {
    "Fruits & Vegetables": [
        "Apples", "Bananas", "Oranges", "Tomatoes", "Potatoes", "Onions", "Carrots"
    ],
    "Dairy & Eggs": [
        "Milk", "Cheese", "Yogurt", "Butter", "Eggs"
    ],
    "Grains & Cereals": [
        "Rice", "Wheat Flour", "Bread", "Pasta", "Oats"
    ],
    "Protein": [
        "Chicken", "Fish", "Tofu", "Lentils", "Beans"
    ],
    "Pantry Items": [
        "Oil", "Sugar", "Salt", "Spices", "Tea", "Coffee"
    ]
}

def main():
    st.set_page_config(page_title="Grocery & Meal Planner", page_icon="🛒", layout="wide")
    
    st.title("🛒 Grocery Expense & Meal Planner")
    st.write("Plan your meals and track grocery expenses")
    
    # Initialize session state
    if 'grocery_data' not in st.session_state:
        st.session_state.grocery_data = load_grocery_data()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Meal Planning", "Shopping List", "Expense Tracking", "Analysis"])
    
    # Meal Planning Tab
    with tab1:
        st.markdown("### 📋 Weekly Meal Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Add new meal
            meal_date = st.date_input("Date")
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner"])
            meal_name = st.text_input("Meal Name")
            ingredients = st.multiselect(
                "Ingredients",
                [item for items in GROCERY_CATEGORIES.values() for item in items]
            )
            servings = st.number_input("Servings", min_value=1, value=2)
            
            if st.button("Add Meal"):
                meal = {
                    "date": meal_date.strftime("%Y-%m-%d"),
                    "type": meal_type,
                    "name": meal_name,
                    "ingredients": ingredients,
                    "servings": servings
                }
                st.session_state.grocery_data["meals"].append(meal)
                save_grocery_data(st.session_state.grocery_data)
                st.success("Meal added to plan!")
        
        with col2:
            if st.session_state.grocery_data["meals"]:
                # Display meal plan
                df_meals = pd.DataFrame(st.session_state.grocery_data["meals"])
                df_meals['date'] = pd.to_datetime(df_meals['date'])
                df_meals = df_meals.sort_values(['date', 'type'])
                
                for date in df_meals['date'].unique():
                    st.markdown(f"#### {date.strftime('%A, %B %d')}")
                    day_meals = df_meals[df_meals['date'] == date]
                    for _, meal in day_meals.iterrows():
                        st.markdown(f"**{meal['type']}**: {meal['name']} ({meal['servings']} servings)")
                        st.write(", ".join(meal['ingredients']))
                        st.markdown("---")
    
    # Shopping List Tab
    with tab2:
        st.markdown("### 🛍️ Shopping List Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate shopping list from meal plan
            start_date = st.date_input("Start Date")
            days = st.number_input("Number of Days", min_value=1, max_value=14, value=7)
            
            if st.button("Generate Shopping List"):
                end_date = start_date + timedelta(days=days)
                
                # Get meals within date range
                df_meals = pd.DataFrame(st.session_state.grocery_data["meals"])
                if not df_meals.empty:
                    df_meals['date'] = pd.to_datetime(df_meals['date'])
                    mask = (df_meals['date'] >= pd.Timestamp(start_date)) & \
                           (df_meals['date'] <= pd.Timestamp(end_date))
                    selected_meals = df_meals[mask]
                    
                    # Compile ingredients
                    ingredients_list = []
                    for _, meal in selected_meals.iterrows():
                        ingredients_list.extend(meal['ingredients'])
                    
                    # Count ingredients
                    ingredients_count = pd.Series(ingredients_list).value_counts()
                    
                    # Create shopping list
                    shopping_list = {
                        "date_created": datetime.now().strftime("%Y-%m-%d"),
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d"),
                        "items": [{"item": item, "quantity": count} 
                                for item, count in ingredients_count.items()]
                    }
                    
                    st.session_state.grocery_data["shopping_lists"].append(shopping_list)
                    save_grocery_data(st.session_state.grocery_data)
                    
                    with col2:
                        st.markdown("### 📝 Shopping List")
                        for category, items in GROCERY_CATEGORIES.items():
                            category_items = [item for item in shopping_list["items"] 
                                           if item["item"] in items]
                            if category_items:
                                st.markdown(f"#### {category}")
                                for item in category_items:
                                    st.write(f"- {item['item']} (x{item['quantity']})")
    
    # Expense Tracking Tab
    with tab3:
        st.markdown("### 💰 Grocery Expense Tracker")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Add new item
            category = st.selectbox("Category", list(GROCERY_CATEGORIES.keys()))
            item = st.selectbox("Item", GROCERY_CATEGORIES[category])
            quantity = st.number_input("Quantity", min_value=1, value=1)
            price = st.number_input("Price (₹)", min_value=0.0, value=0.0)
            purchase_date = st.date_input("Purchase Date")
            
            if st.button("Add Item"):
                item_data = {
                    "category": category,
                    "item": item,
                    "quantity": quantity,
                    "price": price,
                    "date": purchase_date.strftime("%Y-%m-%d")
                }
                st.session_state.grocery_data["items"].append(item_data)
                save_grocery_data(st.session_state.grocery_data)
                st.success("Item added to expenses!")
        
        with col2:
            if st.session_state.grocery_data["items"]:
                df_items = pd.DataFrame(st.session_state.grocery_data["items"])
                df_items['date'] = pd.to_datetime(df_items['date'])
                
                # Display recent expenses
                st.markdown("### Recent Expenses")
                recent_items = df_items.sort_values('date', ascending=False).head(10)
                st.dataframe(
                    recent_items[['date', 'item', 'quantity', 'price']]
                    .style.format({
                        'date': lambda x: x.strftime('%Y-%m-%d'),
                        'price': '₹{:.2f}'
                    })
                )
    
    # Analysis Tab
    with tab4:
        if st.session_state.grocery_data["items"]:
            df_items = pd.DataFrame(st.session_state.grocery_data["items"])
            df_items['date'] = pd.to_datetime(df_items['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Spending by category
                category_spending = df_items.groupby('category')['price'].sum()
                
                fig1 = go.Figure(data=[go.Pie(
                    labels=category_spending.index,
                    values=category_spending.values,
                    hole=.3
                )])
                fig1.update_layout(title="Spending by Category")
                st.plotly_chart(fig1)
                
                # Monthly spending trend
                monthly_spending = df_items.set_index('date')\
                    .resample('M')['price'].sum().reset_index()
                
                fig2 = px.line(monthly_spending, x='date', y='price',
                              title='Monthly Spending Trend')
                st.plotly_chart(fig2)
            
            with col2:
                # Spending insights
                st.markdown("### 💡 Spending Insights")
                
                total_spent = df_items['price'].sum()
                avg_monthly = monthly_spending['price'].mean()
                
                st.info(f"Total Spent: ₹{total_spent:,.2f}")
                st.success(f"Average Monthly Spending: ₹{avg_monthly:,.2f}")
                
                # Most expensive items
                top_items = df_items.groupby('item')['price'].sum()\
                    .sort_values(ascending=False).head(5)
                
                st.markdown("#### Most Expensive Items")
                for item, price in top_items.items():
                    st.write(f"- {item}: ₹{price:,.2f}")
                
                # Budget recommendations
                st.markdown("### 🎯 Budget Recommendations")
                recommended_budget = avg_monthly * 1.1  # 10% buffer
                
                st.warning(f"Recommended Monthly Budget: ₹{recommended_budget:,.2f}")
                
                # Saving opportunities
                st.markdown("#### 💰 Saving Opportunities")
                tips = [
                    "- Buy seasonal fruits and vegetables",
                    "- Purchase non-perishables in bulk",
                    "- Compare prices across stores",
                    "- Plan meals to minimize waste",
                    "- Use loyalty programs and discounts"
                ]
                st.write("\n".join(tips))
        else:
            st.write("Add some grocery expenses to see the analysis!")

if __name__ == "__main__":
    main()
