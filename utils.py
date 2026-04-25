import yfinance as yf
import requests
import os
import streamlit as st

ALPHA_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]

def get_stock_price(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")

    if data.empty:
        return "No data"

    d = data.iloc[-1]
    return {
        "price": float(d["Close"]),
        "open": float(d["Open"]),
        "high": float(d["High"]),
        "low": float(d["Low"]),
        "volume": int(d["Volume"]),
    }

def get_rsi(symbol: str):
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval=daily&time_period=14&series_type=close&apikey={ALPHA_KEY}"
    res = requests.get(url).json()
    try:
        return list(res["Technical Analysis: RSI"].values())[0]
    except:
        return "No RSI"

def get_fundamentals(symbol: str):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_KEY}"
    res = requests.get(url).json()

    if "Name" not in res:
        return "No fundamentals"

    return {
        "name": res["Name"],
        "sector": res["Sector"],
        "market_cap": res["MarketCapitalization"],
        "pe_ratio": res["PERatio"],
        "eps": res["EPS"],
    }



def get_price_levels(symbol: str):
    df = yf.download(symbol, period="3mo", progress=False)

    if df.empty:
        return {"error": "No data found"}

    low = df["Low"]
    high = df["High"]
    close = df["Close"]

    # FIX multi-index
    if hasattr(low, "squeeze"):
        low = low.squeeze()
        high = high.squeeze()
        close = close.squeeze()

    support = float(low.min())
    resistance = float(high.max())
    current_price = float(close.iloc[-1])

    return {
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "current_price": round(current_price, 2)
    }



def get_sma(symbol: str, period: int = 20):
    df = yf.download(symbol, period="3mo", progress=False)

    if df.empty:
        return {"error": "No data"}

    close = df["Close"]

    # FIX: handle multi-index case
    if isinstance(close, type(df)):
        close = close.squeeze()

    sma_series = close.rolling(window=period).mean()

    sma_value = sma_series.iloc[-1]

    return round(float(sma_value), 2)

def get_macd(symbol: str):
    df = yf.download(symbol, period="3mo", progress=False)

    if df.empty:
        return {"error": "No data"}

    close = df["Close"].squeeze()

    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    return {
        "macd": round(float(macd.iloc[-1]), 2),
        "signal": round(float(signal.iloc[-1]), 2)
    }