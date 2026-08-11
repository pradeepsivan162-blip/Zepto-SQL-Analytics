import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection, load_data
from queries import PREBUILT_QUERIES
from ai_helper import ask_gemini

# Page Configuration
st.set_page_config(
    page_title="Zepto Analytics Dashboard & AI Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Zepto Purple & Gold Palette)
st.markdown("""
<style>
    /* Global styles */
    .main-header {
        background: linear-gradient(135deg, #7000FF 0%, #8E24AA 100%);
        color: #FFC107;
        text-align: center;
        padding: 24px 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(112, 0, 255, 0.3);
        margin-bottom: 25px;
        font-family: 'Inter', sans-serif;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #FFD54F;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 1.05rem;
        color: #E1BEE7;
    }
    
    /* Metric / KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #D4AF37 0%, #C5A028 100%);
        border: 2px solid #7000FF;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        color: #1A237E;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #6A1B9A;
        line-height: 1.2;
    }
    .kpi-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0D47A1;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("""
<div class="main-header">
    <h1>ZEPTO ANALYTICS DASHBOARD</h1>
    <p>PostgreSQL & Excel Data Analytics • Business Insights • Gemini AI Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar: Dataset & Filters
st.sidebar.header("📂 Data & AI Controls")

# 1. Dynamic Daily Dataset Upload
uploaded_file = st.sidebar.file_uploader(
    "📅 Upload Daily Dataset (CSV / Excel)",
    type=["csv", "xlsx", "xls"],
    help="Upload a new daily dataset file to update all dashboard analytics instantly."
)

if uploaded_file is not None:
    st.session_state['active_df'] = load_data(uploaded_file)
    st.sidebar.success(f"✅ Loaded {len(st.session_state['active_df'])} rows from uploaded file!")
elif 'active_df' not in st.session_state:
    st.session_state['active_df'] = load_data()

df_raw = st.session_state['active_df']

if df_raw.empty:
    st.error("⚠️ Dataset is empty! Please upload a valid CSV or Excel file.")
    st.stop()

# 2. Gemini API Key Input (Safe secrets handling)
st.sidebar.markdown("---")
st.sidebar.header("🤖 Gemini AI Settings")
gemini_key_input = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    help="Enter your Google Gemini API Key for live AI responses, or set GEMINI_API_KEY in Streamlit Secrets."
)

secret_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        secret_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    secret_key = None

active_gemini_key = gemini_key_input or secret_key

# 3. Visual Dashboard Filters
st.sidebar.markdown("---")
st.sidebar.header("🔍 Visual Filters")

categories = sorted(df_raw['category'].dropna().unique().tolist()) if 'category' in df_raw.columns else []
selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories
)

stock_option = st.sidebar.radio(
    "Availability Status",
    options=["All", "In Stock (False)", "Out of Stock (True)"],
    index=0
)

mrp_min = float(df_raw['mrp'].min()) if 'mrp' in df_raw.columns else 0.0
mrp_max = float(df_raw['mrp'].max()) if 'mrp' in df_raw.columns else 1000.0
selected_mrp = st.sidebar.slider(
    "MRP Range (₹)",
    min_value=mrp_min,
    max_value=mrp_max,
    value=(mrp_min, mrp_max)
)

# Apply Filters to Active Dataframe
df_filtered = df_raw.copy()
if 'category' in df_filtered.columns and selected_categories:
    df_filtered = df_filtered[df_filtered['category'].isin(selected_categories)]
if 'mrp' in df_filtered.columns:
    df_filtered = df_filtered[(df_filtered['mrp'] >= selected_mrp[0]) & (df_filtered['mrp'] <= selected_mrp[1])]
if 'outOfStock' in df_filtered.columns:
    if stock_option == "In Stock (False)":
        df_filtered = df_filtered[df_filtered['outOfStock'] == False]
    elif stock_option == "Out of Stock (True)":
        df_filtered = df_filtered[df_filtered['outOfStock'] == True]

# Tabs Definition
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visual Dashboard",
    "⚡ Interactive SQL Playground",
    "🤖 Gemini AI Assistant",
    "📄 Dataset Explorer"
])

