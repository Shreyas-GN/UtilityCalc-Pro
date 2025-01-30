import streamlit as st
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="wide")
    
    st.title("⚖️ BMI & Ideal Weight Calculator")
    st.write("Calculate your BMI and find your ideal weight range")
    
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
    if st.button("Calculate BMI"):
        # Calculate BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        # Calculate ideal weight range (using Hamwi formula)
        if gender == "Male":
            ideal_weight = 48 + 2.7 * (height - 152.4) / 2.54
        else:
            ideal_weight = 45.5 + 2.2 * (height - 152.4) / 2.54
            
        weight_range = (ideal_weight * 0.9, ideal_weight * 1.1)
        
        with col2:
            st.markdown("### 📊 BMI Results")
            st.info(f"Your BMI: {bmi:.1f}")
            
            # BMI Category
            if bmi < 18.5:
                category = "Underweight"
                color = "blue"
            elif bmi < 25:
                category = "Normal weight"
                color = "green"
            elif bmi < 30:
                category = "Overweight"
                color = "orange"
            else:
                category = "Obese"
                color = "red"
                
            st.markdown(f"<h3 style='color: {color};'>Category: {category}</h3>", unsafe_allow_html=True)
            st.success(f"Ideal Weight Range: {weight_range[0]:.1f} - {weight_range[1]:.1f} kg")
            
            # Create BMI visualization
            fig = go.Figure()
            
            # Add BMI categories
            categories = [
                {"name": "Underweight", "range": (0, 18.5), "color": "blue"},
                {"name": "Normal", "range": (18.5, 25), "color": "green"},
                {"name": "Overweight", "range": (25, 30), "color": "orange"},
                {"name": "Obese", "range": (30, 40), "color": "red"}
            ]
            
            for cat in categories:
                fig.add_shape(
                    type="rect",
                    x0=cat["range"][0],
                    x1=cat["range"][1],
                    y0=0,
                    y1=1,
                    fillcolor=cat["color"],
                    opacity=0.3,
                    line_width=0,
                    layer="below"
                )
            
            # Add marker for user's BMI
            fig.add_trace(go.Scatter(x=[bmi], y=[0.5],
                                   mode="markers",
                                   marker=dict(size=15, color="black"),
                                   name="Your BMI"))
            
            fig.update_layout(
                title="BMI Scale",
                xaxis_title="BMI",
                yaxis_visible=False,
                height=200,
                showlegend=False
            )
            
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
