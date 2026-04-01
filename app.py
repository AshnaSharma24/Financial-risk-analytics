# import streamlit as st
# import numpy as np

# from data_fetch import fetch_stock_data
# from clean_data import clean_data
# from risk_metrics import cal_returns, volatility, sharpe_ratio, value_at_risk
# from portfolio import portfolio_performance
# from visualization import (
#     plot_cumulative_returns,
#     plot_rolling_volatility,
#     plot_correlation_heatmap
# )

# # ---------- PAGE CONFIG ----------
# st.set_page_config(
#     page_title="Financial Risk Analytics Engine",
#     layout="wide"
# )

# # ----------  HEADER ----------
# st.markdown("""
# # Financial Portfolio Risk & Analytics Engine
# ### Analyze portfolio performance, risk exposure, and diversification using real-time market data.
# """)

# st.info(
#     "Tip: Try combining US tech stocks (AAPL, MSFT) with Indian equities (RELIANCE.NS) to evaluate diversification."
# )

# # ---------- SIDEBAR ----------
# st.sidebar.header("Portfolio Settings")

# tickers = st.sidebar.text_input(
#     "Stock Tickers",
#     "AAPL,MSFT,TSLA"
# )

# weights_input = st.sidebar.text_input(
#     "Portfolio Weights",
#     "0.4,0.3,0.3"
# )

# analyze = st.sidebar.button("Analyze Portfolio")

# # ---------- INPUT VALIDATION ----------
# if not tickers.strip():
#     st.warning("Please enter at least one ticker.")
#     st.stop()

# try:
#     stocks = [t.strip().upper() for t in tickers.split(",")]
#     weights = np.array([float(w) for w in weights_input.split(",")])

# except:
#     st.error("Invalid input format. Please check tickers and weights.")
#     st.stop()


# # ---------- MAIN ANALYSIS ----------
# if analyze:

#     with st.spinner("Fetching live market data and running analytics..."):

#         try:
#             data = fetch_stock_data(stocks)
#             cleaned = clean_data(data)

#         except ValueError:
#             st.error("""
# ❌ No valid tickers found.

# Tips:
# • US stocks → AAPL, MSFT, TSLA  
# • Indian stocks → RELIANCE.NS, TCS.NS
# """)
#             st.stop()

#         except Exception:
#             st.error("Something went wrong while fetching market data.")
#             st.stop()

#         # ---------- VALID STOCKS ----------
#         valid_stocks = cleaned.columns.tolist()
#         st.success(f"Stocks used for analysis: {valid_stocks}")

#         if len(valid_stocks) < 2:
#             st.error("Need at least TWO valid stocks for portfolio analysis.")
#             st.stop()

#         # ---------- AUTO FIX WEIGHTS ----------
#         if len(weights) != len(valid_stocks):

#             st.warning("Some tickers were invalid. Adjusting weights automatically.")
#             weights = np.repeat(1/len(valid_stocks), len(valid_stocks))

#             st.info(f"New weights applied: {weights}")

#         if not np.isclose(sum(weights), 1):
#             st.warning("Weights should sum to 1. Normalizing automatically.")
#             weights = weights / sum(weights)

#         try:
#             returns = cal_returns(cleaned)

#             if returns.empty:
#                 st.error("Not enough data to calculate returns.")
#                 st.stop()

#             p_return, p_vol = portfolio_performance(returns, weights)

#             vol = volatility(returns).mean()
#             sharpe = sharpe_ratio(returns).mean()
#             var = value_at_risk(returns).mean()

#         except Exception:
#             st.error("Error while calculating portfolio metrics.")
#             st.stop()

#     # ---------- METRICS SECTION ----------
#     st.divider()
#     st.subheader("Portfolio Summary")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Expected Return", f"{p_return:.2%}")
#     col2.metric("Volatility", f"{p_vol:.2%}")
#     col3.metric("Sharpe Ratio", f"{sharpe:.2f}")
#     col4.metric("Value at Risk (5%)", f"{var:.2%}")

#     # ---------- VISUALIZATIONS ----------
#     st.divider()
#     st.subheader("Portfolio Visualizations")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.pyplot(plot_cumulative_returns(returns))

#     with col2:
#         st.pyplot(plot_rolling_volatility(returns))

#     st.pyplot(plot_correlation_heatmap(returns))


import streamlit as st
import numpy as np
import yfinance as yf

from data_fetch import fetch_stock_data
from clean_data import clean_data
from risk_metrics import cal_returns, volatility, sharpe_ratio, value_at_risk
from portfolio import portfolio_performance
from visualization import (
    plot_cumulative_returns,
    plot_rolling_volatility,
    plot_correlation_heatmap
)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Financial Risk Analytics Engine",
    layout="wide"
)

# ---------- PREMIUM CYAN THEME ----------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #050A18, #0A1F2C);
    color: #E0FFFF;
    font-family: 'Inter', sans-serif;
}

h1 {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    color: #00FFFF;
}

h2, h3 {
    color: #00E5FF;
}

section[data-testid="stSidebar"] {
    background: rgba(0, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(0,255,255,0.2);
}

div[data-testid="metric-container"] {
    background: rgba(0, 255, 255, 0.05);
    border: 1px solid rgba(0,255,255,0.4);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 0px 20px rgba(0,255,255,0.2);
    transition: 0.3s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-6px);
    box-shadow: 0px 0px 35px rgba(0,255,255,0.4);
}

div[data-testid="metric-container"] label {
    color: #00FFFF !important;
    font-weight: 600;
}

