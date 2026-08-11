import os
import pandas as pd
import duckdb

DATASET_PATH = os.path.join(os.path.dirname(__file__), "Dataset", "zepto_v1.csv")

def read_csv_safe(path):
    """Safely reads CSV with multiple encoding fallbacks."""
    encodings = ['utf-8', 'latin1', 'cp1252', 'utf-8-sig']
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except (UnicodeDecodeError, Exception):
            continue
    # Ultimate fallback with error replacement
    return pd.read_csv(path, encoding='utf-8', encoding_errors='replace')

def get_connection():
    """Returns a DuckDB in-memory database connection with `zepto` table pre-loaded."""
    conn = duckdb.connect(database=':memory:')
    if os.path.exists(DATASET_PATH):
        df = read_csv_safe(DATASET_PATH)
        # Ensure column compatibility with SQL queries
        if 'discountedSellingPrice' in df.columns and 'discountSellingPrice' not in df.columns:
            df['discountSellingPrice'] = df['discountedSellingPrice']
        
        # Clean string columns
        if 'category' in df.columns:
            df['category'] = df['category'].astype(str).str.strip()
        if 'name' in df.columns:
            df['name'] = df['name'].astype(str).str.strip()
            
        # Ensure boolean outOfStock
        if 'outOfStock' in df.columns:
            df['outOfStock'] = df['outOfStock'].astype(str).str.upper().map({'TRUE': True, 'FALSE': False, '1': True, '0': False}).fillna(False)

        # Register dataframe as 'zepto' table in DuckDB
        conn.register('zepto', df)
    return conn

def load_data():
    """Loads dataset into Pandas DataFrame."""
    if os.path.exists(DATASET_PATH):
        df = read_csv_safe(DATASET_PATH)
        if 'discountedSellingPrice' in df.columns and 'discountSellingPrice' not in df.columns:
            df['discountSellingPrice'] = df['discountedSellingPrice']
        if 'category' in df.columns:
            df['category'] = df['category'].astype(str).str.strip()
        if 'name' in df.columns:
            df['name'] = df['name'].astype(str).str.strip()
        if 'outOfStock' in df.columns:
            df['outOfStock'] = df['outOfStock'].astype(str).str.upper().map({'TRUE': True, 'FALSE': False, '1': True, '0': False}).fillna(False)
        return df
    return pd.DataFrame()
