import plotly.graph_objects as go
import plotly.express as px


# ---------- CUMULATIVE RETURNS ----------
def plot_cumulative_returns(returns):

    cumulative = (1 + returns).cumprod()

    fig = go.Figure()

    for col in cumulative.columns:

        fig.add_trace(
            go.Scatter(
                x=cumulative.index,
                y=cumulative[col],
                mode='lines',
                name=col,
                line=dict(width=3)
            )
        )

    fig.update_layout(

        title="Cumulative Returns",

        template="plotly_dark",

        height=500,

        paper_bgcolor="#050A18",
        plot_bgcolor="#050A18",

        font=dict(
            color="#E0FFFF",
            size=14
        ),

        title_font=dict(
            size=24,
            color="#00FFFF"
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        hovermode="x unified"
    )

    return fig


# ---------- ROLLING VOLATILITY ----------
def plot_rolling_volatility(returns, window=30):

    rolling_vol = returns.rolling(window).std() * (252 ** 0.5)

    fig = go.Figure()

    for col in rolling_vol.columns:

        fig.add_trace(
            go.Scatter(
                x=rolling_vol.index,
                y=rolling_vol[col],
                mode='lines',
                name=col,
                line=dict(width=2)
            )
        )

    fig.update_layout(

        title=f"Rolling Volatility ({window} Days)",

        template="plotly_dark",

        height=500,

        paper_bgcolor="#050A18",
        plot_bgcolor="#050A18",

        font=dict(
            color="#E0FFFF",
            size=14
        ),

        title_font=dict(
            size=24,
            color="#00FFFF"
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        hovermode="x unified"
    )

    return fig


# ---------- CORRELATION HEATMAP ----------
def plot_correlation_heatmap(returns):

    corr = returns.corr()

    fig = px.imshow(

        corr,

        color_continuous_scale="RdBu_r",

        aspect="auto",

        text_auto=False
    )

    fig.update_layout(

        title="Stock Correlation Heatmap",

        template="plotly_dark",

        height=850,

        paper_bgcolor="#050A18",
        plot_bgcolor="#050A18",

        font=dict(
            color="#E0FFFF",
            size=13
        ),

        title_font=dict(
            size=24,
            color="#00FFFF"
        ),

        coloraxis_colorbar=dict(
            title="Correlation"
        )
    )

    return fig
