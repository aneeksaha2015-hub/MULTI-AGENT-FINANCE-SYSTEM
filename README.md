# ◈ QuantMind AI — Multi-Agent Finance Intelligence System

🚀 Live App: https://multi-agent-finance-system.streamlit.app/

---

## 📌 Overview

**QuantMind AI** is an advanced multi-agent financial intelligence system that analyzes stock market data using specialized AI agents working in parallel.

Each agent focuses on a specific domain:
- Market Data Analysis
- Technical Indicators (RSI, MACD, SMA)
- Fundamental Analysis
- News & Sentiment Intelligence
- Price Level Detection
- Risk Evaluation
- Quantitative Strategy Generation
- Final Decision Engine

The system combines all outputs into a **single institutional-grade trading decision**.

---
                                                                                                                    

📊 Unified Investment Verdict (BUY / SELL / HOLD)

---

## ⚙️ Features

### 📈 Market Intelligence
- Real-time stock price (Yahoo Finance)
- OHLC + Volume analysis
- Session range tracking

### 📊 Technical Analysis
- RSI (14-period)
- MACD (trend strength)
- SMA (20-period)
- Signal interpretation

### 🏦 Fundamental Analysis
- Market cap
- P/E ratio
- EPS
- Sector classification

### 📰 News & Sentiment Engine
- Live financial news (Tavily API)
- AI sentiment classification:
  - Bullish
  - Bearish
  - Neutral

### ⚡ Quant Strategy Engine
- Entry zones
- Target levels
- Stop-loss suggestions
- Support/resistance modeling

### 🧠 AI Decision System
- Multi-agent consensus
- Conflict resolution engine
- Final BUY / SELL / HOLD recommendation
- Confidence scoring

---

## 🧩 Tech Stack

- **Frontend:** Streamlit
- **LLM:** Mistral AI (LangChain)
- **APIs:**
  - Yahoo Finance (yfinance)
  - Alpha Vantage
  - Tavily Search API
- **Backend Logic:**
  - LangChain Agents
  - Custom Python Financial Engine

---

## 📁 Project Structure
project/
│
├── app.py # Streamlit UI
├── agents.py # AI agents + chains
├── tools.py # LangChain tools
├── utils.py # Financial calculations
├── pipelines.py # Orchestrator pipeline
│
├── .streamlit/
│ └── secrets.toml # API keys (production)
│
├── requirements.txt
└── README.md


---

## 🔐 API Keys Required

Set secrets in Streamlit Cloud:
ALPHA_VANTAGE_API_KEY = "your_key"
TAVILY_API_KEY = "your_key"
MISTRAL_API_KEY = "your_key" toml 

🚀 How It Works
User enters stock symbol (e.g. AAPL)
Multiple AI agents run in parallel
Market + technical + sentiment data collected
Quant models compute levels & indicators
Decision engine resolves conflicts
Final investment verdict generated
Streamlit UI renders institutional dashboard

📊 Example Output
BUY / SELL / HOLD decision
Confidence score (%)
Entry / Target / Stop-loss zones
Market sentiment (Bullish / Bearish / Neutral)
Risk level assessment
⚠️ Disclaimer

This project is for educational and research purposes only.
It does not constitute financial advice.

🧠 Future Improvements
Portfolio tracking system
Live streaming market updates
Backtesting engine
Multi-stock comparison dashboard
Crypto + forex expansion
Agent memory layer (long-term learning)

👨‍💻 Author
Built with ❤️ using Streamlit + LangChain + Mistral AI
