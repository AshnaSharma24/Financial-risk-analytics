import matplotlib.pyplot as plt
import seaborn as sns

# cumulative returns plot
def plot_cumulative_returns(returns):
    cumulative = (1 + returns).cumprod()    #growth of money over time

    fig, ax = plt.subplots(figsize=(12,6))
    cumulative.plot(ax=ax)

    ax.set_title("Cumulative Returns")

    return fig

# rolling volatility plot
def plot_rolling_volatility(returns, window=30):
    rolling_vol = returns.rolling(window).std() * (252 ** 0.5)

    fig, ax = plt.subplots(figsize=(12,6))
    rolling_vol.plot(ax=ax)

    ax.set_title("Rolling Volatility")

    return fig

# correlation heatmap ie how different assets are correlated with each other
def plot_correlation_heatmap(returns):
    corr = returns.corr()

    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

    ax.set_title("Correlation Heatmap")

    return fig