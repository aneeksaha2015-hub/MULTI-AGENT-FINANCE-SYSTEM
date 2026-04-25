from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import market_tool , technical_tool , fundamental_tool , news_tool
import streamlit as st

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0,
    api_key=st.secrets["MISTRAL_API_KEY"]
)

# -- AGENTS --

def build_market_agent():
    return create_agent(model = llm , tools=[market_tool])


def build_technical_agent():
    return create_agent(model = llm , tools=[technical_tool])


def build_fundamental_agent():
    return create_agent(model = llm , tools=[fundamental_tool])


def build_news_agent():
    return create_agent(model = llm , tools=[news_tool])

# ── RISK AGENT (CHAIN) ──

risk_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a financial risk analyst."),
    ("human", """
Analyze risk for this stock.

Market: {market}
Technical: {technical}
Fundamental: {fundamental}
News: {news}

Give:
- Risk Level (Low/Medium/High)
- Key Risks
- Volatility Insight
""")
])

risk_chain = risk_prompt | llm | StrOutputParser()


# ── DECISION AGENT (CHAIN) ──

decision_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hedge fund decision maker."),
    ("human", """
Based on all analysis:

Market: {market}
Technical: {technical}
Fundamental: {fundamental}
News: {news}
Risk: {risk}

Give FINAL DECISION:
- Buy / Hold / Sell
- Strong reasoning
""")
])

decision_chain = decision_prompt | llm | StrOutputParser()


# ── REFINER (REPLACES CRITIC) ──

refiner_prompt = ChatPromptTemplate.from_messages([
    ("system", "You improve financial reports."),
    ("human", """
Refine and improve this report:

{report}

Make it:
- clearer
- more professional
- more confident
""")
])

refiner_chain = refiner_prompt | llm | StrOutputParser()


# =========================
# SENTIMENT CHAIN (NEW)
# =========================

sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a financial sentiment analyst."),
    ("human", """
Analyze the sentiment of the following financial news:

{news}

Return:
- Overall Sentiment (Bullish / Bearish / Neutral)
- Key Drivers (bullet points)
- Impact on stock price
""")
])

sentiment_chain = sentiment_prompt | llm | StrOutputParser()


# =========================
# CONFLICT RESOLVER (NEW)
# =========================

conflict_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hedge fund decision engine."),
    ("human", """
Market Data:
{market}

Technical Analysis:
{technical}

Fundamental Analysis:
{fundamental}

News Sentiment:
{sentiment}

Based on ALL signals:

1. Resolve any conflicts
2. Give FINAL DECISION:

Return strictly:

Decision: Buy / Sell / Hold
Confidence: %
Entry Zone:
Target:
Stop Loss:
Reasoning:
""")
])

conflict_chain = conflict_prompt | llm | StrOutputParser()

# =========================
# PRICE STRATEGY CHAIN (NEW 🔥)
# =========================

price_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a quantitative trading analyst."),
    ("human", """
Stock Market Data:
{market}

Technical:
{technical}

Support / Resistance:
{levels}

Generate:

- Entry Range (near support)
- Target (near resistance)
- Stop Loss (below support)
- Explain using real price levels

Be realistic. No guessing.
""")
])

price_chain = price_prompt | llm | StrOutputParser()

