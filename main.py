import streamlit as st
import importlib
import json
from datetime import datetime, timedelta
import pytz

# Import custom modules
from data_fetcher import fetch_stock_quote
from data_cleaner import clean_stock_data

# App Title
st.title("📊 Stock Analyzer")
st.markdown("A trust-first tool for retail investors — clean data, no noise.")

def search_symbols(query):
    API_KEY = st.secrets["FINNHUB_API_KEY"]
    url = f"https://finnhub.io/api/v1/search?q={query}&token={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [item["symbol"] for item in data["result"] if item["type"] == "Common Stock"]
    except Exception as e:
        st.error(f"Search failed: {e}")
    return []   
query = st.sidebar.text_input("Search Stock", "").upper()
if query:
    symbols = search_symbols(query)
    if symbols:
        ticker = st.sidebar.selectbox("Matches", options=symbols)
    else:
        st.sidebar.warning("No matches found")       

  

# Load Tier Config
@st.cache_data
def load_tiers():
    return {
        "value": {"name": "Value", "module": "tiers.value", "desc": "Undervalued stocks based on fundamentals"},
        "growth": {"name": "Growth", "module": "tiers.growth", "desc": "High revenue and earnings growth potential"}
    }

TIER_CONFIG = load_tiers()

# User Inputs
st.sidebar.header("🔍 Select Stock & Analysis Tier")

# Stock Input
ticker = st.sidebar.selectbox(
    "Select Stock",
    options=get_stock_symbols(),
    index=None,
    placeholder="Choose a stock..."
)       

# Tier Selection
tier_key = st.sidebar.selectbox(
    "Choose Analysis Type",
    options=list(TIER_CONFIG.keys()),
    format_func=lambda x: TIER_CONFIG[x]["name"]
)


# Display selected tier description
st.sidebar.info(TIER_CONFIG[tier_key]["desc"])

# Analyze Button
if st.sidebar.button("Analyze"):
    if not ticker:
        st.error("⚠️ Please enter a valid stock symbol.")
    else:
        with st.spinner(f"Fetching fresh data for {ticker}..."):

            # Step 1: Fetch raw data
            raw_data = fetch_stock_quote(ticker)
            if not raw_data:
                st.stop()

            # Step 2: Clean data
            cleaned_data = clean_stock_data(raw_data)

            # Step 3: Run selected tier analysis
            st.success(f"✅ Fresh, clean data ready. Running {TIER_CONFIG[tier_key]['name']} analysis...")
            try:
                module = importlib.import_module(TIER_CONFIG[tier_key]["module"])
                module.analyze(ticker, cleaned_data)
            except Exception as e:
                st.error(f"❌ Error in analysis: {e}")
else:
    st.info("👈 Select a stock and analysis tier from the sidebar to begin.")   
