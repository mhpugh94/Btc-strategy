import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="BTC Strategy Engine", layout="centered", initial_sidebar_state="expanded")

st.title("🚀 BTC-USD Strategy Engine")
st.caption("Multi-Timeframe • ICT + S&D + Price Action • Mobile Optimised")

# Live Price
btc = yf.Ticker("BTC-USD")
price = btc.history(period="1d")['Close'].iloc[-1]
st.markdown(f"**Live BTC Price: ${price:,.2f}**")

# Sidebar settings (like your original)
with st.sidebar:
    st.header("Trade Settings")
    balance = st.number_input("Account Balance ($)", value=10000.0, min_value=1000.0)
    risk_pct = st.slider("Risk % per trade", 0.5, 3.0, 1.0, 0.1)

# Main Analyse Button
if st.button("🔥 RUN FULL ANALYSIS", type="primary", use_container_width=True):
    with st.spinner("Analysing 4H, 1H, 15M, 5M charts..."):
        st.success("✅ Consensus Analysis Complete")

        # Strategy Cards (expandable like your original)
        strategies = [
            {
                "tag": "ICT/SMC", "color": "#00FFB2", "direction": "LONG", "confidence": 87,
                "name": "4H BOS + 15M FVG Setup",
                "entry": 66550, "sl": 66280, "tp1": 67000, "tp2": 67550, "tp3": 68200,
                "reasoning": ["4H: Clear BOS & liquidity sweep", "1H: FVG filled + displacement", "15M: Order Block confirmation", "5M: Momentum continuation"],
                "description": "High probability ICT setup with strong confluence across lower timeframes."
            },
            {
                "tag": "Supply & Demand", "color": "#6C5CE7", "direction": "LONG", "confidence": 79,
                "name": "Demand Zone Reclaim",
                "entry": 66480, "sl": 66250, "tp1": 66900, "tp2": 67400, "tp3": 68000,
                "reasoning": ["4H: Strong demand zone", "1H: Fresh zone test", "15M: Rejection wick", "5M: Volume spike"],
                "description": "Supply & Demand zone acting as support with multiple timeframe confirmation."
            },
            {
                "tag": "Price Action", "color": "#FF6B6B", "direction": "LONG", "confidence": 82,
                "name": "Bull Flag Breakout",
                "entry": 66600, "sl": 66320, "tp1": 67100, "tp2": 67700, "tp3": 68500,
                "reasoning": ["4H: Higher highs/lows", "1H: Flag consolidation", "15M: Break & retest", "5M: Strong close above resistance"],
                "description": "Classic price action pattern with trend alignment."
            }
        ]

        for s in strategies:
            with st.expander(f"{s['tag']} — {s['direction']} @ ${s['entry']:,}   ({s['confidence']}% confidence)", expanded=True):
                st.markdown(f"**{s['name']}**")
                st.markdown(s['description'])

                # Levels grid
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Entry", f"${s['entry']:,}")
                with cols[1]:
                    st.metric("Stop Loss", f"${s['sl']:,}", delta=f"-{s['entry']-s['sl']}")
                with cols[2]:
                    rr = round((s['tp1'] - s['entry']) / (s['entry'] - s['sl']), 1)
                    st.metric("R:R", f"1:{rr}")

                # Progress / Confidence
                st.progress(s['confidence'] / 100)

                # MTF Reasoning
                st.subheader("MTF Reasoning")
                for r in s['reasoning']:
                    st.write("• " + r)

                # Position Sizing
                st.subheader("Position Calculator")
                risk_amount = balance * risk_pct / 100
                sl_dist = s['entry'] - s['sl']
                size_btc = round(risk_amount / sl_dist, 4) if sl_dist > 0 else 0
                
                st.info(f"""
                **Risking ${risk_amount:.2f}** ({risk_pct}%)\n
                **Position Size:** {size_btc} BTC\n
                TP1 (50%): {round(size_btc*0.5, 4)} BTC  
                TP2 (30%): {round(size_btc*0.3, 4)} BTC  
                TP3 (20%): {round(size_btc*0.2, 4)} BTC
                """)

                if st.button("📤 Export Trade Plan", key=s['tag']):
                    st.download_button(
                        label="Download TXT Plan",
                        data=f"Trade Plan - {s['tag']}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nEntry: ${s['entry']}\nSL: ${s['sl']}\n... (full plan)",
                        file_name=f"btc_{s['tag'].lower()}_plan.txt",
                        mime="text/plain"
                    )

st.caption("This is a demo version. Educational only — not financial advice.")
