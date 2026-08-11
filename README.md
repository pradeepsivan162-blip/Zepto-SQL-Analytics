# 🛒 Zepto SQL Analytics & Interactive Web Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL%20%7C%20DuckDB-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📌 Project Overview

This project provides an end-to-end data analytics solution for **Zepto** quick-commerce product data. It combines **PostgreSQL SQL analysis**, **Power BI metrics**, and an **interactive Streamlit Web Application** featuring live SQL query execution and dynamic visual dashboards.

---

## 📊 Dashboard & Web Application Features

1. **Executive Visual Dashboard (Power BI Replica)**:
   - **KPI Cards**: Total Products, Total MRP, Total Categories.
   - **Interactive Charts**:
     - Total MRP by Category (Bar Chart)
     - Product Quantity by Category (Horizontal Bar Chart)
     - Product Availability Status (Donut Chart - In Stock vs Out of Stock)
   - **Interactive Sidebar Filters**: Category multi-select, In-Stock/Out-of-Stock toggle, and MRP Price range slider.

2. **Live SQL Analytics Playground**:
   - Embedded in-memory SQL engine (**DuckDB**) pre-loaded with `zepto_v1.csv`.
   - Run custom PostgreSQL-compatible SQL queries directly in the browser.
   - 10+ pre-built business analysis queries (CTEs, Window Functions, Aggregations).
   - Instant query result view & CSV export.

3. **Raw Dataset Explorer**:
   - Browse filtered dataset records, view metadata, and download processed data.

---

## 🚀 Live Deployment Guide

You can deploy this project online for **FREE** using **Streamlit Community Cloud** or **Render**.

### Option 1: Deploy to Streamlit Community Cloud (Recommended - 1 Minute Setup)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy Zepto Streamlit Web App"
   git push origin main
   ```
2. **Go to Streamlit Cloud**:
   - Open [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. **Deploy New App**:
   - Click **New app**.
   - Select your GitHub repository: `Zepto-SQL-Analytics`.
   - Set **Branch**: `main`.
   - Set **Main file path**: `app.py`.
   - Click **Deploy!**
4. 🎉 **Done!** Your dashboard will be live at `https://<your-username>-zepto-sql-analytics-app.streamlit.app`.

---

### Option 2: Deploy to Render Web Service

1. Sign up / Log in to [Render.com](https://render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository `Zepto-SQL-Analytics`.
4. Configure setting details:
   - **Name**: `zepto-sql-analytics`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Click **Create Web Service**. Render will build and launch your live application URL!

---

## 💻 Running Locally

To run the application locally on your machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pradeepsivan162-blip/Zepto-SQL-Analytics.git
   cd Zepto-SQL-Analytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Streamlit**:
   ```bash
   streamlit run app.py
   ```

4. Open `http://localhost:8501` in your browser.

---

## 📂 Project Structure

```text
Zepto-SQL-Analytics/
├── .streamlit/
│   └── config.toml         # Custom Streamlit theme styling
├── Dashboard/
│   ├── Zepto.pbix          # Power BI dashboard report file
│   └── dashboard-1.png     # Power BI original dashboard screenshot
├── Dataset/
│   ├── zepto_v1.csv        # Primary CSV Dataset
│   └── zepto_v1.csv.xlsx   # Excel Dataset
├── SQL/
│   ├── 01_Create_Table.sql
│   ├── 02_Data_Exploration.sql
│   ├── 03_Data_Cleaning.sql
│   ├── 04_Business_Analysis.sql
│   ├── 05_Window_Functions.sql
│   ├── 06_CTEs.sql
│   └── 07_Views.sql
├── app.py                  # Main Streamlit web application
├── db.py                   # In-memory DuckDB database loader
├── queries.py              # Pre-built SQL queries collection
├── requirements.txt        # Python dependencies
└── README.md               # Documentation & Deployment guide
```

---

## 🚀 Key SQL Concepts Demonstrated

- **Aggregation & Summary Stats**: `SUM`, `AVG`, `COUNT`, `ROUND`
- **Conditional Logic**: `CASE WHEN ... THEN ... END`
- **Filtering & Grouping**: `GROUP BY`, `HAVING`, `ORDER BY`
- **CTEs (Common Table Expressions)**: `WITH RankedProducts AS (...)`
- **Window Functions**: `RANK() OVER (...)`, `ROW_NUMBER() OVER (...)`

---

## 👨‍💻 Author

**Pradeep S**
- 💼 **LinkedIn**: [linkedin.com/in/pradeep-s-836b57323/](https://www.linkedin.com/in/pradeep-s-836b57323/)
- 🐙 **GitHub**: [github.com/pradeepsivan162-blip](https://github.com/pradeepsivan162-blip)