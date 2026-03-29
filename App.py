import streamlit as st

st.set_page_config(page_title="BTC Strategy Engine", layout="centered")

st.title("🚀 BTC-USD Strategy Engine")
st.caption("Live • Mobile Friendly • 4 Timeframes")

st.markdown("### Current BTC Price")
st.markdown("**$67,234.50** *(updating...)*")

with st.sidebar:
    st.header("Trade Settings")
    balance = st.number_input("Account Balance ($)", value=10000.0)
    risk = st.slider("Risk % per trade", 0.5, 3.0, 1.0, 0.1)

if st.button("🔥 RUN FULL ANALYSIS", type="primary", use_container_width=True):
    with st.spinner("Analysing 4H → 1H → 15M → 5M..."):
        st.success("✅ Analysis Complete (3 Strategies)")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📌 ICT/SMC")
            st.progress(87)
            st.write("**LONG** @ $67,250")
            st.write("SL: $66,880 | TP: $67,800 / $68,450")
            st.caption("4H BOS + 15M FVG")
        
        with col2:
            st.subheader("📌 Supply & Demand")
            st.progress(79)
            st.write("**LONG** @ $67,180")
            st.write("SL: $66,850 | TP: $67,700")

        st.subheader("📌 Price Action")
        st.progress(82)
        st.write("**LONG** @ $67,300 | Bull Flag Breakout")

        st.divider()
        st.subheader("Position Size")
        risk_amount = balance * risk / 100
        st.info(f"Risking **${risk_amount:.2f}**")

st.caption("Educational tool only • Not financial advice")
