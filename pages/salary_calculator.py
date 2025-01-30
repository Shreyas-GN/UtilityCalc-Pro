import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def calculate_tax_old_regime(taxable_income):
    tax = 0
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 750000:
        tax = 12500 + (taxable_income - 500000) * 0.10
    elif taxable_income <= 1000000:
        tax = 37500 + (taxable_income - 750000) * 0.15
    elif taxable_income <= 1250000:
        tax = 75000 + (taxable_income - 1000000) * 0.20
    elif taxable_income <= 1500000:
        tax = 125000 + (taxable_income - 1250000) * 0.25
    else:
        tax = 187500 + (taxable_income - 1500000) * 0.30
    return tax

def calculate_tax_new_regime(taxable_income):
    tax = 0
    if taxable_income <= 300000:
        tax = 0
    elif taxable_income <= 600000:
        tax = (taxable_income - 300000) * 0.05
    elif taxable_income <= 900000:
        tax = 15000 + (taxable_income - 600000) * 0.10
    elif taxable_income <= 1200000:
        tax = 45000 + (taxable_income - 900000) * 0.15
    elif taxable_income <= 1500000:
        tax = 90000 + (taxable_income - 1200000) * 0.20
    else:
        tax = 150000 + (taxable_income - 1500000) * 0.30
    return tax

def main():
    st.set_page_config(page_title="Salary Calculator", page_icon="💰", layout="wide")
    
    st.title("💰 Salary Tax & Take-Home Pay Calculator")
    st.write("Calculate your take-home salary after tax deductions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        annual_salary = st.number_input("Annual Salary (₹)", min_value=0, value=500000)
        regime = st.radio("Tax Regime", ["New Regime", "Old Regime"])
        
        # Deductions (only for old regime)
        if regime == "Old Regime":
            st.markdown("### 📋 Deductions under Section 80C")
            epf = st.number_input("EPF Contribution (₹)", min_value=0, value=0)
            insurance = st.number_input("Life Insurance Premium (₹)", min_value=0, value=0)
            elss = st.number_input("ELSS Investment (₹)", min_value=0, value=0)
            
            st.markdown("### 🏥 Other Deductions")
            medical_insurance = st.number_input("Medical Insurance Premium (80D) (₹)", min_value=0, value=0)
            home_loan_interest = st.number_input("Home Loan Interest (80EE) (₹)", min_value=0, value=0)
            
            total_deductions = min(epf + insurance + elss, 150000) + medical_insurance + home_loan_interest
        else:
            total_deductions = 0
        
    if st.button("Calculate Tax"):
        # Calculate taxable income
        taxable_income = annual_salary - total_deductions
        
        # Calculate tax based on regime
        if regime == "Old Regime":
            tax = calculate_tax_old_regime(taxable_income)
        else:
            tax = calculate_tax_new_regime(taxable_income)
        
        # Calculate cess
        cess = tax * 0.04
        total_tax = tax + cess
        
        # Calculate monthly take-home
        monthly_salary = (annual_salary - total_tax) / 12
        
        with col2:
            st.markdown("### 📊 Tax Calculation Summary")
            
            # Create summary table
            summary_data = {
                "Component": ["Gross Annual Salary", "Total Deductions", "Taxable Income", 
                            "Income Tax", "Health & Education Cess", "Total Tax", 
                            "Annual Take-Home", "Monthly Take-Home"],
                "Amount": [annual_salary, total_deductions, taxable_income,
                          tax, cess, total_tax,
                          annual_salary - total_tax, monthly_salary]
            }
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(
                summary_df.style.format({
                    "Amount": "₹{:,.2f}"
                })
            )
            
            # Create pie chart for tax breakdown
            fig = go.Figure(data=[go.Pie(
                labels=["Take-Home Pay", "Tax", "Cess"],
                values=[annual_salary - total_tax, tax, cess],
                hole=.3
            )])
            fig.update_layout(title="Salary Breakdown")
            st.plotly_chart(fig)
            
            # Display effective tax rate
            effective_tax_rate = (total_tax / annual_salary) * 100
            st.info(f"Effective Tax Rate: {effective_tax_rate:.2f}%")
            
            # Tax saving suggestions
            if regime == "Old Regime":
                st.markdown("### 💡 Tax Saving Suggestions")
                suggestions = []
                
                if epf + insurance + elss < 150000:
                    remaining_80c = 150000 - (epf + insurance + elss)
                    suggestions.append(f"- You can still invest ₹{remaining_80c:,.2f} under Section 80C")
                
                if medical_insurance == 0:
                    suggestions.append("- Consider getting medical insurance for tax benefits under Section 80D")
                
                if suggestions:
                    st.write("\n".join(suggestions))
                else:
                    st.success("You're making good use of available tax deductions!")
            else:
                st.markdown("### 💡 Note")
                st.write("The new tax regime offers lower tax rates but doesn't allow most deductions. "
                        "Compare both regimes to choose what's best for you.")

if __name__ == "__main__":
    main()
