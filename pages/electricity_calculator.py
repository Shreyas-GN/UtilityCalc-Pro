import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime

def load_appliance_data():
    if os.path.exists('appliance_usage.json'):
        with open('appliance_usage.json', 'r') as f:
            return json.load(f)
    return []

def save_appliance_data(data):
    with open('appliance_usage.json', 'w') as f:
        json.dump(data, f)

# Common household appliances and their typical power consumption
COMMON_APPLIANCES = {
    "Air Conditioner": 1500,
    "Refrigerator": 150,
    "Washing Machine": 500,
    "Television": 100,
    "Microwave": 1000,
    "Electric Fan": 75,
    "LED Light Bulb": 10,
    "Desktop Computer": 200,
    "Laptop": 60,
    "Water Heater": 2000,
    "Iron": 1000,
    "Dishwasher": 1500,
    "Electric Kettle": 1500,
    "Ceiling Fan": 75,
    "Router/Modem": 10
}

def calculate_daily_consumption(appliances):
    total_kwh = 0
    for appliance in appliances:
        hours = appliance['hours']
        watts = appliance['watts']
        quantity = appliance['quantity']
        total_kwh += (watts * hours * quantity) / 1000
    return total_kwh

def calculate_bill(total_kwh, rate):
    return total_kwh * rate

