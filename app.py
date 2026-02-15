import streamlit as st
import numpy as np

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

st.title("📈 Financial Portfolio Risk & Analytics Engine")


# ---------- USER INPUT ----------
tickers = st.text_input(
    "Enter stock tickers (comma separated):",
    "AAPL,MSFT,TSLA"
)

weights_input = st.text_input(
    "Enter portfolio weights (comma separated):",
    "0.4,0.3,0.3"
)


# ---------- INPUT VALIDATION ----------
if not tickers.strip():
    st.warning("Please enter at least one ticker.")
    st.stop()

try:
    stocks = [t.strip().upper() for t in tickers.split(",")]
    weights = np.array([float(w) for w in weights_input.split(",")])

except:
    st.error("Invalid input format. Please check tickers and weights.")
    st.stop()


if st.button("Analyze Portfolio"):

    with st.spinner("Fetching market data..."):

        try:
            # ---------- FETCH DATA ----------
            data = fetch_stock_data(stocks)
            cleaned = clean_data(data)

        except ValueError:
            st.error("""
❌ No valid tickers found.

Tips:
• US stocks → AAPL, MSFT, TSLA  
• Indian stocks → RELIANCE.NS, TCS.NS
""")
            st.stop()

        except Exception:
            st.error("Something went wrong while fetching market data.")
            st.stop()


        # ---------- SHOW VALID STOCKS ----------
        valid_stocks = cleaned.columns.tolist()
        st.success(f"Stocks used for analysis: {valid_stocks}")


        # ---------- PORTFOLIO CHECK ----------
        if len(valid_stocks) < 2:
            st.error("Need at least TWO valid stocks for portfolio analysis.")
            st.stop()


        # ---------- AUTO FIX WEIGHTS ----------
        if len(weights) != len(valid_stocks):

            st.warning("Some tickers were invalid. Adjusting weights automatically.")

            weights = np.repeat(1/len(valid_stocks), len(valid_stocks))

            st.info(f"New weights applied: {weights}")


        if not np.isclose(sum(weights), 1):
            st.warning("Weights should sum to 1. Normalizing automatically.")
            weights = weights / sum(weights)


        try:
            # ---------- CALCULATIONS ----------
            returns = cal_returns(cleaned)

            if returns.empty:
                st.error("Not enough data to calculate returns.")
                st.stop()

            p_return, p_vol = portfolio_performance(returns, weights)

            vol = volatility(returns).mean()
            sharpe = sharpe_ratio(returns).mean()
            var = value_at_risk(returns).mean()

        except Exception:
            st.error("Error while calculating portfolio metrics.")
            st.stop()


    # ---------- DISPLAY METRICS ----------
    st.subheader("📊 Key Risk Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Expected Return", f"{p_return:.2%}")
    col2.metric("Portfolio Volatility", f"{p_vol:.2%}")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

    st.metric("Value at Risk (5%)", f"{var:.2%}")


    # ---------- GRAPHS ----------
    try:
        st.subheader("Cumulative Returns")
        st.pyplot(plot_cumulative_returns(returns))

        st.subheader("Rolling Volatility")
        st.pyplot(plot_rolling_volatility(returns))

        st.subheader("Correlation Heatmap")
        st.pyplot(plot_correlation_heatmap(returns))

    except Exception:
        st.warning("Could not generate some visualizations.")