# ==========================================
# TAB 1: VISUAL DASHBOARD
# ==========================================
with tab1:
    total_products = len(df_filtered)
    total_mrp = df_filtered['mrp'].sum() if 'mrp' in df_filtered.columns else 0
    total_categories = df_filtered['category'].nunique() if 'category' in df_filtered.columns else 0

    def format_mrp(val):
        if val >= 1_000_000:
            return f"{val / 1_000_000:.1f}M"
        elif val >= 1_000:
            return f"{val / 1_000:.0f}K"
        return f"{val:,.0f}"

    def format_kpi(val):
        if val >= 1_000:
            return f"{val / 1_000:.0f}K"
        return str(val)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{format_kpi(total_products)}</div>
            <div class="kpi-label">Total Products</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{format_mrp(total_mrp)}</div>
            <div class="kpi-label">Total MRP</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_categories}</div>
            <div class="kpi-label">Total Categories</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if 'category' in df_filtered.columns and 'mrp' in df_filtered.columns:
        st.subheader("Total MRP by Category")
        mrp_by_cat = df_filtered.groupby('category')['mrp'].sum().reset_index().sort_values(by='mrp', ascending=False)
        fig_mrp = px.bar(
            mrp_by_cat,
            x='category',
            y='mrp',
            labels={'category': '', 'mrp': 'Sum of mrp'},
            color_discrete_sequence=['#1E88E5']
        )
        fig_mrp.update_layout(xaxis_tickangle=-15, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=340)
        st.plotly_chart(fig_mrp, use_container_width=True)

    col_left, col_right = st.columns([1.2, 1])
    with col_left:
        if 'category' in df_filtered.columns and 'quantity' in df_filtered.columns:
            st.subheader("Product Quantity by Category")
            qty_by_cat = df_filtered.groupby('category')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=True)
            fig_qty = px.bar(
                qty_by_cat,
                x='quantity',
                y='category',
                orientation='h',
                labels={'category': 'Category', 'quantity': 'Sum of quantity'},
                color_discrete_sequence=['#1E88E5']
            )
            fig_qty.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=360)
            st.plotly_chart(fig_qty, use_container_width=True)

    with col_right:
        if 'outOfStock' in df_filtered.columns:
            st.subheader("Product Availability Status")
            stock_counts = df_filtered['outOfStock'].value_counts().reset_index()
            stock_counts.columns = ['outOfStock', 'count']
            stock_counts['status_label'] = stock_counts['outOfStock'].map({False: 'False (In Stock)', True: 'True (Out of Stock)'})

            fig_donut = px.pie(
                stock_counts,
                names='status_label',
                values='count',
                hole=0.6,
                color='status_label',
                color_discrete_map={'False (In Stock)': '#1E88E5', 'True (Out of Stock)': '#0D47A1'}
            )
            fig_donut.update_traces(textinfo='percent', hovertemplate='%{label}: %{value} (%{percent})')
            fig_donut.update_layout(height=360)
            st.plotly_chart(fig_donut, use_container_width=True)

# ==========================================
# TAB 2: INTERACTIVE SQL PLAYGROUND
# ==========================================
with tab2:
    st.header("⚡ Live SQL Analytics Playground")
    st.markdown("Execute PostgreSQL-compatible SQL queries directly against the `zepto` table using DuckDB.")

    selected_query_name = st.selectbox(
        "📌 Select Prebuilt Business Analysis Query:",
        options=["-- Custom SQL Query --"] + list(PREBUILT_QUERIES.keys())
    )

    default_sql = PREBUILT_QUERIES[selected_query_name] if selected_query_name != "-- Custom SQL Query --" else "SELECT category, COUNT(*) as total_items, ROUND(AVG(mrp), 2) as avg_mrp FROM zepto GROUP BY category ORDER BY avg_mrp DESC;"

    query_input = st.text_area("✍️ SQL Query Editor:", value=default_sql, height=180)

    if st.button("🚀 Run SQL Query", type="primary"):
        try:
            conn = get_connection(df_raw)
            result_df = conn.execute(query_input).df()
            st.success(f"✅ Query executed successfully! Returned {len(result_df)} rows.")
            st.dataframe(result_df, use_container_width=True)

            csv_data = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Query Results (CSV)",
                data=csv_data,
                file_name="zepto_sql_result.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"❌ SQL Execution Error: {e}")

# ==========================================
# TAB 3: GEMINI AI ASSISTANT
# ==========================================
with tab3:
    st.header("🤖 Gemini AI Data Assistant")
    st.markdown("Ask natural language questions about your Zepto dataset. Gemini AI will generate live SQL, execute it against your active dataset, and explain business insights!")

    # Preset Quick Prompts
    st.markdown("#### 💡 Quick Prompt Suggestions:")
    col_a, col_b, col_c = st.columns(3)
    preset_prompt = None
    if col_a.button("🔥 Top 5 Highest Discount Items"):
        preset_prompt = "Show top 5 products with highest discount percentage"
    if col_b.button("📦 Out of Stock Items with High MRP"):
        preset_prompt = "List top 10 out of stock products ordered by highest MRP"
    if col_c.button("💰 Estimated Revenue by Category"):
        preset_prompt = "Calculate estimated total revenue per category ordered from highest to lowest"

    if 'chat_messages' not in st.session_state:
        st.session_state['chat_messages'] = []

    # Display chat history
    for msg in st.session_state['chat_messages']:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sql" in msg and msg["sql"]:
                st.code(msg["sql"], language="sql")
            if "df" in msg and msg["df"] is not None:
                st.dataframe(msg["df"], use_container_width=True)

    # Chat Input
    user_input = st.chat_input("Ask Gemini AI a question about your Zepto dataset...") or preset_prompt

    if user_input:
        # User message
        st.session_state['chat_messages'].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Gemini AI is analyzing your data..."):
                ai_res = ask_gemini(user_input, api_key=active_gemini_key)

            st.markdown(ai_res["explanation"])

            result_df = None
            if ai_res.get("sql"):
                st.markdown("**Generated SQL Query:**")
                st.code(ai_res["sql"], language="sql")
                try:
                    conn = get_connection(df_raw)
                    result_df = conn.execute(ai_res["sql"]).df()
                    st.markdown(f"**Query Results ({len(result_df)} rows):**")
                    st.dataframe(result_df, use_container_width=True)
                except Exception as ex:
                    st.warning(f"⚠️ Could not execute generated SQL query: {ex}")

            st.session_state['chat_messages'].append({
                "role": "assistant",
                "content": ai_res["explanation"],
                "sql": ai_res.get("sql"),
                "df": result_df
            })

# ==========================================
# TAB 4: DATASET EXPLORER
# ==========================================
with tab4:
    st.header("📄 Zepto Active Dataset Explorer")
    st.write(f"Showing **{len(df_filtered)}** of **{len(df_raw)}** records.")
    
    st.dataframe(df_filtered, use_container_width=True)
    
    csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_filtered,
        file_name="zepto_active_dataset.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("👨‍💻 **Developed by Pradeep S** • Powered by Google Gemini AI & Streamlit")
