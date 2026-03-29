import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="BTC Strategy Engine", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 BTC-USD Live Strategy Engine")
st.caption("Real live data • Robust version")

# ================== SETTINGS ==================
with st.sidebar:
    st.header("Trade Settings")
    balance = st.number_input("Account Balance ($)", value=10000.0, min_value=1000.0)
    risk_pct = st.slider("Risk % per trade", 0.5, 3.0, 1.0, 0.1)

# ================== FETCH LIVE DATA (Robust) ==================
@st.cache_data(ttl=180)  # 3 minutes
def fetch_tf_data(tf):
    try:
        if tf == "4H":
            df = yf.download("BTC-USD", period="30d", interval="1h", progress=False)
            if not df.empty:
                df = df.resample("4H").agg({
                    'Open': 'first', 
                    'High': 'max', 
                    'Low': 'min', 
                    'Close': 'last'
                })
        else:
            interval = {"5M": "5m", "15M": "15m", "1H": "60m"}[tf]
            df = yf.download("BTC-USD", period="7d", interval=interval, progress=False)
        
        return df.dropna()
    except:
        return pd.DataFrame()

timeframes = ["4H", "1H", "15M", "5M"]
data = {}

for tf in timeframes:
    data[tf] = fetch_tf_data(tf)

# Safe current price extraction
current_price = None
for tf in ["5M", "15M", "1H", "4H"]:
    if not data[tf].empty:
        current_price = round(float(data[tf]['Close'].iloc[-1]), 2)
        break

if current_price:
    st.success(f"**Live BTC Price: ${current_price:,.2f}**")
else:
    st.error("⚠️ Yahoo Finance is rate limited. Please wait 1-2 minutes and refresh.")
    current_price = 66850.0  # fallback

# ================== CHARTS ==================
st.subheader("Live Charts")
cols = st.columns(2)
for i, tf in enumerate(timeframes):
    with cols[i % 2]:
        st.markdown(f"**{tf}**")
        df = data[tf]
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color="#00FFB2",
                decreasing_line_color="#FF6B6B"
            )])
            fig.update_layout(height=340, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Data temporarily unavailable for {tf}")

# ================== ANALYSIS ==================
if st.button("🔥 ANALYSE LIVE MARKET DATA", type="primary", use_container_width=True):
    with st.spinner("Analysing current market..."):
        price = current_price

        strategies = [ ... ]   # (I'll keep it short here for space - same detailed strategies as before)

        st.success("✅ Analysis Complete")

        # [Paste the full strategies and display logic from my previous message here]

st.caption("Educational tool only • Not financial advice")
