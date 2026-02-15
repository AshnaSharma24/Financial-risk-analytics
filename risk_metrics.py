import numpy as np

# Calculate returns from price data 
# pct_change() computes the percentage change between the current and a previous element.
def cal_returns(prices):
    return prices.pct_change().dropna()

#to convert the daily risk (volatility) of an asset into an annualized risk. 252 trading days in a year
def volatility(returns):
    return returns.std() * np.sqrt(252)  

#High Sharp Ratio = Smooth returns, consistent growth. Low/Negative Sharp Ratio = Wild fluctuations, or returns not worth the risk. 
# return per unit of risk
def sharpe_ratio(returns, risk_free_rate=0.02):                     # risk_free_rate is the return of a risk-free asset 
    excess_returns = returns - risk_free_rate / 252                 # actual returns - risk-free returns (adjusted for daily)
    return (excess_returns.mean() / returns.std()) * np.sqrt(252)

# estimate of the potential maximum loss  over a given time period at a certain confidence level.
# There is a 95% chance that your actual loss will be less than 2%
def value_at_risk(returns, confidence=5):
    if returns.empty:
        raise ValueError("Returns data is empty.")
    return np.percentile(returns.dropna(), confidence)
