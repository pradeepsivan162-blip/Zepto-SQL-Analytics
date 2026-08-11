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

def process_dataframe(df):
    """Normalizes column names and data types for seamless SQL and Streamlit usage."""
    if df.empty:
        return df

    # Map column names case-insensitively
    rename_map = {}
    for col in df.columns:
        c_clean = str(col).strip()
        c_lower = c_clean.lower()
        if c_lower == 'category':
            rename_map[col] = 'category'
        elif c_lower == 'name':
            rename_map[col] = 'name'
        elif c_lower == 'mrp':
            rename_map[col] = 'mrp'
        elif c_lower in ['discountpercent', 'discount_percent']:
            rename_map[col] = 'discountPercent'
        elif c_lower in ['availablequantity', 'available_quantity']:
            rename_map[col] = 'availableQuantity'
        elif c_lower in ['discountedsellingprice', 'discountsellingprice']:
            rename_map[col] = 'discountedSellingPrice'
        elif c_lower in ['weightingms', 'weight_in_gms']:
            rename_map[col] = 'weightInGms'
        elif c_lower in ['outofstock', 'out_of_stock']:
            rename_map[col] = 'outOfStock'
        elif c_lower == 'quantity':
            rename_map[col] = 'quantity'
        else:
            rename_map[col] = c_clean

    df = df.rename(columns=rename_map)

    # Ensure dual availability of discountSellingPrice / discountedSellingPrice for legacy SQL queries
    if 'discountedSellingPrice' in df.columns and 'discountSellingPrice' not in df.columns:
        df['discountSellingPrice'] = df['discountedSellingPrice']

    # Clean string values
    if 'category' in df.columns:
        df['category'] = df['category'].astype(str).str.strip()
    if 'name' in df.columns:
        df['name'] = df['name'].astype(str).str.strip()

    # Clean boolean outOfStock
    if 'outOfStock' in df.columns:
        df['outOfStock'] = df['outOfStock'].astype(str).str.upper().map(
            {'TRUE': True, 'FALSE': False, '1': True, '0': False}
        ).fillna(False)

    return df

def get_connection():
    """Returns a DuckDB in-memory database connection with `zepto` table pre-loaded."""
    conn = duckdb.connect(database=':memory:')
    if os.path.exists(DATASET_PATH):
        df = read_csv_safe(DATASET_PATH)
        df = process_dataframe(df)
        conn.register('zepto', df)
    return conn

def load_data():
    """Loads dataset into Pandas DataFrame."""
    if os.path.exists(DATASET_PATH):
        df = read_csv_safe(DATASET_PATH)
        return process_dataframe(df)
    return pd.DataFrame()
