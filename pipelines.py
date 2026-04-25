from agents import (
    build_market_agent,
    build_fundamental_agent,
    build_technical_agent,
    build_news_agent,
    risk_chain,
    decision_chain,
    refiner_chain,
    sentiment_chain,
    conflict_chain,
    price_chain                
)

from utils import get_price_levels, get_sma , get_macd


def run_pipeline(symbol: str):
    state = {}

    # =========================
    # MARKET
    # =========================
    market_agent = build_market_agent()
    state['market'] = market_agent.invoke({
        "messages": [("user", f"Fetch real-time stock data for ticker: {symbol}")]
    })["messages"][-1].content

    # =========================
    # TECHNICAL
    # =========================
    tech_agent = build_technical_agent()
    state["technical"] = tech_agent.invoke({
        "messages": [("user", f"Get RSI indicator for stock: {symbol}")]
    })["messages"][-1].content

    # =========================
    # PRICE LEVELS (NEW)
    # =========================
    levels = get_price_levels(symbol)
    sma = get_sma(symbol)

    state["levels"] = levels
    state["sma"] = sma

    # =========================
    # MACD (NEW 🔥)
    # =========================
    macd = get_macd(symbol)
    state["macd"] = macd

    # =========================
    # FUNDAMENTAL
    # =========================
    fund_agent = build_fundamental_agent()
    state["fundamental"] = fund_agent.invoke({
        "messages": [("user", f"Get company fundamentals for: {symbol}")]
    })["messages"][-1].content

    # =========================
    # NEWS
    # =========================
    news_agent = build_news_agent()
    state["news"] = news_agent.invoke({
        "messages": [("user", f"Fetch latest financial news about: {symbol}")]
    })["messages"][-1].content

    # =========================
    # SENTIMENT
    # =========================
    state["sentiment"] = sentiment_chain.invoke({
        "news": state["news"]
    })

    # =========================
    # PRICE STRATEGY (NEW)
    # =========================
    state["price_strategy"] = price_chain.invoke({
        "market": state["market"],
        "technical": state["technical"],
        "levels": f"Support: {levels['support']}, Resistance: {levels['resistance']}, SMA: {sma}, MACD: {state['macd']['macd']} , Signal: {state['macd']['signal']} "
    })

    # =========================
    # RISK
    # =========================
    state["risk"] = risk_chain.invoke({
        "market": state["market"],
        "technical": state["technical"],
        "fundamental": state["fundamental"],
        "news": state["news"],
    })

    # =========================
    # DECISION (BASIC)
    # =========================
    state["decision"] = decision_chain.invoke({
        "market": state["market"],
        "technical": state["technical"],
        "fundamental": state["fundamental"],
        "news": state["news"],
        "risk": state["risk"],
    })

    # =========================
    # FINAL AI DECISION
    # =========================
    state["final_decision"] = conflict_chain.invoke({
        "market": state["market"],
        "technical": state["technical"],
        "fundamental": state["fundamental"],
        "sentiment": state["sentiment"],
        "macd": state["macd"]   
    })

    # =========================
    # FINAL REPORT (UPDATED)
    # =========================
    report = f"""
### Market
{state['market']}

### Technical
{state['technical']}

### Fundamental
{state['fundamental']}

### News
{state['news']}

### Sentiment
{state['sentiment']}

### Price Levels (REAL DATA)
Support: {levels['support']}
Resistance: {levels['resistance']}
SMA(20): {sma}

### MACD (Trend Strength 🔥)
MACD: {state['macd']['macd']}
Signal: {state['macd']['signal']}

### Price Strategy (Quant Based 🔥)
{state['price_strategy']}

### Risk
{state['risk']}

### Decision (Basic)
{state['decision']}

### AI Final Decision (Advanced 🚀)
{state['final_decision']}
"""

    # =========================
    # REFINER
    # =========================
    state["final"] = refiner_chain.invoke({
        "report": report
    })

    return state