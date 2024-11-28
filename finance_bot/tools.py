from datetime import date

import pandas as pd
import yfinance as yf
from langchain_core.tools import tool
from pandas import DataFrame


@tool
def company_information(ticker: str) -> dict:
    """Use this tool to retrieve company information like address,
    industry, sector, company officers, business summary, website,
    marketCap, current price, ebitda, total debt, total revenue,
    debt-to-equity, etc."""

    ticker_obj = yf.Ticker(ticker)
    ticker_info = ticker_obj.get_info()

    return ticker_info


@tool
def company_financials(ticker: str) -> DataFrame:
    """
    Use this tool to retrieve company's financials information like EBITDA, EBIT,
    Net Income, Tax Rate, Gross Profit, etc. They include information to calculate other indicators.

    Args:
        - ticker (str): The ticker symbol (e.g., 'NVDA' for Nvidia).
    Return:
        - dict: A dictionary containing the financial information from 2021 of the company.
    """
    ticker_obj = yf.Ticker(ticker)
    ticker_financials = ticker_obj.financials

    return ticker_financials


@tool
def stock_news(ticker: str) -> list:
    """
    Use this to retrieve latest news articles discussing particular stock ticker.

    Args:
        - ticker (str): The stock ticker symbol.
    Return:
        - list: A list containing the link to the latest news of this company
    """
    ticker_obj = yf.Ticker(ticker)

    return ticker_obj.get_news()


@tool
def last_dividend_and_earnings_date(ticker: str) -> dict:
    """
    Use this tool to retrieve company's last dividend date and earnings release dates.
    It does not provide information about historical dividend yields.
    """
    ticker_obj = yf.Ticker(ticker)

    return ticker_obj.get_calendar()


@tool
def summary_of_mutual_fund_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top mutual fund holders.
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = yf.Ticker(ticker)
    mf_holders = ticker_obj.get_mutualfund_holders()

    return mf_holders.to_dict(orient="records")


@tool
def summary_of_institutional_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top institutional holders.
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = yf.Ticker(ticker)
    inst_holders = ticker_obj.get_institutional_holders()

    return inst_holders.to_dict(orient="records")


@tool
def stock_grade_updrages_downgrades(ticker: str) -> dict:
    """
    Use this to retrieve grade ratings upgrades and downgrades details of particular stock.
    It'll provide name of firms along with 'To Grade' and 'From Grade' details. Grade date is also provided.
    """
    ticker_obj = yf.Ticker(ticker)

    curr_year = date.today().year

    upgrades_downgrades = ticker_obj.get_upgrades_downgrades()
    upgrades_downgrades = upgrades_downgrades.loc[
        upgrades_downgrades.index > f"{curr_year}-01-01"
    ]
    upgrades_downgrades = upgrades_downgrades[
        upgrades_downgrades["Action"].isin(["up", "down"])
    ]

    return upgrades_downgrades.to_dict(orient="records")


@tool
def stock_splits_history(ticker: str) -> dict:
    """
    Use this tool to retrieve company's historical stock splits data.
    """
    ticker_obj = yf.Ticker(ticker)
    hist_splits = ticker_obj.get_splits()

    return hist_splits.to_dict()


@tool
def get_growth_metrics(ticker: str) -> dict[str, str] | DataFrame:
    """
    Use this tool to retrieve growth metrics for a given stock ticker.
    Returns a dictionary containing Net Revenue Growth, Profit After Tax growth, and Earnings Growth Rate.

    Argss:
    - ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple).

    Return:
        -  DataFrame: A DataFrame that contain some useful solvency ratios that help evaluate the stock ticker.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        financials = ticker_obj.financials

        # Get Net Revenue Growth
        revenue = financials.loc["Total Revenue"][:2]

        # Get Profit After Tax growth
        net_income = financials.loc["Net Income"][:2]

        # Get Earnings Growth Rate
        gross_profit = financials.loc["Gross Profit"][:2]

        # Calculate growth rate
        def calculate_growth_rate(current, previous):
            if previous == 0:
                return None
            return (current - previous) / previous * 100

        net_revenue_growth = calculate_growth_rate(revenue[0], revenue[1])
        profit_after_tax_growth = calculate_growth_rate(net_income[0], net_income[1])
        earnings_growth_rate = calculate_growth_rate(gross_profit[0], gross_profit[1])

        growth_metrics = {
            "Net Revenue Growth": net_revenue_growth,
            "Profit After Tax Growth": profit_after_tax_growth,
            "Earnings Growth Rate": earnings_growth_rate,
        }

    except Exception as e:
        return {"error": str(e)}

    growth_metrics_df = pd.DataFrame([growth_metrics], index=["Value"])

    if growth_metrics_df.empty:
        return pd.DataFrame(columns=["Growth Metrics", "Value"])

    return growth_metrics_df.reset_index(drop=True)
