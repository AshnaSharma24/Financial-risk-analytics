# 📈 Financial Portfolio Risk & Analytics Engine

🔗 **Live App:**  
https://financial-risk-analytics-aecwvsaueeyezprswthvjb.streamlit.app/

---

## 🚀 Overview

The Financial Portfolio Risk & Analytics Engine is an interactive web application that helps investors analyze portfolio performance using real-time market data.

It calculates key financial risk metrics, visualizes asset behavior, and provides insights into diversification and volatility — enabling smarter investment decisions.

---

## ✨ Key Features

✅ Real-time stock data retrieval using Yahoo Finance  
✅ Intelligent ticker validation with automatic fallback (e.g., Indian stocks `.NS`)  
✅ Portfolio return & volatility calculation  
✅ Sharpe Ratio for risk-adjusted performance  
✅ Value at Risk (VaR) for downside estimation  
✅ Correlation heatmap to evaluate diversification  
✅ Rolling volatility analysis  
✅ Automatic portfolio weight normalization  
✅ Defensive error handling for invalid inputs  
✅ Interactive visualizations with Streamlit  

---

## 🧠 Tech Stack

**Frontend / App Layer**
- Streamlit

**Data & Analytics**
- Python  
- Pandas  
- NumPy  

**Visualization**
- Matplotlib  
- Seaborn  

**Market Data**
- yFinance API  

---

## 📊 Risk Metrics Implemented

### ✔ Expected Portfolio Return
Weighted average return of selected assets.

### ✔ Portfolio Volatility
Measures total portfolio risk using covariance.

### ✔ Sharpe Ratio
Evaluates return generated per unit of risk.

### ✔ Value at Risk (VaR)
Estimates the maximum expected loss at a given confidence level.

---

## ⚙️ How It Works

1. User enters stock tickers and portfolio weights  
2. App fetches historical market data  
3. Cleans and validates the dataset  
4. Computes financial risk metrics  
5. Generates visual insights  
6. Displays an interactive analytics dashboard  

---

## ▶️ Run Locally

Clone the repository:

```bash
git clone https://github.com/AshnaSharma24/Financial-risk-analytics.git
cd Financial-risk-analytics
