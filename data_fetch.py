import yfinance as yf
import pandas as pd


def fetch_stock_data(tickers, period="5y"):

    valid_data = pd.DataFrame()

    for ticker in tickers:

        # ---------- TRY ORIGINAL ----------
        data = yf.download(
            ticker,
            period=period,
            auto_adjust=True,
            progress=False
        )["Close"]

        # ---------- FALLBACK TO .NS ----------
        if data.empty and "." not in ticker:

            ns_ticker = ticker + ".NS"

            data = yf.download(
                ns_ticker,
                period=period,
                auto_adjust=True,
                progress=False
            )["Close"]

            if not data.empty:
                ticker = ns_ticker   # rename column correctly

        # ---------- STORE IF VALID ----------
        if not data.empty:
            valid_data[ticker] = data

    if valid_data.empty:
        raise ValueError("No valid tickers found.")

    return valid_data
