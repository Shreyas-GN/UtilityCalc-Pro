import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="Calorie Calculator", page_icon="🍎", layout="wide")
    
    st.title("🍎 Daily Calorie & Macronutrient Calculator")
    st.write("Calculate your daily calorie needs and macronutrient distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
            value="Moderately Active"
        )
        goal = st.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Weight"])
        
    if st.button("Calculate Needs"):
        # Calculate BMR using Mifflin-St Jeor Equation
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
        # Activity multiplier
        activity_multipliers = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extra Active": 1.9
        }
        
        tdee = bmr * activity_multipliers[activity_level]
        
        # Adjust calories based on goal
        if goal == "Lose Weight":
            calories = tdee - 500
        elif goal == "Gain Weight":
            calories = tdee + 500
        else:
            calories = tdee
            
        # Calculate macronutrients
        protein = weight * 2.2  # 2.2g per kg
        fat = (calories * 0.25) / 9  # 25% of calories from fat
        carbs = (calories - (protein * 4) - (fat * 9)) / 4  # Remaining calories from carbs
        
        with col2:
            st.markdown("### 📊 Daily Needs")
            st.info(f"Daily Calories: {calories:.0f} kcal")
            
            # Create macronutrient breakdown
            macros = {
                "Protein": {"amount": protein, "calories": protein * 4},
                "Carbs": {"amount": carbs, "calories": carbs * 4},
                "Fat": {"amount": fat, "calories": fat * 9}
            }
            
            # Display macronutrient table
            st.markdown("### 🍖 Macronutrient Breakdown")
            macro_df = pd.DataFrame({
                "Nutrient": macros.keys(),
                "Amount (g)": [m["amount"] for m in macros.values()],
                "Calories": [m["calories"] for m in macros.values()]
            })
            st.dataframe(macro_df.round(1))
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(macros.keys()),
                values=[m["calories"] for m in macros.values()],
                hole=.3
            )])
            fig.update_layout(title="Calorie Distribution")
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
