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

st.set_page_config(
    page_title="Financial Risk Analytics Engine",
    layout="wide"
)

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

st.title("📈 Financial Portfolio Risk & Analytics Engine")

st.markdown("## 🌍 Market Overview")

market_col1, market_col2, market_col3 = st.columns(3)

try:
    sp500  = yf.Ticker("^GSPC").history(period="1d")
    nasdaq = yf.Ticker("^IXIC").history(period="1d")
    nifty  = yf.Ticker("^NSEI").history(period="1d")

    # ✅ Fixed: use .iloc[-1] instead of [-1]
    sp_change    = (sp500["Close"].iloc[-1]  - sp500["Open"].iloc[-1])  / sp500["Open"].iloc[-1]
    nas_change   = (nasdaq["Close"].iloc[-1] - nasdaq["Open"].iloc[-1]) / nasdaq["Open"].iloc[-1]
    nifty_change = (nifty["Close"].iloc[-1]  - nifty["Open"].iloc[-1])  / nifty["Open"].iloc[-1]

    market_col1.metric("S&P 500",  f"{sp500['Close'].iloc[-1]:.2f}",  f"{sp_change:.2%}")
    market_col2.metric("NASDAQ",   f"{nasdaq['Close'].iloc[-1]:.2f}", f"{nas_change:.2%}")
    market_col3.metric("NIFTY 50", f"{nifty['Close'].iloc[-1]:.2f}",  f"{nifty_change:.2%}")

except Exception:
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

volatility_window = st.sidebar.slider(
    "Rolling Volatility Window (Days)",
    min_value=7,
    max_value=180,
    value=30,
    step=1
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
        stocks  = [t.strip().upper() for t in tickers.split(",")]
        weights = np.array([float(w) for w in weights_input.split(",")])
    except Exception:
        st.error("Invalid input format. Please check tickers and weights.")
        st.stop()

    with st.spinner("Fetching market data..."):

        try:
            data    = fetch_stock_data(stocks)
            cleaned = clean_data(data)
        except ValueError as e:
            st.error(f"""
❌ No valid tickers found.

Tips:
• US stocks  → AAPL, MSFT, TSLA
• Indian stocks → RELIANCE.NS, TCS.NS
""")
            st.stop()
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")
            st.stop()

        valid_stocks = cleaned.columns.tolist()
        st.success(f"Stocks used for analysis: {valid_stocks}")

        if len(valid_stocks) < 2:
            st.error("Need at least TWO valid stocks for portfolio analysis.")
            st.stop()

        # ---------- AUTO FIX WEIGHTS ----------
        if len(weights) != len(valid_stocks):
            st.warning("Ticker/weight mismatch. Adjusting weights equally.")
            weights = np.repeat(1 / len(valid_stocks), len(valid_stocks))
            st.info(f"New equal weights applied: {weights.round(4).tolist()}")

        if not np.isclose(sum(weights), 1):
            st.warning("Weights don't sum to 1. Normalizing automatically.")
            weights = weights / sum(weights)

        try:
            returns = cal_returns(cleaned)

            if returns.empty:
                st.error("Not enough data to calculate returns.")
                st.stop()

            p_return, p_vol = portfolio_performance(returns, weights)
            sharpe           = sharpe_ratio(returns).mean()
            var              = value_at_risk(returns).mean()

        except Exception as e:
            st.error(f"Error calculating portfolio metrics: {e}")
            st.stop()

    # ---------- METRICS ----------
    st.markdown("## 📊 Portfolio Risk Metrics")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📈 Expected Return",  f"{p_return:.2%}")
    col2.metric("📉 Volatility",       f"{p_vol:.2%}")
    col3.metric("⚖ Sharpe Ratio",     f"{sharpe:.2f}")
    col4.metric("💥 VaR (5%)",         f"{var:.2%}")

    # ---------- INTERPRETATION ----------
    st.markdown("##  Portfolio Risk Interpretation")
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

    st.subheader("📈 Cumulative Returns")

    st.plotly_chart(
        plot_cumulative_returns(returns),
        use_container_width=True
    )

    st.subheader("📉 Rolling Volatility")

    st.plotly_chart(
        plot_rolling_volatility(
            returns,
            window=volatility_window
        ),
        use_container_width=True
    )

    st.subheader("🔥 Correlation Heatmap")

    st.plotly_chart(
        plot_correlation_heatmap(returns),
        use_container_width=True
    )

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<center>© 2026 Financial Risk Analytics Engine | Built with Streamlit</center>",
    unsafe_allow_html=True
)
