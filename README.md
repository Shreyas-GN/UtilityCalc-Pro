# UtilityCalc Pro 🧮

A comprehensive suite of calculators and predictive tools designed to simplify your daily calculations and decision-making process. Built with Streamlit, this application offers a modern, user-friendly interface for various calculators ranging from finance to health and productivity.

## 🌟 Features

### Finance Calculators
- **Loan EMI Calculator**: Calculate loan payments and view amortization schedules
- **Investment Growth Calculator**: Plan investments with compound interest calculations
- **Mortgage Calculator**: Make informed home-buying decisions
- **Expense Tracker**: Track and analyze spending patterns
- **Salary Calculator**: Calculate take-home salary after deductions

### Health & Wellness
- **BMI Calculator**: Calculate BMI and get health recommendations
- **Calorie Calculator**: Get personalized daily calorie needs
- **Hydration Calculator**: Track water intake and get hydration tips
- **Sleep Calculator**: Optimize sleep schedule and track patterns

### Home & Utilities
- **Electricity Bill Calculator**: Track and estimate electricity costs
- **Grocery Planner**: Plan meals and generate shopping lists

### Productivity
- **Task Time Estimator**: Get AI-powered task completion estimates

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/utilitycalc-pro.git
cd utilitycalc-pro
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

## 🚀 Deployment

### GitHub Deployment
1. Create a new repository on GitHub
2. Initialize and push your code:
```bash
git init
git add .
git commit -m "Initial commit: UtilityCalc Pro - All-in-One Calculator Suite"
git branch -M main
git remote add origin https://github.com/yourusername/utilitycalc-pro.git
git push -u origin main
```

### Streamlit Cloud Deployment
1. Visit [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch (main)
5. Set main file path as: `app.py`
6. Click "Deploy!"

Your app will be live at: `https://yourusername-utilitycalc-pro-app-xxxxx.streamlit.app`

## 📁 Project Structure

```
utilitycalc-pro/
├── src/                    # Source code
│   ├── app.py             # Main application
│   └── calculators/       # Calculator modules
│       ├── bmi_calculator.py
│       ├── calorie_calculator.py
│       └── ...
├── data/                  # Data files
│   └── sample_data.json   # Example data
├── tests/                 # Test files
│   └── test_calculators.py
├── docs/                  # Documentation
│   └── CONTRIBUTING.md
├── static/               # Static files (CSS, JS)
├── assets/              # Images and other assets
├── run.py               # Entry point
├── requirements.txt     # Dependencies
├── README.md           # Project documentation
├── LICENSE             # MIT License
└── .gitignore         # Git ignore rules
```

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Data Visualization**: Plotly
- **Data Storage**: Local JSON files

## 📱 Usage
1. Launch the main application
2. Choose a calculator from the available categories
3. Each calculator opens in a new window for simultaneous use
4. Data is saved automatically for future reference

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author
- **Shreyas GN**
  - Email: shreyasgn@icloud.com
  - Website: https://shreyas-gn.github.io/
  - LinkedIn: https://linkedin.com/in/shreyas-gn

## ❤️ Acknowledgments
Special thanks to all contributors and users of UtilityCalc Pro!