.stButton>button {
    background: linear-gradient(90deg, #00FFFF, #0088FF);
    color: black;
    font-weight: bold;
    border-radius: 14px;
    height: 3em;
    border: none;
    box-shadow: 0px 0px 15px rgba(0,255,255,0.4);
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 30px rgba(0,255,255,0.8);
}

.stTextInput>div>div>input {
    background-color: rgba(0,255,255,0.05);
    color: #00FFFF;
    border: 1px solid rgba(0,255,255,0.5);
    border-radius: 10px;
}

hr {
    border: 1px solid rgba(0,255,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("📈 Financial Portfolio Risk & Analytics Engine")

# ---------- MARKET OVERVIEW ----------
st.markdown("## 🌍 Market Overview")

market_col1, market_col2, market_col3 = st.columns(3)

try:
    sp500 = yf.Ticker("^GSPC").history(period="1d")
    nasdaq = yf.Ticker("^IXIC").history(period="1d")
    nifty = yf.Ticker("^NSEI").history(period="1d")

    sp_change = (sp500["Close"][-1] - sp500["Open"][-1]) / sp500["Open"][-1]
    nas_change = (nasdaq["Close"][-1] - nasdaq["Open"][-1]) / nasdaq["Open"][-1]
    nifty_change = (nifty["Close"][-1] - nifty["Open"][-1]) / nifty["Open"][-1]

    market_col1.metric("S&P 500", f"{sp500['Close'][-1]:.2f}", f"{sp_change:.2%}")
    market_col2.metric("NASDAQ", f"{nasdaq['Close'][-1]:.2f}", f"{nas_change:.2%}")
    market_col3.metric("NIFTY 50", f"{nifty['Close'][-1]:.2f}", f"{nifty_change:.2%}")

except:
    st.info("Market data currently unavailable.")

st.markdown("---")

# ---------- SIDEBAR ----------
st.sidebar.header("📌 Portfolio Configuration")

tickers = st.sidebar.text_input(
    "Stock Tickers (comma separated)",
    "AAPL,MSFT,TSLA"
)

weights_input = st.sidebar.text_input(
    "Portfolio Weights (comma separated)",
    "0.4,0.3,0.3"
)

analyze_button = st.sidebar.button("🚀 Analyze Portfolio")

# ---------- LANDING PAGE ----------
if not analyze_button:

    st.markdown("## 🚀 Advanced Portfolio Risk Intelligence Platform")
    st.markdown("""
    This platform provides quantitative portfolio analytics using statistical
    risk models and financial performance metrics.
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.markdown("""
    ### 📊 Quantitative Metrics  
    - Expected Returns  
    - Volatility  
    - Sharpe Ratio  
    - Value at Risk (VaR)  
    """)

    col2.markdown("""
    ### 📈 Visual Analytics  
    - Cumulative Returns  
    - Rolling Volatility  
    - Correlation Heatmaps  
    """)

    col3.markdown("""
    ### ⚡ Intelligent Processing  
    - Live market data fetching  
    - Weight normalization  
    - Invalid ticker handling  
    """)

    st.markdown("---")
    st.info("👈 Configure your portfolio in the sidebar and click **Analyze Portfolio** to begin.")

# ---------- ANALYSIS ----------
if analyze_button:

    try:
        stocks = [t.strip().upper() for t in tickers.split(",")]
        weights = np.array([float(w) for w in weights_input.split(",")])
    except:
        st.error("Invalid input format.")
        st.stop()

    with st.spinner("Fetching market data..."):

        try:
            data = fetch_stock_data(stocks)
            cleaned = clean_data(data)
        except:
            st.error("Error fetching stock data.")
            st.stop()

        valid_stocks = cleaned.columns.tolist()
        st.success(f"Stocks used for analysis: {valid_stocks}")

        if len(valid_stocks) < 2:
            st.error("Need at least TWO valid stocks.")
            st.stop()

        if len(weights) != len(valid_stocks):
            weights = np.repeat(1/len(valid_stocks), len(valid_stocks))

        if not np.isclose(sum(weights), 1):
            weights = weights / sum(weights)

        returns = cal_returns(cleaned)

        if returns.empty:
            st.error("Not enough data to calculate returns.")
            st.stop()

        p_return, p_vol = portfolio_performance(returns, weights)
        sharpe = sharpe_ratio(returns).mean()
        var = value_at_risk(returns).mean()

    # ---------- METRICS ----------
    st.markdown("## 📊 Portfolio Risk Metrics")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📈 Expected Return", f"{p_return:.2%}")
    col2.metric("📉 Volatility", f"{p_vol:.2%}")
    col3.metric("⚖ Sharpe Ratio", f"{sharpe:.2f}")
    col4.metric("💥 VaR (5%)", f"{var:.2%}")

    # ---------- INTERPRETATION ----------
    st.markdown("## 🧠 Portfolio Risk Interpretation")
    st.markdown("---")

    if sharpe > 1:
        st.success("✅ Strong risk-adjusted returns. Portfolio efficiency is healthy.")
    elif sharpe > 0.5:
        st.info("⚖ Moderate performance. Consider improving asset allocation.")
    else:
        st.warning("⚠ Low risk-adjusted return. Portfolio may be too volatile or underperforming.")

    if p_vol > 0.30:
        st.warning("⚠ High volatility detected. Suitable for aggressive investors.")
    elif p_vol < 0.15:
        st.success("📉 Low volatility profile. Conservative investment posture.")

    # ---------- VISUALS ----------
    st.markdown("## 📊 Portfolio Visual Analytics")
    st.markdown("---")

    st.subheader("Cumulative Returns")
    st.pyplot(plot_cumulative_returns(returns))

    st.subheader("Rolling Volatility")
    st.pyplot(plot_rolling_volatility(returns))

    st.subheader("Correlation Heatmap")
    st.pyplot(plot_correlation_heatmap(returns))

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<center>© 2026 Financial Risk Analytics Engine | Built with Streamlit</center>",
    unsafe_allow_html=True
)