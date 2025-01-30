import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="Investment Growth Calculator", page_icon="📈", layout="wide")
    
    st.title("📈 Investment Growth Calculator")
    st.write("Calculate your investment growth with compound interest")
    
    col1, col2 = st.columns(2)
    
    with col1:
        initial_investment = st.number_input("Initial Investment Amount (₹)", min_value=0, value=10000)
        monthly_contribution = st.number_input("Monthly Contribution (₹)", min_value=0, value=1000)
        annual_return = st.number_input("Expected Annual Return (%)", min_value=0.0, max_value=30.0, value=8.0)
        investment_period = st.number_input("Investment Period (Years)", min_value=1, max_value=50, value=10)
        
    if st.button("Calculate Returns"):
        # Monthly rate
        monthly_rate = annual_return / (12 * 100)
        months = investment_period * 12
        
        # Calculate future value
        future_value = initial_investment * (1 + monthly_rate) ** months
        
        # Calculate future value with monthly contributions
        if monthly_contribution > 0:
            future_value += monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        
        total_invested = initial_investment + (monthly_contribution * months)
        total_returns = future_value - total_invested
        
        with col2:
            st.markdown("### 📊 Investment Summary")
            st.info(f"Future Value: ₹{future_value:,.2f}")
            st.success(f"Total Returns: ₹{total_returns:,.2f}")
            st.warning(f"Total Invested: ₹{total_invested:,.2f}")
            
            # Create growth visualization
            years = list(range(investment_period + 1))
            values = []
            for year in years:
                months = year * 12
                value = initial_investment * (1 + monthly_rate) ** months
                if monthly_contribution > 0:
                    value += monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
                values.append(value)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=values,
                                   name='Investment Growth',
                                   fill='tozeroy'))
            fig.update_layout(title='Investment Growth Over Time',
                            xaxis_title='Years',
                            yaxis_title='Value (₹)')
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
