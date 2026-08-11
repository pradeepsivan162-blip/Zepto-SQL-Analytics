import os
import pandas as pd
import duckdb

DEFAULT_DATASET_PATH = os.path.join(os.path.dirname(__file__), "Dataset", "zepto_v1.csv")

def read_csv_safe(path_or_file):
    """Safely reads CSV or Excel file with multiple encoding fallbacks."""
    if hasattr(path_or_file, 'name') and path_or_file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(path_or_file)
    
    encodings = ['utf-8', 'latin1', 'cp1252', 'utf-8-sig']
    for enc in encodings:
        try:
            if hasattr(path_or_file, 'seek'):
                path_or_file.seek(0)
            return pd.read_csv(path_or_file, encoding=enc)
        except (UnicodeDecodeError, Exception):
            continue
    
    if hasattr(path_or_file, 'seek'):
        path_or_file.seek(0)
    return pd.read_csv(path_or_file, encoding='utf-8', encoding_errors='replace')

def process_dataframe(df):
    """Normalizes column names and data types for seamless SQL and Streamlit usage."""
    if df.empty:
        return df

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

    # Legacy SQL column alias support
    if 'discountedSellingPrice' in df.columns and 'discountSellingPrice' not in df.columns:
        df['discountSellingPrice'] = df['discountedSellingPrice']

    # Clean strings
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

def load_data(custom_file=None):
    """Loads dataset from custom file or default Dataset/zepto_v1.csv."""
    if custom_file is not None:
        df = read_csv_safe(custom_file)
        return process_dataframe(df)
    elif os.path.exists(DEFAULT_DATASET_PATH):
        df = read_csv_safe(DEFAULT_DATASET_PATH)
        return process_dataframe(df)
    return pd.DataFrame()

def get_connection(df=None):
    """Returns a DuckDB in-memory database connection with `zepto` table pre-loaded."""
    conn = duckdb.connect(database=':memory:')
    if df is None:
        df = load_data()
    if not df.empty:
        conn.register('zepto', df)
    return conn
