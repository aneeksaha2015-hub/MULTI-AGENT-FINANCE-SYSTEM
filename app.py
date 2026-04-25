import streamlit as st
import time
import re

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantMind AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, .stApp {
    background: #080b10;
    color: #e8eaf0;
    font-family: 'DM Mono', monospace;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, header, footer, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #2a3245; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00d4aa; }

/* ── NOISE OVERLAY ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 0; opacity: 0.4;
}

/* ── NAV BAR ── */
.qm-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 22px 56px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    position: sticky; top: 0; z-index: 100;
    background: rgba(8, 11, 16, 0.9);
}

.qm-logo {
    display: flex; align-items: center; gap: 12px;
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: 1.4rem; letter-spacing: -0.02em; color: #ffffff;
}

.qm-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #00d4aa, #0099ff);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 900;
}

.qm-nav-badge {
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    color: #00d4aa; border: 1px solid rgba(0,212,170,0.3);
    padding: 5px 16px; border-radius: 20px;
    letter-spacing: 0.1em; text-transform: uppercase;
}

/* ── HERO ── */
.qm-hero {
    padding: 72px 56px 48px; text-align: center; position: relative;
}

.qm-hero::after {
    content: ''; position: absolute; top: 0; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 320px;
    background: radial-gradient(ellipse, rgba(0,212,170,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.qm-eyebrow {
    font-family: 'DM Mono', monospace; font-size: 0.8rem;
    letter-spacing: 0.25em; text-transform: uppercase; color: #00d4aa;
    margin-bottom: 24px;
    display: flex; align-items: center; justify-content: center; gap: 14px;
}

.qm-eyebrow::before, .qm-eyebrow::after {
    content: ''; display: block; width: 48px; height: 1px;
    background: rgba(0,212,170,0.4);
}

.qm-headline {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    font-weight: 800; line-height: 1.08;
    letter-spacing: -0.03em; color: #ffffff; margin-bottom: 20px;
}

.qm-headline em {
    font-family: 'Instrument Serif', serif; font-style: italic;
    background: linear-gradient(90deg, #00d4aa, #0099ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.qm-subline {
    font-size: 1rem; color: rgba(232,234,240,0.45);
    max-width: 540px; margin: 0 auto; line-height: 1.75;
}

.qm-sublines-wrap {
    display: flex; gap: 80px; justify-content: center;
    max-width: 1000px; margin: 40px auto 0; text-align: left;
}
.qm-sublines-wrap .qm-subline {
    flex: 1; margin: 0;
}

/* ── TICKER CHIPS ── */
.qm-chips-container {
    display: flex; gap: 8px; justify-content: center; margin-top: 24px;
}

/* Style Streamlit buttons to look like chips */
div[data-testid="column"] button[kind="secondary"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: rgba(232,234,240,0.5) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    padding: 4px 12px !important;
    border-radius: 7px !important;
    height: auto !important;
    min-height: unset !important;
    line-height: 1 !important;
}

div[data-testid="column"] button[kind="secondary"]:hover {
    border-color: rgba(0,212,170,0.4) !important;
    color: #00d4aa !important;
    background: rgba(0,212,170,0.05) !important;
}

/* Override Streamlit inputs */
div[data-testid="stTextInput"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s, background 0.2s !important;
}

div[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(0,212,170,0.55) !important;
    background: rgba(0,212,170,0.04) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.08) !important;
}

div[data-testid="stTextInput"] input {
    color: #e8eaf0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.05rem !important;
    padding: 0 18px !important;
    height: 54px !important;
    
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(232,234,240,0.28) !important;
}
div[data-testid="stTextInput"] label { display: none !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4aa 0%, #0099ff 100%) !important;
    color: #080b10 !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.88rem !important;
    letter-spacing: 0.04em !important; text-transform: uppercase !important;
    height: 54px !important; padding: 0 24px !important;
    width: 100% !important;
    transition: all 0.2s !important; white-space: nowrap !important;
    display: flex; align-items: center; justify-content: center;
}

.stButton > button:hover {
    opacity: 0.88 !important; transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(0,212,170,0.28) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── DIVIDER ── */
.qm-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 48px 0 0;
}

/* ── RESULTS AREA ── */
.qm-results { padding: 36px 56px 80px; }

/* ── SECTION LABEL ── */
.qm-section-label {
    font-family: 'DM Mono', monospace; font-size: 0.74rem;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: rgba(232,234,240,0.3);
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 14px;
}
.qm-section-label::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ── AGENT GRID (8 columns) ── */
.qm-agents-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 10px; margin-bottom: 14px;
}

.qm-agent-pulse {
    display: flex; flex-direction: column;
    align-items: center; gap: 10px;
    padding: 18px 8px;
    border-radius: 12px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    font-size: 0.72rem;
    color: rgba(232,234,240,0.4);
    letter-spacing: 0.05em; text-transform: uppercase;
    text-align: center; transition: all 0.2s;
}

.qm-agent-pulse.active {
    border-color: rgba(0,212,170,0.35);
    background: rgba(0,212,170,0.06); color: #00d4aa;
}

.qm-agent-pulse.done {
    border-color: rgba(0,212,170,0.15);
    background: rgba(0,212,170,0.025); color: rgba(0,212,170,0.55);
}

.pulse-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: rgba(255,255,255,0.12);
}

.pulse-dot.active {
    background: #00d4aa;
    box-shadow: 0 0 0 4px rgba(0,212,170,0.18);
    animation: pulse-anim 1.1s ease-in-out infinite;
}

.pulse-dot.done { background: rgba(0,212,170,0.5); }

@keyframes pulse-anim {
    0%,100% { box-shadow: 0 0 0 4px rgba(0,212,170,0.18); }
    50%      { box-shadow: 0 0 0 8px rgba(0,212,170,0.05); }
}

/* ── PROGRESS BAR ── */
.qm-progress-wrap {
    height: 2px; background: rgba(255,255,255,0.05);
    border-radius: 1px; overflow: hidden; margin-bottom: 36px;
}
.qm-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #00d4aa, #0099ff);
    transition: width 0.4s ease;
}

