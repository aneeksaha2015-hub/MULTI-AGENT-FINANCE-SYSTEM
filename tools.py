from langchain.tools import tool
from tavily import TavilyClient
import os
from dotenv import  load_dotenv
from utils import get_stock_price , get_rsi , get_fundamentals

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def market_tool(symbol: str) -> str:
    """Get latest stock price data (open, high, low, close, volume) for a given stock symbol."""
    return str(get_stock_price(symbol))

@tool
def technical_tool(symbol: str) -> str:
    """Fetch technical indicator RSI (Relative Strength Index) for a stock symbol."""
    return str(get_rsi(symbol))

@tool
def fundamental_tool(symbol : str) -> str:
    """Retrieve company fundamentals like PE ratio, EPS, market cap, and sector."""
    return str(get_fundamentals(symbol))

@tool
def news_tool(query: str) -> str:
    """Search and return latest financial news and sentiment about a company or stock."""
    
    res = tavily.search(query=query, max_results=5)

    out = []

    for i, r in enumerate(res["results"], 1):
        out.append(
            f"📰 Article {i}\n"
            f"🔹 Title   : {r['title']}\n"
            f"📝 Summary : {r['content'][:200]}...\n"
            f"🔗 Link    : {r['url']}\n"
        )

    return "\n" + ("=" * 60 + "\n").join(out)


