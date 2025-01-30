import streamlit as st
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="Hydration Calculator", page_icon="💧", layout="wide")
    
    st.title("💧 Hydration & Water Intake Calculator")
    st.write("Calculate your daily water needs based on your lifestyle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Light Exercise", "Moderate Exercise", "Heavy Exercise", "Athlete"],
            value="Light Exercise"
        )
        climate = st.select_slider(
            "Climate",
            options=["Cold", "Moderate", "Hot", "Very Hot"],
            value="Moderate"
        )
        
        # Additional factors
        pregnant = st.checkbox("Pregnant or Breastfeeding")
        altitude = st.checkbox("Living at High Altitude")
        caffeine = st.number_input("Daily Caffeine Intake (cups)", min_value=0, max_value=10, value=2)
        
    if st.button("Calculate Hydration Needs"):
        # Base calculation (ml per kg)
        base_water = weight * 30  # 30ml per kg body weight
        
        # Activity level adjustments
        activity_multipliers = {
            "Sedentary": 1.0,
            "Light Exercise": 1.2,
            "Moderate Exercise": 1.4,
            "Heavy Exercise": 1.6,
            "Athlete": 1.8
        }
        
        # Climate adjustments
        climate_multipliers = {
            "Cold": 0.9,
            "Moderate": 1.0,
            "Hot": 1.2,
            "Very Hot": 1.4
        }
        
        # Calculate total water needs
        water_needs = base_water * activity_multipliers[activity_level] * climate_multipliers[climate]
        
        # Additional adjustments
        if pregnant:
            water_needs += 300  # Additional 300ml for pregnant/breastfeeding
        if altitude:
            water_needs *= 1.15  # 15% increase for high altitude
        if caffeine > 0:
            water_needs += caffeine * 200  # Additional water for caffeine intake
            
        # Convert to liters
        water_needs_l = water_needs / 1000
        
        with col2:
            st.markdown("### 📊 Daily Water Needs")
            st.info(f"Recommended Daily Intake: {water_needs_l:.1f} liters")
            
            # Create hourly breakdown
            waking_hours = 16  # Assume 16 waking hours
            hourly_intake = water_needs / waking_hours
            
            # Create schedule visualization
            hours = list(range(6, 22))  # 6 AM to 10 PM
            recommended_intake = [hourly_intake] * len(hours)
            
            # Adjust for optimal distribution
            # More in the morning and less in the evening
            for i in range(len(recommended_intake)):
                if i < 4:  # Morning hours
                    recommended_intake[i] *= 1.2
                elif i > len(recommended_intake) - 4:  # Evening hours
                    recommended_intake[i] *= 0.8
                    
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[f"{hour}:00" for hour in hours],
                y=recommended_intake,
                name="Recommended Intake (ml)"
            ))
            
            fig.update_layout(
                title="Recommended Hourly Water Intake",
                xaxis_title="Time",
                yaxis_title="Water (ml)"
            )
            st.plotly_chart(fig)
            
            # Tips
            st.markdown("### 💡 Hydration Tips")
            tips = [
                "- Start your day with a glass of water",
                "- Keep a water bottle with you throughout the day",
                "- Set reminders to drink water every hour",
                "- Drink water before, during, and after exercise",
                f"- Aim to drink {(water_needs_l/8):.1f} glasses (250ml) every 2 hours while awake"
            ]
            
            if climate in ["Hot", "Very Hot"]:
                tips.append("- Increase intake during hot weather")
            if activity_level in ["Heavy Exercise", "Athlete"]:
                tips.append("- Consider electrolyte replacement during intense exercise")
            if caffeine > 3:
                tips.append("- Consider reducing caffeine intake or increasing water to compensate")
                
            st.write("\n".join(tips))
            
            # Progress tracker
            st.markdown("### 📝 Daily Tracking")
            glasses_drunk = st.slider("Glasses of water (250ml) consumed today", 0, int(water_needs_l * 4))
            progress = (glasses_drunk * 250) / water_needs
            
            st.progress(min(progress, 1.0))
            if progress < 0.5:
                st.warning(f"You need to drink {water_needs_l - (glasses_drunk * 0.25):.1f} more liters today")
            elif progress < 1:
                st.info(f"Almost there! {water_needs_l - (glasses_drunk * 0.25):.1f} more liters to go")
            else:
                st.success("You've met your hydration goal for today!")

if __name__ == "__main__":
    main()
