# 🛒 Zepto SQL Analytics & AI Assistant Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![AI Powered](https://img.shields.io/badge/AI-Google%20Gemini-purple.svg)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL%20%7C%20DuckDB-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📌 Project Overview

This project is an advanced, AI-powered data analytics platform for **Zepto** quick-commerce product data. It combines **PostgreSQL SQL analysis**, **Power BI metrics**, **dynamic daily dataset uploads**, and an **interactive Google Gemini AI Assistant** that translates natural language questions into live SQL queries and business insights.

---

## 🌟 Key Features

1. **📊 Executive Visual Dashboard (Power BI Replica)**:
   - **KPI Cards**: Total Products, Total MRP, Total Categories.
   - **Interactive Charts**: Total MRP by Category, Product Quantity by Category, and Availability Status (Donut Chart).
   - **Sidebar Filters**: Category multiselect, In-Stock/Out-of-Stock toggle, and Price range slider.

2. **📅 Daily Dataset Uploader (CSV / Excel)**:
   - Upload new daily `.csv` or `.xlsx` dataset files directly in the sidebar UI.
   - All charts, metrics, and SQL query engines automatically adapt and update instantly.

3. **🤖 Gemini AI Data Assistant (Powered by Google Gemini 2.5)**:
   - Conversational chat interface to ask natural language questions about your dataset.
   - Converts questions like *"What are the top 5 categories by total revenue?"* into executable SQL queries automatically.
   - Runs SQL against the active dataset using DuckDB and renders both tables and plain-English explanations.

4. **⚡ Live SQL Analytics Playground**:
   - Embedded DuckDB SQL engine pre-loaded with your dataset.
   - Run custom PostgreSQL queries or select from 11 pre-built SQL analysis templates (CTEs, Window Functions, Aggregations).
   - CSV data download support.

---

## 🤖 Configuring Gemini AI API Key

To enable live Gemini AI responses in Streamlit Cloud:

1. Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).
2. On Streamlit Cloud:
   - Open your App -> **Settings** -> **Secrets**.
   - Add your API Key:
     ```toml
     GEMINI_API_KEY = "your_actual_gemini_api_key_here"
     ```
3. Alternatively, users can enter their Gemini API Key directly in the UI sidebar password field.

---

## 🚀 Live Deployment Guide (Streamlit Cloud)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Gemini AI Assistant and Daily Dataset Upload"
   git push origin main
   ```
2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/).
   - Connect repository `Zepto-SQL-Analytics`, branch `main`, main file `app.py`.
   - Click **Deploy!**

---

## 📂 Project Structure

```text
Zepto-SQL-Analytics/
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── Dashboard/
│   ├── Zepto.pbix          # Power BI dashboard report
│   └── dashboard-1.png     # Power BI screenshot
├── Dataset/
│   ├── zepto_v1.csv        # Primary CSV Dataset
│   └── zepto_v1.csv.xlsx   # Excel Dataset
├── SQL/
│   ├── 01_Create_Table.sql ... 07_Views.sql
├── ai_helper.py            # Google Gemini AI assistant module
├── app.py                  # Streamlit web application & chat UI
├── db.py                   # Dynamic data loader & DuckDB SQL engine
├── queries.py              # Pre-built SQL queries suite
├── requirements.txt        # Python dependencies
└── README.md               # Documentation & Deployment guide
```

---

## 👨‍💻 Author

**Pradeep S**
- 💼 **LinkedIn**: [linkedin.com/in/pradeep-s-836b57323/](https://www.linkedin.com/in/pradeep-s-836b57323/)
- 🐙 **GitHub**: [github.com/pradeepsivan162-blip](https://github.com/pradeepsivan162-blip)