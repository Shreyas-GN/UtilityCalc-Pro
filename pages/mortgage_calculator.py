import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def calculate_mortgage_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12
    
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    
    return monthly_payment

def calculate_affordability(monthly_income, other_debts=0, down_payment=0, annual_rate=8.0, years=20):
    # Using the 28/36 rule
    max_mortgage_payment = monthly_income * 0.28
    max_total_debt_payment = monthly_income * 0.36 - other_debts
    
    # Use the lower of the two values
    max_payment = min(max_mortgage_payment, max_total_debt_payment)
    
    # Calculate maximum affordable loan
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12
    
    if monthly_rate == 0:
        max_loan = max_payment * months
    else:
        max_loan = max_payment * ((1 - (1 + monthly_rate)**(-months)) / monthly_rate)
    
    max_home_price = max_loan + down_payment
    
    return max_home_price, max_loan, max_payment

def main():
    st.set_page_config(page_title="Mortgage Calculator", page_icon="🏠", layout="wide")
    
    st.title("🏠 Home Mortgage & Rent Affordability Calculator")
    st.write("Calculate your home affordability and mortgage payments")
    
    tab1, tab2 = st.tabs(["Mortgage Calculator", "Rent vs Buy Analysis"])
    
    # Mortgage Calculator Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Income & Expenses")
            monthly_income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            other_debts = st.number_input("Monthly Debt Payments (₹)", min_value=0, value=0)
            credit_score = st.slider("Credit Score", 300, 900, 750)
            
            st.markdown("### 🏦 Loan Details")
            down_payment = st.number_input("Down Payment (₹)", min_value=0, value=500000)
            annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=8.0)
            years = st.number_input("Loan Term (Years)", min_value=5, max_value=30, value=20)
            
            if st.button("Calculate Affordability"):
                max_price, max_loan, max_payment = calculate_affordability(
                    monthly_income, other_debts, down_payment, annual_rate, years
                )
                
                with col2:
                    st.markdown("### 📊 Affordability Analysis")
                    st.info(f"Maximum Home Price: ₹{max_price:,.2f}")
                    st.success(f"Maximum Loan Amount: ₹{max_loan:,.2f}")
                    st.warning(f"Maximum Monthly Payment: ₹{max_payment:,.2f}")
                    
                    # Create payment breakdown
                    monthly_payment = calculate_mortgage_payment(max_loan, annual_rate, years)
                    total_payment = monthly_payment * years * 12
                    total_interest = total_payment - max_loan
                    
                    # Payment distribution chart
                    fig = go.Figure(data=[go.Pie(
                        labels=["Principal", "Interest"],
                        values=[max_loan, total_interest],
                        hole=.3
                    )])
                    fig.update_layout(title="Payment Distribution")
                    st.plotly_chart(fig)
                    
                    # Amortization schedule
                    st.markdown("### 📅 Amortization Schedule")
                    balance = max_loan
                    monthly_rate = annual_rate / (12 * 100)
                    schedule_data = []
                    
                    for year in range(1, years + 1):
                        yearly_principal = 0
                        yearly_interest = 0
                        
                        for month in range(12):
                            interest_payment = balance * monthly_rate
                            principal_payment = monthly_payment - interest_payment
                            balance -= principal_payment
                            
                            yearly_principal += principal_payment
                            yearly_interest += interest_payment
                        
                        schedule_data.append({
                            'Year': year,
                            'Principal': yearly_principal,
                            'Interest': yearly_interest,
                            'Remaining Balance': balance
                        })
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    st.dataframe(
                        schedule_df.style.format({
                            'Principal': '₹{:,.2f}',
                            'Interest': '₹{:,.2f}',
                            'Remaining Balance': '₹{:,.2f}'
                        })
                    )
    
    # Rent vs Buy Analysis Tab
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏠 Property Details")
            home_price = st.number_input("Home Price (₹)", min_value=0, value=5000000)
            monthly_rent = st.number_input("Comparable Monthly Rent (₹)", min_value=0, value=20000)
            
            st.markdown("### 📈 Assumptions")
            home_appreciation = st.slider("Annual Home Appreciation (%)", 0, 10, 5)
            rent_increase = st.slider("Annual Rent Increase (%)", 0, 10, 7)
            property_tax_rate = st.slider("Property Tax Rate (%)", 0.0, 5.0, 1.0)
            maintenance_percent = st.slider("Annual Maintenance (% of home value)", 0.0, 2.0, 1.0)
            
            analysis_years = st.slider("Analysis Period (Years)", 5, 30, 10)
            
            if st.button("Compare Rent vs Buy"):
                # Calculate buying costs
                monthly_payment = calculate_mortgage_payment(
                    home_price - down_payment, annual_rate, years
                )
                
                buy_costs = []
                rent_costs = []
                home_values = []
                
                current_home_value = home_price
                current_rent = monthly_rent
                
                for year in range(1, analysis_years + 1):
                    # Buying costs
                    yearly_mortgage = monthly_payment * 12
                    property_tax = current_home_value * property_tax_rate / 100
                    maintenance = current_home_value * maintenance_percent / 100
                    
                    total_buy_cost = yearly_mortgage + property_tax + maintenance
                    buy_costs.append(total_buy_cost)
                    
                    # Home appreciation
                    current_home_value *= (1 + home_appreciation / 100)
                    home_values.append(current_home_value)
                    
                    # Renting costs
                    yearly_rent = current_rent * 12
                    rent_costs.append(yearly_rent)
                    current_rent *= (1 + rent_increase / 100)
                
                with col2:
                    st.markdown("### 📊 Cost Comparison")
                    
                    # Create comparison chart
                    years = list(range(1, analysis_years + 1))
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=years,
                        y=buy_costs,
                        name="Buying Costs",
                        line=dict(color="blue")
                    ))
                    fig.add_trace(go.Scatter(
                        x=years,
                        y=rent_costs,
                        name="Renting Costs",
                        line=dict(color="red")
                    ))
                    
                    fig.update_layout(
                        title="Yearly Cost Comparison",
                        xaxis_title="Year",
                        yaxis_title="Annual Cost (₹)"
                    )
                    st.plotly_chart(fig)
                    
                    # Calculate total costs
                    total_buy_cost = sum(buy_costs)
                    total_rent_cost = sum(rent_costs)
                    final_home_value = home_values[-1]
                    
                    st.info(f"Total Buying Costs: ₹{total_buy_cost:,.2f}")
                    st.warning(f"Total Renting Costs: ₹{total_rent_cost:,.2f}")
                    st.success(f"Estimated Home Value after {analysis_years} years: ₹{final_home_value:,.2f}")
                    
                    # Break-even analysis
                    cumulative_buy = np.cumsum(buy_costs)
                    cumulative_rent = np.cumsum(rent_costs)
                    break_even_year = np.where(cumulative_rent > cumulative_buy)[0]
                    
                    if len(break_even_year) > 0:
                        st.success(f"Break-even Point: Year {break_even_year[0] + 1}")
                    else:
                        st.error("No break-even point within the analysis period")
                    
                    # Recommendation
                    if total_rent_cost > total_buy_cost:
                        st.markdown("### 💡 Recommendation")
                        st.write("Based on your inputs, buying appears to be more financially advantageous "
                                "in the long term. However, consider other factors such as flexibility, "
                                "maintenance responsibilities, and your long-term plans.")
                    else:
                        st.markdown("### 💡 Recommendation")
                        st.write("Based on your inputs, renting appears to be more cost-effective. "
                                "Consider your long-term plans and the non-financial benefits of "
                                "homeownership before making a decision.")

if __name__ == "__main__":
    main()