/* ── DECISION CARD ── */
.qm-decision-card {
    background: linear-gradient(135deg,
        rgba(0,212,170,0.07) 0%,
        rgba(0,153,255,0.05) 50%,
        rgba(8,11,16,0) 100%);
    border: 1px solid rgba(0,212,170,0.18);
    border-radius: 20px; padding: 40px 44px;
    margin-bottom: 20px; position: relative; overflow: hidden;
}

.qm-decision-card::before {
    content: ''; position: absolute; top: -40%; right: -15%;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(0,212,170,0.05), transparent 60%);
    pointer-events: none;
}

.qm-decision-inner {
    display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: start;
}

.qm-decision-symbol {
    font-family: 'DM Mono', monospace; font-size: 0.8rem;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: rgba(232,234,240,0.35); margin-bottom: 12px;
}

.qm-decision-verdict {
    font-family: 'Syne', sans-serif; font-size: 4.5rem;
    font-weight: 800; letter-spacing: -0.03em; line-height: 1; margin-bottom: 10px;
}

.verdict-buy  { color: #00d4aa; }
.verdict-sell { color: #ff4d6a; }
.verdict-hold { color: #ffb400; }

.qm-confidence-wrap { margin: 22px 0; }

.qm-confidence-label {
    font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(232,234,240,0.35); margin-bottom: 9px;
    display: flex; justify-content: space-between;
}

.qm-confidence-bar {
    height: 5px; background: rgba(255,255,255,0.06);
    border-radius: 3px; overflow: hidden;
}

.qm-confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #00d4aa, #0099ff);
    border-radius: 3px;
}

.qm-badges-row {
    display: flex; gap: 12px; margin-top: 20px; flex-wrap: wrap; align-items: center;
}

.qm-sentiment-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 9px 20px; border-radius: 100px;
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem;
}

.pill-bullish { background: rgba(0,212,170,0.12); border: 1px solid rgba(0,212,170,0.28); color: #00d4aa; }
.pill-bearish { background: rgba(255,77,106,0.12); border: 1px solid rgba(255,77,106,0.28); color: #ff4d6a; }
.pill-neutral { background: rgba(255,180,0,0.12);  border: 1px solid rgba(255,180,0,0.28);  color: #ffb400; }

.qm-risk-badge {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 9px 18px; border-radius: 100px;
    font-family: 'Syne', sans-serif; font-size: 0.9rem; font-weight: 600;
}

.risk-low    { background: rgba(0,212,170,0.12); color: #00d4aa; border: 1px solid rgba(0,212,170,0.22); }
.risk-medium { background: rgba(255,180,0,0.12);  color: #ffb400; border: 1px solid rgba(255,180,0,0.22);  }
.risk-high   { background: rgba(255,77,106,0.12); color: #ff4d6a; border: 1px solid rgba(255,77,106,0.22); }

/* ── PRICE LEVEL ZONES ── */
.qm-levels-title {
    font-family: 'DM Mono', monospace; font-size: 0.74rem;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: rgba(232,234,240,0.3); margin-bottom: 16px;
}

.qm-zones { display: flex; flex-direction: column; gap: 10px; }

.qm-zone {
    display: flex; align-items: center; justify-content: space-between;
    padding: 15px 20px; border-radius: 10px;
}

.zone-resist  { background: rgba(255,77,106,0.08);  border: 1px solid rgba(255,77,106,0.18); }
.zone-current { background: rgba(0,153,255,0.08);   border: 1px solid rgba(0,153,255,0.18); }
.zone-support { background: rgba(0,212,170,0.08);   border: 1px solid rgba(0,212,170,0.18); }

.zone-label {
    font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: rgba(232,234,240,0.45);
}

.zone-value { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.1rem; }
.zone-resist  .zone-value { color: #ff4d6a; }
.zone-current .zone-value { color: #0099ff; }
.zone-support .zone-value { color: #00d4aa; }

/* ── STATS GRID ── */
.qm-stats-grid {
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: 14px; margin-bottom: 28px;
}

.qm-stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 24px 20px;
    position: relative; overflow: hidden; transition: border-color 0.2s;
}

.qm-stat-card:hover { border-color: rgba(0,212,170,0.22); }

.qm-stat-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,212,170,0.35), transparent);
}

.qm-stat-label {
    font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: rgba(232,234,240,0.35); margin-bottom: 12px;
}

.qm-stat-value {
    font-family: 'Syne', sans-serif; font-size: 1.6rem;
    font-weight: 700; color: #ffffff; letter-spacing: -0.02em; line-height: 1;
}

.qm-stat-meta { font-size: 0.72rem; color: rgba(232,234,240,0.28); margin-top: 7px; }
.qm-stat-up   { color: #00d4aa !important; }
.qm-stat-down { color: #ff4d6a !important; }

/* ── ANALYSIS CARD ── */
.qm-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 28px 30px;
    position: relative; overflow: hidden;
    transition: border-color 0.25s;
}

.qm-card:hover { border-color: rgba(255,255,255,0.14); }

.qm-card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 18px; padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.qm-card-title {
    font-family: 'Syne', sans-serif; font-size: 0.88rem;
    font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
    color: rgba(232,234,240,0.6);
    display: flex; align-items: center; gap: 10px;
}

.qm-card-icon {
    width: 30px; height: 30px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center; font-size: 0.85rem;
}

.icon-blue   { background: rgba(0,153,255,0.15); }
.icon-green  { background: rgba(0,212,170,0.15); }
.icon-amber  { background: rgba(255,180,0,0.15); }
.icon-red    { background: rgba(255,77,106,0.15); }
.icon-purple { background: rgba(167,100,255,0.15); }
.icon-cyan   { background: rgba(0,220,255,0.15); }

.qm-card-body {
    font-size: 0.9rem; line-height: 1.82;
    color: rgba(232,234,240,0.72); white-space: pre-wrap;
}

/* ── MACD VISUAL ── */
.qm-macd-visual {
    display: flex; align-items: flex-end;
    gap: 3px; height: 64px; margin: 16px 0;
}

.qm-macd-bar { flex: 1; border-radius: 2px 2px 0 0; }
.macd-pos { background: rgba(0,212,170,0.55); }
.macd-neg { background: rgba(255,77,106,0.45); border-radius: 0 0 2px 2px; }

.qm-macd-values {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 14px;
}

.qm-macd-cell {
    background: rgba(255,255,255,0.03); border-radius: 9px; padding: 12px 14px;
}

.qm-macd-cell-label {
    font-size: 0.67rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: rgba(232,234,240,0.3); margin-bottom: 5px;
}

.qm-macd-cell-val {
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.25rem;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.025) !important;
    border-radius: 12px !important; padding: 5px !important;
    gap: 4px !important; border: 1px solid rgba(255,255,255,0.07) !important;
    margin-bottom: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important; font-size: 0.82rem !important;
    letter-spacing: 0.06em !important; color: rgba(232,234,240,0.4) !important;
    border-radius: 8px !important; padding: 10px 24px !important; border: none !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,212,170,0.12) !important; color: #00d4aa !important;
}

.stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

/* ── FULL REPORT ── */
.qm-full-report {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 32px 36px;
    font-size: 0.9rem; line-height: 1.9; color: rgba(232,234,240,0.65);
    white-space: pre-wrap; font-family: 'DM Mono', monospace;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    font-family: 'DM Mono', monospace !important; font-size: 0.84rem !important;
    color: rgba(232,234,240,0.4) !important; letter-spacing: 0.08em !important;
    background: rgba(255,255,255,0.02) !important; border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── COLUMN GAPS ── */
[data-testid="column"] { padding: 0 8px !important; }
[data-testid="stHorizontalBlock"] { gap: 0 !important; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #00d4aa !important; }

/* ── CARD GAP ── */
.qm-card-gap { height: 14px; }

/* ── FOOTER ── */
.qm-footer {
    text-align: center; padding: 28px 56px;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-size: 0.74rem; color: rgba(232,234,240,0.2); letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def extract_verdict(text: str) -> str:
    t = text.upper()
    if "BUY" in t:  return "BUY"
    if "SELL" in t: return "SELL"
    return "HOLD"

def extract_confidence(text: str) -> int:
    m = re.search(r'confidence[:\s]*(\d+)', text, re.IGNORECASE)
    if m: return min(int(m.group(1)), 100)
    return 72

def extract_sentiment_type(text: str) -> str:
    t = text.upper()
    if "BULLISH" in t:  return "bullish"
    if "BEARISH" in t:  return "bearish"
    return "neutral"

def extract_risk_level(text: str) -> str:
    t = text.upper()
    if "HIGH" in t:  return "high"
    if "LOW" in t:   return "low"
    return "medium"

def safe_price(text: str, key: str) -> str:
    """Robustly extract a numeric value by key from agent text output."""
    patterns = [
        # dict repr: 'price': 376.3  or "price": 376.3
        rf"['\"]?{key}['\"]?\s*[:=]\s*\$?\s*([0-9][0-9,]*\.?[0-9]*)",
        # natural: Price: $376.30
        rf"{key}[:\s]+\$?\s*([0-9][0-9,]*\.?[0-9]*)",
        # bold markdown: **Price:** $376.30
        rf"\*\*{key}[:\*]+\s*\$?\s*([0-9][0-9,]*\.?[0-9]*)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).replace(",", "")
            try:
                return f"${float(val):,.2f}"
            except:
                pass
    return "—"

def safe_volume(text: str) -> str:
    m = re.search(r"volume['\"]?\s*[:=]\s*([0-9,]+)", text, re.IGNORECASE)
    if m:
        try:
            return f"{int(m.group(1).replace(',',''))  :,}"
        except:
            pass
    return "—"

def safe_rsi(text: str) -> str:
    # Try: RSI … 48.92
    for pat in [
        r"RSI[^\d]{0,40}([3-9]\d\.\d+)",
        r"approximately\s+([3-9]\d\.\d+)",
        r"RSI.*?(\d{2,3}\.\d+)",
        r"(\d{2,3}\.\d+).*?RSI",
    ]:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            try:
                v = float(m.group(1))
                if 0 < v < 100:
                    return f"{v:.1f}"
            except:
                pass
    return "—"

def card(title: str, icon: str, icon_class: str, body: str):
    st.markdown(f"""
    <div class="qm-card">
        <div class="qm-card-header">
            <div class="qm-card-title">
                <div class="qm-card-icon {icon_class}">{icon}</div>
                {title}
            </div>
        </div>
        <div class="qm-card-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── STATE INITIALIZATION ──────────────────────────────────────────────────────
if "symbol" not in st.session_state:
    st.session_state.symbol = ""
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# ─── NAV ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="qm-nav">
    <div class="qm-logo">
        <div class="qm-logo-icon">◈</div>
        QuantMind AI
    </div>
    <div class="qm-nav-badge">Multi-Agent Engine v2</div>
</div>
""", unsafe_allow_html=True)


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="qm-hero">
    <div class="qm-eyebrow">AI-Powered Stock Intelligence</div>
    <h1 class="qm-headline">Research any stock<br>with <em>institutional precision</em></h1>
    <div class="qm-sublines-wrap">
        <p class="qm-subline">Seven specialised AI agents analyse market data, technicals,
        fundamentals, news, sentiment, price levels and MACD in parallel —
        delivering one unified decision.</p>
        <p class="qm-subline">Seven specialised AI agents analyse market data, technicals,
        fundamentals, news, sentiment, price levels and MACD in parallel —
        delivering one unified decision.</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── INPUT ROW — centred with equal left/right margins ───────────────────────
_, mid, _ = st.columns([1, 2.8, 1])
with mid:
    inp_c, btn_c = st.columns([4.2, 1])
    with inp_c:
        symbol_input = st.text_input(
            "ticker",
            value=st.session_state.symbol,
            placeholder="Enter ticker symbol — e.g. AAPL, TSLA, NVDA",
            label_visibility="collapsed",
            key="ticker_input"
        )
    with btn_c:
        run_btn = st.button("Analyse →", use_container_width=True)

    # Update session state symbol if typed and Enter pressed
    if symbol_input != st.session_state.symbol:
        st.session_state.symbol = symbol_input
        st.session_state.run_analysis = True

    # ─── CHIPS ROW ───
    chips = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "NFLX"]
    st.markdown('<div class="qm-chips-container">', unsafe_allow_html=True)
    chip_cols = st.columns(len(chips))
    for i, chip in enumerate(chips):
        with chip_cols[i]:
            if st.button(chip, key=f"chip_{chip}"):
                st.session_state.symbol = chip
                st.session_state.run_analysis = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)




# ─── PIPELINE ─────────────────────────────────────────────────────────────────
if (run_btn or st.session_state.run_analysis) and st.session_state.symbol:
    # Reset trigger
    st.session_state.run_analysis = False
    symbol = st.session_state.symbol.strip().upper()
    st.markdown('<hr class="qm-divider">', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="qm-results">', unsafe_allow_html=True)

        agents_meta = [
            ("📈", "Market",       "price & vol"),
            ("📉", "Technical",    "RSI"),
            ("🏦", "Fundamental",  "PE · EPS"),
            ("📰", "News",         "headlines"),
            ("💬", "Sentiment",    "NLP"),
            ("⚡", "Quant",        "S/R levels"),
            ("🔀", "MACD",         "trend"),
            ("🧠", "Decision",     "verdict"),
        ]

        agent_ph = st.empty()
        prog_ph  = st.empty()

        def render_agents(done: int):
            html = '<div class="qm-agents-grid">'
            for i, (icon, name, sub) in enumerate(agents_meta):
                if i < done:     cls, dot = "done",   "done"
                elif i == done:  cls, dot = "active", "active"
                else:            cls, dot = "",       ""
                html += f"""
                <div class="qm-agent-pulse {cls}">
                    <div class="pulse-dot {dot}"></div>
                    <div style="font-size:0.78rem;">{icon} {name}</div>
                    <div style="font-size:0.62rem;opacity:0.5;">{sub}</div>
                </div>"""
            html += "</div>"
            agent_ph.markdown(html, unsafe_allow_html=True)
            pct = int((done / len(agents_meta)) * 100)
            prog_ph.markdown(f"""
            <div class="qm-progress-wrap">
                <div class="qm-progress-fill" style="width:{pct}%"></div>
            </div>""", unsafe_allow_html=True)

        render_agents(0)

        try:
            from pipelines import run_pipeline

            status_ph = st.empty()
            status_ph.markdown(
                '<div style="text-align:center;font-size:0.82rem;'
                'color:rgba(232,234,240,0.26);letter-spacing:0.12em;'
                'text-transform:uppercase;padding:4px 0 28px;">'
                'Initialising agents…</div>',
                unsafe_allow_html=True
            )

            with st.spinner(""):
                state = run_pipeline(symbol)

            render_agents(8)
            status_ph.empty()

            # ── Unpack state ──────────────────────────────────────────
            market_text = state.get("market", "")
            tech_text   = state.get("technical", "")
            levels      = state.get("levels", {})
            macd_data   = state.get("macd", {})
            sma         = state.get("sma", "—")

            # ── Stat values — prefer structured levels dict, fall back to text parse
            cp = levels.get("current_price")
            price_val = f"${cp:,.2f}" if cp else safe_price(market_text, "price")
            high_val  = safe_price(market_text, "high")
            low_val   = safe_price(market_text, "low")
            vol_val   = safe_volume(market_text)
            rsi_raw   = safe_rsi(tech_text)

            try:    rsi_f = float(rsi_raw)
            except: rsi_f = None
            rsi_zone = ("Overbought" if rsi_f and rsi_f > 70 else
                        "Oversold"   if rsi_f and rsi_f < 30 else "Neutral zone")

            try:
                macd_f  = float(macd_data.get("macd", 0))
                sig_f   = float(macd_data.get("signal", 0))
                macd_color = "qm-stat-up" if macd_f >= 0 else "qm-stat-down"
                macd_disp  = f"{macd_f:+.2f}"
                sig_disp   = f"{sig_f:+.2f}"
            except:
                macd_f = sig_f = 0.0
                macd_color = ""
                macd_disp  = str(macd_data.get("macd", "—"))
                sig_disp   = str(macd_data.get("signal", "—"))

            verdict    = extract_verdict(state.get("final_decision", ""))
            confidence = extract_confidence(state.get("final_decision", ""))
            sentiment  = extract_sentiment_type(state.get("sentiment", ""))
            risk_lvl   = extract_risk_level(state.get("risk", ""))

            verdict_class  = f"verdict-{verdict.lower()}"
            pill_class     = f"pill-{sentiment}"
            risk_class     = f"risk-{risk_lvl}"
            s_icon = {"bullish": "↑", "bearish": "↓", "neutral": "→"}.get(sentiment, "→")
            r_icon = {"high": "⚠", "medium": "◉", "low": "✓"}.get(risk_lvl, "◉")

            # ── DECISION HERO CARD ────────────────────────────────────
            st.markdown(f"""
            <div class="qm-decision-card">
                <div class="qm-decision-inner">
                    <div>
                        <div class="qm-decision-symbol">AI Final Decision · {symbol}</div>
                        <div class="qm-decision-verdict {verdict_class}">{verdict}</div>
                        <div class="qm-confidence-wrap">
                            <div class="qm-confidence-label">
                                <span>Confidence</span>
                                <span>{confidence}%</span>
                            </div>
                            <div class="qm-confidence-bar">
                                <div class="qm-confidence-fill" style="width:{confidence}%"></div>
                            </div>
                        </div>
                        <div class="qm-badges-row">
                            <div class="qm-sentiment-pill {pill_class}">{s_icon} {sentiment.capitalize()}</div>
                            <div class="qm-risk-badge {risk_class}">{r_icon} {risk_lvl.capitalize()} Risk</div>
                        </div>
                    </div>
                    <div>
                        <div class="qm-levels-title">Price Levels</div>
                        <div class="qm-zones">
                            <div class="qm-zone zone-resist">
                                <span class="zone-label">Resistance</span>
                                <span class="zone-value">${levels.get('resistance', '—')}</span>
                            </div>
                            <div class="qm-zone zone-current">
                                <span class="zone-label">Current</span>
                                <span class="zone-value">${levels.get('current_price', '—')}</span>
                            </div>
                            <div class="qm-zone zone-support">
                                <span class="zone-label">Support</span>
                                <span class="zone-value">${levels.get('support', '—')}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── STAT CARDS ────────────────────────────────────────────
            st.markdown(f"""
            <div class="qm-stats-grid">
                <div class="qm-stat-card">
                    <div class="qm-stat-label">Last Price</div>
                    <div class="qm-stat-value">{price_val}</div>
                    <div class="qm-stat-meta">{symbol} · live</div>
                </div>
                <div class="qm-stat-card">
                    <div class="qm-stat-label">Session High</div>
                    <div class="qm-stat-value qm-stat-up">{high_val}</div>
                    <div class="qm-stat-meta">Daily range top</div>
                </div>
                <div class="qm-stat-card">
                    <div class="qm-stat-label">Session Low</div>
                    <div class="qm-stat-value qm-stat-down">{low_val}</div>
                    <div class="qm-stat-meta">Daily range bottom</div>
                </div>
                <div class="qm-stat-card">
                    <div class="qm-stat-label">RSI (14)</div>
                    <div class="qm-stat-value">{rsi_raw}</div>
                    <div class="qm-stat-meta">{rsi_zone}</div>
                </div>
                <div class="qm-stat-card">
                    <div class="qm-stat-label">MACD</div>
                    <div class="qm-stat-value {macd_color}">{macd_disp}</div>
                    <div class="qm-stat-meta">Signal: {sig_disp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── TABS ──────────────────────────────────────────────────
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊  Analysis",
                "📰  News & Sentiment",
                "⚡  Quant Strategy",
                "📋  Full Report",
            ])

            with tab1:
                c1, c2 = st.columns([3, 2])
                with c1:
                    card("Market Data", "📈", "icon-blue", state.get("market", "No data."))
                    st.markdown('<div class="qm-card-gap"></div>', unsafe_allow_html=True)
                    card("Fundamental Analysis", "🏦", "icon-amber", state.get("fundamental", "No data."))
                    st.markdown('<div class="qm-card-gap"></div>', unsafe_allow_html=True)
                    card("Risk Analysis", "⚠️", "icon-red", state.get("risk", "No data."))
                with c2:
                    card("Technical Indicators", "📉", "icon-green", state.get("technical", "No data."))
                    st.markdown('<div class="qm-card-gap"></div>', unsafe_allow_html=True)

                    # MACD bar visual
                    heights  = [14, 10, 20, 13, 26, 16, 32, 20, 40, 28]
                    bar_cls  = ["macd-pos","macd-neg","macd-pos","macd-neg","macd-pos",
                                "macd-pos","macd-neg","macd-pos","macd-pos","macd-neg"]
                    bars_html = "".join(
                        f'<div class="qm-macd-bar {bc}" style="height:{h}px;opacity:0.42;"></div>'
                        for h, bc in zip(heights, bar_cls)
                    )
                    live_col = "macd-pos" if macd_f >= 0 else "macd-neg"
                    live_h   = max(12, min(64, int(abs(macd_f) * 6 + 22)))
                    bars_html += f'<div class="qm-macd-bar {live_col}" style="height:{live_h}px;opacity:1;flex:2;"></div>'

                    st.markdown(f"""
                    <div class="qm-card">
                        <div class="qm-card-header">
                            <div class="qm-card-title">
                                <div class="qm-card-icon icon-cyan">🔀</div>
                                MACD Trend
                            </div>
                        </div>
                        <div class="qm-macd-visual">{bars_html}</div>
                        <div class="qm-macd-values">
                            <div class="qm-macd-cell">
                                <div class="qm-macd-cell-label">MACD Line</div>
                                <div class="qm-macd-cell-val" style="color:{'#00d4aa' if macd_f>=0 else '#ff4d6a'}">
                                    {macd_f:+.2f}
                                </div>
                            </div>
                            <div class="qm-macd-cell">
                                <div class="qm-macd-cell-label">Signal Line</div>
                                <div class="qm-macd-cell-val" style="color:{'#00d4aa' if sig_f>=0 else '#ff4d6a'}">
                                    {sig_f:+.2f}
                                </div>
                            </div>
                        </div>
                        <div style="margin-top:14px;font-size:0.78rem;color:rgba(232,234,240,0.35);">
                            SMA (20) &mdash; <span style="color:rgba(232,234,240,0.65);">${sma}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with tab2:
                c1, c2 = st.columns([3, 2])
                with c1:
                    card("Latest News", "📰", "icon-blue", state.get("news", "No news."))
                with c2:
                    card("Sentiment Analysis", "💬", "icon-green",
                         state.get("sentiment", "No sentiment data."))

            with tab3:
                c1, c2 = st.columns([1, 1])
                with c1:
                    card("Quant Price Strategy", "⚡", "icon-purple",
                         state.get("price_strategy", "No strategy."))
                with c2:
                    card("Basic Decision Model", "🧮", "icon-amber",
                         state.get("decision", "No decision."))
                st.markdown('<div class="qm-card-gap"></div>', unsafe_allow_html=True)
                card("AI Conflict Resolution & Final Decision", "🧠", "icon-cyan",
                     state.get("final_decision", "No final decision."))

            with tab4:
                st.markdown(
                    '<div class="qm-section-label">Refined full report</div>',
                    unsafe_allow_html=True
                )
                with st.expander("◈  View complete AI-refined report", expanded=True):
                    st.markdown(
                        f'<div class="qm-full-report">'
                        f'{state.get("final", "Report not generated.")}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        except ImportError as e:
            st.error(f"Pipeline import error: {e}")
        except Exception as e:
            st.error(f"Analysis error: {e}")
            import traceback
            st.code(traceback.format_exc())

        st.markdown("</div>", unsafe_allow_html=True)

elif run_btn and not symbol_input:
    st.warning("Please enter a ticker symbol before running.")


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="qm-footer">
    ◈ QuantMind AI — Multi-Agent Finance Engine &nbsp;·&nbsp;
    LangChain · MistralAI · Tavily · Alpha Vantage · yFinance &nbsp;·&nbsp;
    For informational purposes only — not financial advice.
</div>
""", unsafe_allow_html=True)
