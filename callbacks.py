from dash import Output, Input, html, dcc, callback_context
import dash
import plotly.express as px
from visuals.time_series import create_time_series_chart
import pandas as pd

def register_callbacks(app, time_series_df):

    @app.callback(
        Output("time-series-chart", "figure"),
        Input("stock-selector", "value"),
        Input("date-range-slider", "value")
    )
    def update_main_chart(selected_tickers, date_range):
        return create_time_series_chart(time_series_df, selected_tickers, date_range)

    @app.callback(
        Output("stock-concept-output", "children"),
        Input("stock-concept-dropdown", "value")
    )
    def update_stock_concept_info(concept):
        descriptions = {
            "volume": """
    ### Volume  
    **What It Is:** Total number of shares traded during a given day.  
    **Why It Matters:** High volume can signal strong investor interest or market-moving news.  
    **How to Use It:** Volume spikes often confirm price trends — big moves on high volume are more reliable.  
    **Fun Fact:** NVIDIA’s trading volume jumped over 250% on its May 2023 earnings day.
    """,
            "close": """
    ### Closing Price  
    **What It Is:** The final price at which a stock trades before the market closes (4 PM EST).  
    **Why It Matters:** Used in most charts and news headlines. It's the baseline for calculating daily gains/losses.  
    **How to Use It:** Compare the close to the previous day’s to gauge direction.  
    **Fun Fact:** NVIDIA closed at an all-time high in November 2023.
    """,
            "open": """
    ### Opening Price  
    **What It Is:** The first price a stock trades at when the market opens at 9:30 AM EST.  
    **Why It Matters:** Reflects overnight news, premarket activity, and investor sentiment.  
    **How to Use It:** Compare it to the prior close to assess early momentum.  
    **Fun Fact:** Big “gap ups” at open often suggest bullish market reaction.
    """,
            "high": """
    ### High Price  
    **What It Is:** The highest price reached during a trading day.  
    **Why It Matters:** Traders use it to identify potential resistance levels.  
    **How to Use It:** Helps gauge upward momentum and spot breakout points.  
    **Fun Fact:** NVIDIA hit a new intraday high just hours after releasing its Q2 2023 earnings.
    """,
            "low": """
    ### Low Price  
    **What It Is:** The lowest price a stock traded at during the session.  
    **Why It Matters:** Useful for identifying market support and investor fear.  
    **How to Use It:** Can inform stop-loss strategies and dip-buying opportunities.  
    **Fun Fact:** Sudden low dips followed by rebounds are called “hammer patterns.”
    """,
            "adj_close": """
    ### Adjusted Close  
    **What It Is:** Closing price adjusted for dividends, splits, and other events.  
    **Why It Matters:** More accurate for long-term analysis and return calculations.  
    **How to Use It:** Use this over raw closing price when back-testing strategies or comparing over time.  
    **Fun Fact:** Without adjusted close, Apple’s 7-for-1 stock split would look like a massive price crash.
    """,
            "earnings": """
    ### Earnings  
    **What It Is:** A company’s quarterly report on profits, revenue, and other financials.  
    **Why It Matters:** Stock prices often jump or drop based on earnings surprises.  
    **How to Use It:** Monitor earnings calendars — a big earnings “beat” or “miss” can move the whole market.  
    **Fun Fact:** NVIDIA rose 24% in one day after blowing past expectations in Q2 2023.
    """
        }

        return dcc.Markdown(descriptions.get(concept, ""))

    @app.callback(
        Output("nvda-price-chart", "figure"),
        Output("nvda-volume-chart", "figure"),
        Output("nvda-summary", "children"),
        Input("tabs", "active_tab"),
        Input("nvda-earnings-zoom", "value")
    )
    def update_nvda_tab(tab, selected_earnings_date):
        ctx = callback_context

        if not ctx.triggered:
            return {}, {}, ""

        if tab != "tab-nvda":
            raise dash.exceptions.PreventUpdate

        df = time_series_df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Price"] = df["NVIDIA"]
        df["Volume"] = df["NVIDIA"] * 0.75e6

        if selected_earnings_date:
            selected_date = pd.to_datetime(selected_earnings_date)
            start = selected_date - pd.Timedelta(days=5)
            end = selected_date + pd.Timedelta(days=5)
            df = df[(df["Date"] >= start) & (df["Date"] <= end)]

        price_fig = px.line(df, x="Date", y="Price", title="NVIDIA Stock Price (Raw)",
                            labels={"Price": "Price (USD)"})
        price_fig.update_layout(template="plotly_white")

        vol_fig = px.bar(df, x="Date", y="Volume", title="NVIDIA Volume (Simulated)",
                         labels={"Volume": "Volume"})
        vol_fig.update_layout(template="plotly_white")

        df_full = time_series_df.copy()
        df_full["Date"] = pd.to_datetime(df_full["Date"])

        pct_2023 = ((df_full[df_full["Date"].dt.year == 2023]["NVIDIA"].iloc[-1] -
                     df_full[df_full["Date"].dt.year == 2023]["NVIDIA"].iloc[0]) /
                    df_full[df_full["Date"].dt.year == 2023]["NVIDIA"].iloc[0]) * 100

        pct_2024 = ((df_full[df_full["Date"].dt.year == 2024]["NVIDIA"].iloc[-1] -
                     df_full[df_full["Date"].dt.year == 2024]["NVIDIA"].iloc[0]) /
                    df_full[df_full["Date"].dt.year == 2024]["NVIDIA"].iloc[0]) * 100

        summary = html.Div([
        ], style={"marginTop": "15px", "lineHeight": "1.8"})

        return price_fig, vol_fig, summary

    @app.callback(
        Output("company-info", "children"),
        Input("company-dropdown", "value")
    )
    def display_company_info(company):
        descriptions = {
            "NVDA": """
        ### NVIDIA Corporation (NVDA)  
        **What They Do:** Design GPUs for gaming, AI, and self-driving cars.  
        **What They Sell:** High-end chips like the H100, RTX series, and AI software.  
        **Why It Matters:** Their chips power ChatGPT and most cutting-edge AI — they’re at the heart of the AI gold rush.
        """,
            "AMD": """
        ### Advanced Micro Devices, Inc. (AMD)  
        **What They Do:** Make CPUs and GPUs for PCs, servers, and gaming.  
        **What They Sell:** Ryzen CPUs, Radeon GPUs, and EPYC server chips.  
        **Why It Matters:** NVIDIA’s top competitor in the chip space, and gaining ground in AI and data centers.
        """,
            "INTC": """
        ### Intel Corporation (INTC)  
        **What They Do:** Longtime CPU leader and major player in semiconductor tech.  
        **What They Sell:** Core and Xeon processors, plus new Arc GPUs.  
        **Why It Matters:** Still huge in traditional computing but trying to catch up in AI infrastructure.
        """,
            "MSFT": """
        ### Microsoft Corporation (MSFT)  
        **What They Do:** Software giant, cloud computing powerhouse, and AI investor.  
        **What They Sell:** Office 365, Azure, and OpenAI-powered tools.  
        **Why It Matters:** Their partnership with OpenAI means they’re a massive buyer of NVIDIA chips.
        """,
            "DELL": """
        ### Dell Technologies Inc. (DELL)  
        **What They Do:** PC and enterprise hardware provider.  
        **What They Sell:** Servers, laptops, desktops, and cloud infrastructure gear.  
        **Why It Matters:** Dell integrates NVIDIA tech into servers — growing relevance in AI data centers.
        """,
            "HPE": """
        ### Hewlett Packard Enterprise Company (HPE)  
        **What They Do:** Build cloud and edge computing infrastructure.  
        **What They Sell:** Servers, storage, and enterprise services.  
        **Why It Matters:** Competes in the AI server space — uses NVIDIA chips in enterprise solutions.
        """,
            "SMCI": """
        ### Super Micro Computer, Inc. (SMCI)  
        **What They Do:** Make custom AI and high-performance servers.  
        **What They Sell:** GPU-optimized server racks using NVIDIA hardware.  
        **Why It Matters:** Their stock exploded alongside NVIDIA — they scale AI infrastructure globally.
        """,
            "SPY": """
        ### S&P 500 Index Fund (SPY)  
        **What It Is:** An index tracking the 500 largest U.S. companies.  
        **Why It Matters:** Serves as a benchmark for the whole U.S. stock market — NVIDIA is now one of its top components.
        """,
            "QQQ": """
        ### Invesco QQQ Trust (QQQ)  
        **What It Is:** Index of the top 100 non-financial tech-heavy companies listed on NASDAQ.  
        **Why It Matters:** NVIDIA is a core part of this — their rise pushes the whole index higher.
        """
        }

        return dcc.Markdown(descriptions.get(company, ""))