def main():
    st.set_page_config(page_title="Electricity Bill Calculator", page_icon="⚡", layout="wide")
    
    st.title("⚡ Electricity Bill Estimator")
    st.write("Calculate your electricity consumption and estimated bill")
    
    # Initialize session state
    if 'appliances' not in st.session_state:
        st.session_state.appliances = load_appliance_data()
    
    tab1, tab2, tab3 = st.tabs(["Add Appliances", "View Usage", "Analysis"])
    
    # Add Appliances Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Add new appliance
            st.markdown("### 🔌 Add Appliance")
            
            # Option to select from common appliances or custom
            appliance_type = st.radio("Appliance Selection", ["Common Appliance", "Custom Appliance"])
            
            if appliance_type == "Common Appliance":
                name = st.selectbox("Select Appliance", list(COMMON_APPLIANCES.keys()))
                watts = st.number_input("Power Rating (Watts)", 
                                      value=COMMON_APPLIANCES[name],
                                      min_value=1)
            else:
                name = st.text_input("Appliance Name")
                watts = st.number_input("Power Rating (Watts)", min_value=1, value=100)
            
            quantity = st.number_input("Quantity", min_value=1, value=1)
            hours = st.number_input("Daily Usage (Hours)", min_value=0.1, max_value=24.0, value=1.0)
            
            if st.button("Add Appliance"):
                appliance = {
                    "name": name,
                    "watts": watts,
                    "quantity": quantity,
                    "hours": hours,
                    "daily_kwh": (watts * hours * quantity) / 1000,
                    "date_added": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.appliances.append(appliance)
                save_appliance_data(st.session_state.appliances)
                st.success(f"Added {name} to appliances!")
        
        with col2:
            if st.session_state.appliances:
                st.markdown("### 📊 Current Appliances")
                df = pd.DataFrame(st.session_state.appliances)
                st.dataframe(
                    df[['name', 'watts', 'quantity', 'hours', 'daily_kwh']]
                    .style.format({
                        'watts': '{:,.0f}',
                        'daily_kwh': '{:.2f}'
                    })
                )
    
    # View Usage Tab
    with tab2:
        if st.session_state.appliances:
            st.markdown("### 📈 Electricity Usage Summary")
            
            # Rate input
            rate = st.number_input("Electricity Rate (₹/kWh)", min_value=0.1, value=8.0)
            
            # Calculate total consumption
            daily_consumption = calculate_daily_consumption(st.session_state.appliances)
            monthly_consumption = daily_consumption * 30
            monthly_bill = calculate_bill(monthly_consumption, rate)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"Daily Consumption: {daily_consumption:.2f} kWh")
                st.warning(f"Monthly Consumption: {monthly_consumption:.2f} kWh")
                st.error(f"Estimated Monthly Bill: ₹{monthly_bill:.2f}")
                
                # Create consumption breakdown
                df = pd.DataFrame(st.session_state.appliances)
                fig = go.Figure(data=[go.Pie(
                    labels=df['name'],
                    values=df['daily_kwh'],
                    hole=.3
                )])
                fig.update_layout(title="Power Consumption Distribution")
                st.plotly_chart(fig)
            
            with col2:
                # Create hourly usage pattern
                st.markdown("### ⏰ Hourly Usage Pattern")
                hours = list(range(24))
                usage_pattern = [0] * 24
                
                # Simulate usage pattern (simplified)
                for appliance in st.session_state.appliances:
                    if appliance['name'] in ['Air Conditioner', 'Light Bulb']:
                        # Evening and night usage
                        for h in range(18, 24):
                            usage_pattern[h] += appliance['daily_kwh'] / appliance['hours']
                    elif appliance['name'] in ['Refrigerator']:
                        # Constant usage
                        for h in range(24):
                            usage_pattern[h] += appliance['daily_kwh'] / 24
                    else:
                        # Daytime usage
                        for h in range(8, 20):
                            usage_pattern[h] += appliance['daily_kwh'] / appliance['hours']
                
                fig2 = go.Figure(data=[go.Bar(
                    x=[f"{h:02d}:00" for h in hours],
                    y=usage_pattern
                )])
                fig2.update_layout(
                    title="Estimated Hourly Power Usage",
                    xaxis_title="Time",
                    yaxis_title="kWh"
                )
                st.plotly_chart(fig2)
    
    # Analysis Tab
    with tab3:
        if st.session_state.appliances:
            st.markdown("### 💡 Energy Saving Recommendations")
            
            df = pd.DataFrame(st.session_state.appliances)
            high_consumption = df.nlargest(3, 'daily_kwh')
            
            st.warning("Top Energy Consuming Appliances:")
            for _, appliance in high_consumption.iterrows():
                st.write(f"- {appliance['name']}: {appliance['daily_kwh']:.2f} kWh/day")
            
            # Generate recommendations
            recommendations = []
            
            for appliance in st.session_state.appliances:
                if appliance['name'] == "Air Conditioner" and appliance['hours'] > 8:
                    recommendations.append("- Consider using AC for fewer hours or at a higher temperature")
                elif appliance['name'] == "Light Bulb" and appliance['watts'] > 10:
                    recommendations.append("- Replace high-wattage bulbs with LED alternatives")
                elif appliance['hours'] > 12:
                    recommendations.append(f"- Reduce usage hours of {appliance['name']}")
            
            if recommendations:
                st.markdown("### 🌱 Energy Saving Tips")
                st.write("\n".join(recommendations))
            
            # Calculate potential savings
            st.markdown("### 💰 Potential Savings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Scenario 1: LED replacement
                led_savings = 0
                for appliance in st.session_state.appliances:
                    if appliance['name'] == "Light Bulb" and appliance['watts'] > 10:
                        led_savings += (appliance['watts'] - 10) * appliance['hours'] * appliance['quantity'] * 30 / 1000
                
                if led_savings > 0:
                    st.info(f"LED Replacement Savings: ₹{led_savings * rate:.2f}/month")
            
            with col2:
                # Scenario 2: Optimal AC usage
                ac_savings = 0
                for appliance in st.session_state.appliances:
                    if appliance['name'] == "Air Conditioner" and appliance['hours'] > 8:
                        ac_savings += (appliance['hours'] - 8) * appliance['watts'] * appliance['quantity'] * 30 / 1000
                
                if ac_savings > 0:
                    st.info(f"Optimal AC Usage Savings: ₹{ac_savings * rate:.2f}/month")
            
            # Historical trend
            if len(df) > 1:
                st.markdown("### 📈 Consumption Trend")
                df['date_added'] = pd.to_datetime(df['date_added'])
                daily_trend = df.groupby('date_added')['daily_kwh'].sum().reset_index()
                
                fig3 = px.line(daily_trend, x='date_added', y='daily_kwh',
                              title='Daily Consumption Trend')
                st.plotly_chart(fig3)
        else:
            st.write("Add some appliances to see the analysis!")

if __name__ == "__main__":
    main()
