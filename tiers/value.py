import streamlit as st
import requests

def analyze(ticker, data):
    st.header(f"🔍 Value Analysis: {ticker}")
    
    # Fetch detailed financials from Finnhub
    API_KEY = st.secrets["FINNHUB_API_KEY"]
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            metrics = response.json().get("metric", {})
            
            # Key Value Metrics
            pe = metrics.get("peBasicExclExtraTTM")
            pb = metrics.get("pb")
            div_yield = metrics.get("dividendYield")
            roe = metrics.get("roe")
            debt_equity = metrics.get("debtEquity")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("P/E Ratio", f"{pe:.2f}" if pe else "N/A")
                st.metric("P/B Ratio", f"{pb:.2f}" if pb else "N/A")
                st.metric("Dividend Yield", f"{div_yield:.2f}%" if div_yield else "N/A")
            
            with col2:
                st.metric("ROE", f"{roe:.2f}%" if roe else "N/A")
                st.metric("Debt/Equity", f"{debt_equity:.2f}" if debt_equity else "N/A")
                st.metric("Prev Close", f"${data['prev_close']:.2f}")
            
            # Interpretation
            st.markdown("### 📌 Interpretation")
            if pe and pe < 15:
                st.success("✅ Low P/E suggests undervaluation.")
            if pb and pb < 1.5:
                st.success("✅ Low P/B suggests asset-rich undervaluation.")
            if div_yield and div_yield > 0.03:
                st.success("✅ High dividend yield — income-friendly.")
            if debt_equity and debt_equity > 2:
                st.warning("⚠️ High debt — monitor financial health.")
                
        else:
            st.error("❌ Could not fetch financial metrics.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")   
