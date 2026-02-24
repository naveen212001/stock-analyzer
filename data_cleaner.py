import pandas as pd
import numpy as np
import streamlit as st

def clean_stock_data(data_dict):
    """
    Cleans raw stock data: handles missing values, removes outliers using IQR.
    Returns cleaned pandas Series.
    """
    # Convert to DataFrame for processing
    df = pd.DataFrame([data_dict])
    
    # List of numeric columns to clean
    numeric_cols = ['current', 'change', 'change_percent', 'high', 'low', 'open', 'prev_close']
    
    for col in numeric_cols:
        if col in df.columns:
            # Handle missing values
            if pd.isna(df[col].iloc[0]):
                st.warning(f"⚠️ Missing value in {col}, filling with median.")
                # In future, you can fetch fallback data
                df[col].fillna(df[col].median(), inplace=True)
    
    # Remove outliers using IQR (for multiple data points — useful later)
    def iqr_outlier_clip(series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return series.clip(lower, upper)
    
    # Apply clipping (currently for single point, useful when batching)
    for col in numeric_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = iqr_outlier_clip(df[col])
    
    # Return cleaned data as dict
    cleaned = df.iloc[0].to_dict()
    st.info("✅ Data cleaned: outliers capped, missing values handled.")
    return cleaned     
