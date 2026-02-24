import streamlit as st
import importlib
import json
from datetime import datetime, timedelta
import pytz

# App Title
st.title("📊 Stock Analyzer")
st.markdown("A trust-first tool for retail investors — clean data, no noise.")

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

# Stock Input (Text for now — later we'll populate from Finnhub)
ticker = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL)", "").upper()

# Tier Selection
tier_key = st.sidebar.selectbox(
    "Choose Analysis Type",
    options=list(TIER_CONFIG.keys()),
    format_func=lambda x: TIER_CONFIG[x]["name"]
)

# Display selected tier description
st.sidebar.info(TIER_CONFIG[tier_key]["desc"])

# UTC Time Check (Data must be <24h old)
def is_data_fresh(api_timestamp):
    now_utc = datetime.now(pytz.UTC)
    data_time = datetime.fromtimestamp(api_timestamp, pytz.UTC)
    return now_utc - data_time < timedelta(hours=24)

# Analyze Button
if st.sidebar.button("Analyze"):
    if not ticker:
        st.error("⚠️ Please enter a valid stock symbol.")
    else:
        with st.spinner(f"Fetching fresh data for {ticker}..."):
            # Simulate data fetch (will be replaced by real API call)
            mock_data = {
                "t": int(datetime.now(pytz.UTC).timestamp()),  # Simulate current UTC timestamp
                "c": 150.25,  # current price
                "pc": 148.70  # previous close
            }

            # Check data freshness
            if not is_data_fresh(mock_data["t"]):
                st.warning("📉 Data is older than 24 hours — skipping analysis.")
            else:
                st.success(f"✅ Fresh data confirmed for {ticker}. Running {TIER_CONFIG[tier_key]['name']} analysis...")

                # Dynamic Tier Loading
                try:
                    module = importlib.import_module(TIER_CONFIG[tier_key]["module"])
                    module.analyze(ticker, mock_data)  # Pass data to tier module
                except ModuleNotFoundError:
                    st.error(f"🔧 Module for {TIER_CONFIG[tier_key]['name']} not found.")
                except Exception as e:
                    st.error(f"❌ Error in analysis: {e}")
else:
    st.info("👈 Select a stock and analysis tier from the sidebar to begin.")   
