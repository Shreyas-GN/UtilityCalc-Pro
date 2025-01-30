import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="Loan EMI Calculator", page_icon="💰", layout="wide")
    
    st.title("💰 Loan EMI Calculator")
    st.write("Calculate your loan EMI and view detailed payment schedule")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input("Loan Amount (₹)", min_value=1000, value=100000)
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, max_value=30.0, value=10.0)
        loan_term = st.number_input("Loan Term (Years)", min_value=1, max_value=30, value=5)

    if st.button("Calculate EMI"):
        # Monthly interest rate
        monthly_rate = interest_rate / (12 * 100)
        
        # Total number of months
        months = loan_term * 12
        
        # Calculate EMI
        emi = loan_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
        
        # Calculate total payment and interest
        total_payment = emi * months
        total_interest = total_payment - loan_amount
        
        with col2:
            st.markdown("### 📊 Loan Summary")
            st.info(f"Monthly EMI: ₹{emi:,.2f}")
            st.success(f"Total Interest: ₹{total_interest:,.2f}")
            st.warning(f"Total Payment: ₹{total_payment:,.2f}")
            
            # Create amortization schedule
            payment_data = []
            remaining_balance = loan_amount
            
            for month in range(1, months + 1):
                interest_payment = remaining_balance * monthly_rate
                principal_payment = emi - interest_payment
                remaining_balance -= principal_payment
                
                payment_data.append({
                    'Month': month,
                    'Principal': principal_payment,
                    'Interest': interest_payment,
                    'Balance': remaining_balance
                })
            
            # Create visualization
            df = pd.DataFrame(payment_data)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Month'], y=df['Balance'],
                                   name='Remaining Balance',
                                   fill='tozeroy'))
            fig.update_layout(title='Loan Amortization Schedule',
                            xaxis_title='Month',
                            yaxis_title='Remaining Balance (₹)')
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
