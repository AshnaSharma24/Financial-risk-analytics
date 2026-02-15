import numpy as np

#returns = behavior of stocks ; weights = your investment choices

def portfolio_performance(returns, weights):

    mean_returns = returns.mean() * 252     # yearly avg returns
    cov_matrix = returns.cov() * 252        # how the stocks move together ie volatility of the stocks

    portfolio_return = np.dot(weights, mean_returns) #  weighted sum of the expected returns of the individual assets

    #calculates overall portfolio risk using covariance between assets.
    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(cov_matrix, weights))
    )

    # returns expected return and volatility/risk of the portfolio
    return portfolio_return, portfolio_volatility
