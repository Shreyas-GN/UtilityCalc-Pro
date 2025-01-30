import streamlit as st
from datetime import datetime
import os

def create_tile(title, description, app_file):
    # Create a unique key for each button
    button_key = f"launch_{app_file.replace('.py', '')}"
    
    st.markdown(f"""
    <div style='
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    '>
        <div>
            <h3 style='
                margin-top: 0;
                color: #1f75fe;
                font-size: 1.2rem;
                margin-bottom: 1rem;
            '>{title}</h3>
            <p style='
                color: #666;
                font-size: 0.9rem;
                line-height: 1.6;
                margin-bottom: 1rem;
            '>{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a button with custom styling
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-top: -0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🚀 Launch", key=button_key, type="primary", use_container_width=True):
            calculator_path = os.path.join("calculators", app_file)
            if os.path.exists(calculator_path):
                try:
                    # Use Streamlit's native page navigation
                    st.switch_page(calculator_path)
                except Exception as e:
                    st.error(f"Error launching {title}: {str(e)}")
            else:
                st.error(f"Calculator not found: {calculator_path}")

def create_header():
    st.markdown("""
    <div style='
        background-color: #1f75fe;
        padding: 2rem 0;
        margin: -6rem -4rem 2rem -4rem;
        text-align: center;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    '>
        <h1 style='
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        '>UtilityCalc Pro</h1>
        <p style='
            font-size: 1.1rem;
            opacity: 0.9;
            margin: 0;
        '>Your All-in-One Calculator Suite</p>
    </div>
    """, unsafe_allow_html=True)

def create_navigation():
    st.markdown("""
    <div style='
        background-color: white;
        padding: 1rem 0;
        margin: 0 -4rem;
        text-align: center;
        border-bottom: 1px solid #eee;
        position: sticky;
        top: 0;
        z-index: 999;
    '>
        <nav style='
            display: flex;
            justify-content: center;
            gap: 2rem;
        '>
            <a href="#home" style='color: #1f75fe; text-decoration: none; font-weight: 500;'>Home</a>
            <a href="#about" style='color: #1f75fe; text-decoration: none; font-weight: 500;'>About</a>
            <a href="#features" style='color: #1f75fe; text-decoration: none; font-weight: 500;'>Features</a>
            <a href="#contact" style='color: #1f75fe; text-decoration: none; font-weight: 500;'>Contact</a>
        </nav>
    </div>
    """, unsafe_allow_html=True)

def show_about_section():
    st.markdown("""
    ## About UtilityCalc Pro
    
    UtilityCalc Pro is a comprehensive suite of calculators and predictive tools designed to simplify your daily calculations and decision-making process. Our platform combines accuracy with user-friendly interfaces to provide you with reliable results instantly.
    
    ### Why Choose UtilityCalc Pro?
    - 🎯 **Accuracy**: Precise calculations using industry-standard formulas
    - 🚀 **Speed**: Instant results with real-time updates
    - 🎨 **User-Friendly**: Clean and intuitive interface
    - 📱 **Accessibility**: Works on all devices
    - 🔒 **Privacy**: Your data stays on your device
    """)

def show_features_section():
    st.markdown("""
    ## Features
    
    ✨ **Current Features**
    - User-friendly interface with intuitive navigation
    - Multiple calculator categories (Finance, Health, Home, Productivity)
    - Real-time calculations and instant results
    - Data visualization with charts and graphs
    - Responsive design for all devices
    
    🔮 **Coming Soon**
    - PDF report generation and sharing
    - Cloud sync for saved calculations
    - AI-powered predictions
    - Mobile app version
    - Custom calculator builder
    """)

def show_contact_section():
    st.markdown("""
    ## Contact Us
    
    Have questions or suggestions? We'd love to hear from you!
    
    📧 **Email**: shreyasgn@icloud.com
    🌐 **Website**: https://shreyas-gn.github.io/
    📨 **LinkedIn**: https://linkedin.com/in/shreyas-gn
    """)

def create_footer():
    current_year = datetime.now().year
    st.markdown(f"""
    <div style='
        margin-top: 4rem;
        padding: 2rem 0;
        text-align: center;
        border-top: 1px solid #eee;
        color: #666;
    '>
        <p>Made with ❤️ by Shreyas GN</p>
        <p> {current_year} UtilityCalc Pro. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="UtilityCalc Pro",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #1f75fe !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            border-radius: 0.25rem !important;
            cursor: pointer !important;
            transition: all 0.3s !important;
            width: 100% !important;
            margin-top: 0.5rem !important;
        }
        .stButton > button:hover {
            background-color: #0056b3 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        .block-container {
            padding-top: 6rem !important;
        }
        h1 {
            margin-bottom: 2rem;
        }
        h2 {
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #eee;
            color: #1f75fe;
        }
        div[data-testid="stToolbar"] {
            display: none;
        }
        footer {
            display: none;
        }
        div[data-testid="stDecoration"] {
            display: none;
        }
        a {
            color: #1f75fe !important;
            text-decoration: none !important;
        }
        a:hover {
            text-decoration: underline !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create header and navigation
    create_header()
    create_navigation()

    # Home section with calculators
    st.markdown('<div id="home"></div>', unsafe_allow_html=True)
    
    # Define calculators with their descriptions
    calculators = {
        "Finance": [
            {
                "title": "Loan EMI Calculator",
                "description": "Calculate monthly EMI payments, total interest cost, and view complete amortization schedule for any loan amount and tenure",
                "file": "loan_emi_calculator.py"
            },
            {
                "title": "Investment Growth Calculator",
                "description": "Plan your investments with compound interest calculations, SIP returns, and goal-based investment planning",
                "file": "investment_calculator.py"
            },
            {
                "title": "Mortgage Calculator",
                "description": "Make informed home-buying decisions with mortgage payments, affordability analysis, and rent vs. buy comparison",
                "file": "mortgage_calculator.py"
            },
            {
                "title": "Expense Tracker",
                "description": "Track daily expenses, set budgets, analyze spending patterns, and get insights on your financial habits",
                "file": "expense_tracker.py"
            },
            {
                "title": "Salary Calculator",
                "description": "Calculate your take-home salary after taxes and deductions, plan your finances better",
                "file": "salary_calculator.py"
            }
        ],
        "Health & Wellness": [
            {
                "title": "BMI Calculator",
                "description": "Calculate your Body Mass Index (BMI), get personalized health insights and weight management recommendations",
                "file": "bmi_calculator.py"
            },
            {
                "title": "Calorie Calculator",
                "description": "Get personalized daily calorie needs based on your age, weight, height, activity level, and fitness goals",
                "file": "calorie_calculator.py"
            },
            {
                "title": "Hydration Calculator",
                "description": "Track your daily water intake, get hydration reminders, and personalized recommendations based on your lifestyle",
                "file": "hydration_calculator.py"
            },
            {
                "title": "Sleep Calculator",
                "description": "Optimize your sleep schedule, track sleep patterns, and get recommendations for better sleep quality",
                "file": "sleep_calculator.py"
            }
        ],
        "Home & Utilities": [
            {
                "title": "Electricity Bill Calculator",
                "description": "Calculate electricity costs, track appliance-wise consumption, and get energy-saving recommendations",
                "file": "electricity_calculator.py"
            },
            {
                "title": "Grocery Planner",
                "description": "Plan your meals, generate shopping lists, track grocery expenses, and minimize food waste",
                "file": "grocery_planner.py"
            }
        ],
        "Productivity": [
            {
                "title": "Task Time Estimator",
                "description": "Get AI-powered estimates for task completion times, track productivity, and improve time management",
                "file": "task_estimator.py"
            }
        ]
    }

    # Create tiles for each category
    for category, apps in calculators.items():
        st.markdown(f"## {category}")
        
        # Calculate number of columns and empty slots needed
        num_apps = len(apps)
        num_cols = 3
        num_empty = (num_cols - (num_apps % num_cols)) % num_cols
        
        # Create columns
        cols = st.columns(num_cols)
        
        # Distribute calculators across columns
        for i, app in enumerate(apps):
            with cols[i % num_cols]:
                create_tile(
                    app["title"],
                    app["description"],
                    app["file"]
                )
        
        # Add empty tiles to maintain grid
        for i in range(num_empty):
            with cols[(num_apps + i) % num_cols]:
                st.markdown("""
                <div style='
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    margin: 0.5rem 0;
                    height: 220px;
                    visibility: hidden;
                '></div>
                """, unsafe_allow_html=True)

    # About section
    st.markdown('<div id="about"></div>', unsafe_allow_html=True)
    show_about_section()

    # Features section
    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    show_features_section()

    # Contact section
    st.markdown('<div id="contact"></div>', unsafe_allow_html=True)
    show_contact_section()

    # Footer
    create_footer()

if __name__ == "__main__":
    main()
