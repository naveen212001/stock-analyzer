import streamlit as st
import requests

def analyze(ticker, data):
    st.header(f"🚀 Growth Analysis: {ticker}")
    
    # Fetch detailed financials from Finnhub
    API_KEY = st.secrets["FINNHUB_API_KEY"]
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            metrics = response.json().get("metric", {})
            
            # Key Growth Metrics
            revenue_growth = metrics.get("revenueGrowthYear")
            eps_growth = metrics.get("epsGrowth5Y")
            roe = metrics.get("roe")
            ebitda_growth = metrics.get("ebitdaGrowthYoy")
            net_income_growth = metrics.get("netIncomeGrowthYoy")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Revenue Growth (YoY)", f"{revenue_growth:.2f}%" if revenue_growth else "N/A")
                st.metric("EPS Growth (5Y)", f"{eps_growth:.2f}%" if eps_growth else "N/A")
                st.metric("EBITDA Growth (YoY)", f"{ebitda_growth:.2f}%" if ebitda_growth else "N/A")
            
            with col2:
                st.metric("Net Income Growth (YoY)", f"{net_income_growth:.2f}%" if net_income_growth else "N/A")
                st.metric("ROE", f"{roe:.2f}%" if roe else "N/A")
                st.metric("Prev Close", f"${data['prev_close']:.2f}")
            
            # Interpretation
            st.markdown("### 📌 Interpretation")
            if revenue_growth and revenue_growth > 10:
                st.success("✅ Strong revenue growth — key for growth stocks.")
            if eps_growth and eps_growth > 15:
                st.success("✅ High EPS growth — earnings momentum.")
            if roe and roe > 15:
                st.success("✅ High ROE — efficient use of equity.")
            if ebitda_growth and ebitda_growth < 0:
                st.warning("⚠️ Declining EBITDA — monitor profitability.")
                  
