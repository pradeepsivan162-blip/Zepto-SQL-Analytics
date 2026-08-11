import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db import get_connection, load_data
from queries import PREBUILT_QUERIES

# Page Configuration
st.set_page_config(
    page_title="Zepto Analytics Dashboard & SQL Explorer",
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

    /* StTab customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("""
<div class="main-header">
    <h1>ZEPTO ANALYTICS DASHBOARD</h1>
    <p>PostgreSQL & Excel Data Analytics • Business Insights & Live SQL Explorer</p>
</div>
""", unsafe_allow_html=True)

# Load Dataset
df_raw = load_data()

if df_raw.empty:
    st.error("⚠️ Dataset file not found! Please check `Dataset/zepto_v1.csv`.")
    st.stop()

# Sidebar Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/8/87/Zepto_Logo.png", width=160) if False else None
st.sidebar.header("🔍 Analytics Filters")

categories = sorted(df_raw['category'].dropna().unique().tolist())
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

mrp_min = float(df_raw['mrp'].min())
mrp_max = float(df_raw['mrp'].max())
selected_mrp = st.sidebar.slider(
    "MRP Range (₹)",
    min_value=mrp_min,
    max_value=mrp_max,
    value=(mrp_min, mrp_max)
)

# Filter Data
df_filtered = df_raw[df_raw['category'].isin(selected_categories)]
df_filtered = df_filtered[(df_filtered['mrp'] >= selected_mrp[0]) & (df_filtered['mrp'] <= selected_mrp[1])]

if stock_option == "In Stock (False)":
    df_filtered = df_filtered[df_filtered['outOfStock'] == False]
elif stock_option == "Out of Stock (True)":
    df_filtered = df_filtered[df_filtered['outOfStock'] == True]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Visual Dashboard", "⚡ Interactive SQL Playground", "📄 Dataset Explorer"])

# ==========================================
# TAB 1: VISUAL DASHBOARD
# ==========================================
with tab1:
    # Top KPI Metrics Cards
    total_products = len(df_filtered)
    total_mrp = df_filtered['mrp'].sum()
    total_categories = df_filtered['category'].nunique()

    def format_mrp(val):
        if val >= 1_000_000:
            return f"{val / 1_000_000:.0f}M" if (val % 1_000_000 == 0) else f"{val / 1_000_000:.1f}M"
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

    # Visual 1: Total MRP by Category (Bar Chart)
    st.subheader("Total MRP by Category")
    mrp_by_cat = df_filtered.groupby('category')['mrp'].sum().reset_index()
    mrp_by_cat = mrp_by_cat.sort_values(by='mrp', ascending=False)

    fig_mrp = px.bar(
        mrp_by_cat,
        x='category',
        y='mrp',
        labels={'category': '', 'mrp': 'Sum of mrp'},
        color_discrete_sequence=['#1E88E5']
    )
    fig_mrp.update_layout(
        xaxis_tickangle=-15,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=340,
        margin=dict(l=20, r=20, t=20, b=60)
    )
    fig_mrp.update_yaxes(showgrid=True, gridcolor='#E0E0E0')
    st.plotly_chart(fig_mrp, use_container_width=True)

    # Visual 2 & 3: Quantity by Category & Availability Donut
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("Product Quantity by Category")
        qty_by_cat = df_filtered.groupby('category')['quantity'].sum().reset_index()
        qty_by_cat = qty_by_cat.sort_values(by='quantity', ascending=True)

        fig_qty = px.bar(
            qty_by_cat,
            x='quantity',
            y='category',
            orientation='h',
            labels={'category': 'Category', 'quantity': 'Sum of quantity'},
            color_discrete_sequence=['#1E88E5']
        )
        fig_qty.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=360,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        fig_qty.update_xaxes(showgrid=True, gridcolor='#E0E0E0')
        st.plotly_chart(fig_qty, use_container_width=True)

    with col_right:
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
            color_discrete_map={
                'False (In Stock)': '#1E88E5',
                'True (Out of Stock)': '#0D47A1'
            }
        )
        fig_donut.update_traces(
            textinfo='percent',
            hovertemplate='%{label}: %{value} (%{percent})'
        )
        fig_donut.update_layout(
            height=360,
            legend=dict(title="outOfStock", orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# ==========================================
# TAB 2: INTERACTIVE SQL PLAYGROUND
# ==========================================
with tab2:
    st.header("⚡ Live SQL Analytics Playground")
    st.markdown("Execute PostgreSQL-compatible SQL queries directly against the `zepto` table using the in-memory SQL engine.")

    # Prebuilt query selector
    selected_query_name = st.selectbox(
        "📌 Select Prebuilt Business Analysis Query:",
        options=["-- Custom SQL Query --"] + list(PREBUILT_QUERIES.keys())
    )

    if selected_query_name != "-- Custom SQL Query --":
        default_sql = PREBUILT_QUERIES[selected_query_name]
    else:
        default_sql = "SELECT category, COUNT(*) as total_items, ROUND(AVG(mrp), 2) as avg_mrp FROM zepto GROUP BY category ORDER BY avg_mrp DESC;"

    query_input = st.text_area("✍️ SQL Query Editor:", value=default_sql, height=180)

    if st.button("🚀 Run SQL Query", type="primary"):
        try:
            conn = get_connection()
            result_df = conn.execute(query_input).df()
            st.success(f"✅ Query executed successfully! Returned {len(result_df)} rows.")
            st.dataframe(result_df, use_container_width=True)

            # Download CSV button
            csv_data = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Query Results (CSV)",
                data=csv_data,
                file_name="zepto_sql_result.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"❌ SQL Execution Error: {e}")

    with st.expander("📚 View Database Schema"):
        st.code("""
TABLE zepto (
    sku_id INTEGER,
    category VARCHAR(120),
    name VARCHAR(150),
    mrp NUMERIC(8,2),
    discountPercent NUMERIC(5,2),
    availableQuantity INTEGER,
    discountSellingPrice NUMERIC(8,2),
    weightInGms INTEGER,
    outOfStock BOOLEAN,
    quantity INTEGER
);
        """, language="sql")

# ==========================================
# TAB 3: DATASET EXPLORER
# ==========================================
with tab3:
    st.header("📄 Zepto Raw Dataset Explorer")
    st.write(f"Showing **{len(df_filtered)}** of **{len(df_raw)}** records.")
    
    st.dataframe(df_filtered, use_container_width=True)
    
    # Download filtered dataset
    csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_filtered,
        file_name="zepto_filtered_dataset.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("👨‍💻 **Developed by Pradeep S** • [GitHub Repository](https://github.com/pradeepsivan162-blip) • [LinkedIn](https://www.linkedin.com/in/pradeep-s-836b57323/)")
