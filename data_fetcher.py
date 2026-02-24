import requests
import streamlit as st
from datetime import datetime, timedelta
import pytz

# Fetch real-time stock quote from Finnhub
def fetch_stock_quote(ticker):
    API_KEY = st.secrets["FINNHUB_API_KEY"]
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Check if data is fresh (<24h)
            if is_data_fresh(data.get("t", 0)):
                return {
                    "current": data["c"],
                    "change": data["d"],
                    "change_percent": data["dp"],
                    "high": data["h"],
                    "low": data["l"],
                    "open": data["o"],
                    "prev_close": data["pc"],
                    "timestamp": data["t"]
                }
            else:
                st.warning("📉 Data is older than 24 hours — skipping.")
                return None
        else:
            st.error(f"❌ API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"⚠️ Connection failed: {e}")
        return None

# Check if data is less than 24 hours old (UTC)
def is_data_fresh(api_timestamp):
    now_utc = datetime.now(pytz.UTC)
    data_time = datetime.fromtimestamp(api_timestamp, pytz.UTC)
    return now_utc - data_time < timedelta(hours=24)   
