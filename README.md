# 🛒 E-Commerce Sales Intelligence & Forecasting System

An end-to-end data analytics platform built on the Superstore sales dataset, combining exploratory data analysis, customer segmentation, machine learning, and time-series forecasting into an interactive Streamlit dashboard.

**🔗 Live Demo:** _[Add your Streamlit Cloud link here]_

---

## 📌 Overview

This project analyzes 10,000+ e-commerce transactions to uncover actionable business insights around sales performance, profitability, customer behavior, and future demand. It goes beyond basic reporting by incorporating unsupervised machine learning (customer clustering) and statistical forecasting (SARIMA) to support data-driven decision-making.

## ✨ Key Features

- **Interactive Multi-Page Dashboard** — Built with Streamlit, featuring dynamic filters (date range, region, category)
- **Business KPI Tracking** — Real-time metrics with period-over-period % change
- **Category & Product Analysis** — Treemap visualization, discount-vs-profit correlation, top/bottom performing products
- **Regional & Geographic Analysis** — State-wise choropleth map of sales and profit distribution
- **Customer Segmentation (RFM Analysis)** — Recency, Frequency, Monetary scoring to classify customers into Champions, Loyal, At Risk, and Lost segments
- **K-Means Clustering** — Unsupervised ML validation of customer segments using scaled RFM features, optimal K selected via the Elbow Method
- **Sales Forecasting** — SARIMA time-series model capturing seasonality to predict sales for the next 6 months
- **Profit Predictor** — Linear Regression model that predicts expected profit for a hypothetical order based on sales amount, quantity, discount, category, and sub-category
- **Shipping Performance Analysis** — Ship mode distribution and delivery time analysis
- **Data Export** — Download filtered datasets directly from the dashboard

## 🔑 Business Insights Uncovered

- Discounts beyond 20% correlate strongly with negative profit margins across all product categories
- The Furniture category generates high sales volume but disproportionately low profit compared to Technology
- Certain high-sales states (e.g., Texas) operate at a net loss, showing that sales volume alone doesn't guarantee profitability
- ~25% of customers fall into "At Risk" or "Lost" RFM segments, highlighting a clear re-engagement opportunity
- K-Means clustering validated RFM segments, identifying a high-value cluster with disproportionate revenue contribution

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Machine Learning | Scikit-learn (KMeans, Linear Regression) |
| Time-Series Forecasting | Statsmodels (SARIMA) |
| Dashboard | Streamlit |
| Deployment | Streamlit Community Cloud |

## 📂 Project Structure

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/ecommerce-sales-intelligence-forecasting-system.git
cd ecommerce-sales-intelligence-forecasting-system
pip install -r requirements.txt
```

### Run the Dashboard

```bash
cd app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### Regenerate the Analysis (optional)

To re-run the full data pipeline (cleaning, RFM, clustering, forecasting):

```bash
cd notebooks
jupyter notebook 01_data_cleaning.ipynb
```

## 📊 Methodology

1. **Data Cleaning** — Missing value checks, duplicate removal, date parsing, feature engineering (shipping days, profit margin)
2. **Exploratory Data Analysis** — Sales/profit trends, category and regional performance, discount impact analysis
3. **RFM Segmentation** — Quantile-based scoring (1–5) across Recency, Frequency, and Monetary dimensions
4. **K-Means Clustering** — Standardized RFM features clustered into 4 groups, validated using the Elbow Method
5. **Time-Series Forecasting** — SARIMA(1,1,1)x(1,1,1,12) model fitted on monthly sales, capturing yearly seasonality
6. **Profit Prediction** — Linear Regression trained on Sales, Quantity, Discount, and encoded Category/Sub-Category

## 📈 Dataset

This project uses the **Sample Superstore** dataset (9,994 rows, 2014–2017), a widely used dataset for retail analytics practice covering Furniture, Office Supplies, and Technology product categories across the US.

## 👨‍💻 Author

**Amit Kumar Verma**
B.Tech, Computer Science & Engineering (AI & ML)
Government Engineering College, Jamui

---

*This project was built as part of a data analytics portfolio, demonstrating end-to-end skills across data cleaning, exploratory analysis, unsupervised machine learning, time-series forecasting, and dashboard deployment.*