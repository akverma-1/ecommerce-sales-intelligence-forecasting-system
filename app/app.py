import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np

st.set_page_config(page_title="E-Commerce Sales Intelligence & Forecasting System", layout="wide", page_icon="🛒")

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv('../data/processed_data.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    rfm = pd.read_csv('../data/rfm_data.csv')
    forecast = pd.read_csv('../data/forecast.csv')
    return df, rfm, forecast

df, rfm, forecast = load_data()
# ---------- Sidebar Navigation ----------
st.sidebar.title("🛒 E-Commerce Analytics")
page = st.sidebar.radio("Navigate", 
    ["Overview", "Category Analysis", "Regional Analysis", 
     "Customer Segmentation (RFM)", "Sales Forecast",
     "Top Customers", "Shipping Analysis", "Profit Predictor"])

# ---------- Sidebar Filters ----------
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

min_date, max_date = df['Order Date'].min(), df['Order Date'].max()
date_range = st.sidebar.date_input("Order Date Range", value=(min_date, max_date),
                                     min_value=min_date, max_value=max_date)

regions = st.sidebar.multiselect("Region", options=df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())

if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = min_date, max_date

filtered_df = df[(df['Region'].isin(regions)) & 
                  (df['Category'].isin(categories)) &
                  (df['Order Date'] >= start_date) & 
                  (df['Order Date'] <= end_date)]

# Download button (always available in sidebar)
st.sidebar.markdown("---")
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download Filtered Data (CSV)", data=csv_data, 
                             file_name="filtered_sales_data.csv", mime="text/csv")

# ================= PAGE 1: OVERVIEW =================
if page == "Overview":
    st.title("Business Overview")

    # KPI trend vs previous equal-length period
    period_days = (end_date - start_date).days
    prev_start = start_date - pd.Timedelta(days=period_days+1)
    prev_end = start_date - pd.Timedelta(days=1)
    prev_df = df[(df['Order Date'] >= prev_start) & (df['Order Date'] <= prev_end) &
                 (df['Region'].isin(regions)) & (df['Category'].isin(categories))]

    def pct_change(curr, prev):
        if prev == 0: return 0
        return ((curr - prev) / prev) * 100

    curr_sales, prev_sales = filtered_df['Sales'].sum(), prev_df['Sales'].sum()
    curr_profit, prev_profit = filtered_df['Profit'].sum(), prev_df['Profit'].sum()
    curr_orders, prev_orders = filtered_df['Order ID'].nunique(), prev_df['Order ID'].nunique()
    curr_cust, prev_cust = filtered_df['Customer ID'].nunique(), prev_df['Customer ID'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${curr_sales:,.0f}", f"{pct_change(curr_sales, prev_sales):.1f}%")
    col2.metric("Total Profit", f"${curr_profit:,.0f}", f"{pct_change(curr_profit, prev_profit):.1f}%")
    col3.metric("Total Orders", f"{curr_orders:,}", f"{pct_change(curr_orders, prev_orders):.1f}%")
    col4.metric("Total Customers", f"{curr_cust:,}", f"{pct_change(curr_cust, prev_cust):.1f}%")
    st.caption("% change compared to previous period of same length")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        monthly = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
        monthly['Order Date'] = monthly['Order Date'].astype(str)
        fig = px.line(monthly, x='Order Date', y='Sales', title='Monthly Sales Trend', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        seg_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
        fig = px.pie(seg_sales, names='Segment', values='Sales', title='Sales by Customer Segment')
        st.plotly_chart(fig, use_container_width=True)

# ================= PAGE 2: CATEGORY ANALYSIS =================
elif page == "Category Analysis":
    st.title("Category & Product Analysis")

    cat_summary = filtered_df.groupby('Category')[['Sales','Profit']].sum().reset_index()
    fig = px.bar(cat_summary, x='Category', y=['Sales','Profit'], barmode='group', title='Sales vs Profit by Category')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Category → Sub-Category Breakdown (Treemap)")
    treemap_data = filtered_df.groupby(['Category','Sub-Category'])['Sales'].sum().reset_index()
    fig_tree = px.treemap(treemap_data, path=['Category','Sub-Category'], values='Sales',
                            color='Sales', color_continuous_scale='Blues',
                            title='Sales Distribution: Category → Sub-Category')
    st.plotly_chart(fig_tree, use_container_width=True)

    st.subheader("Discount vs Profit Impact")
    fig2 = px.scatter(filtered_df, x='Discount', y='Profit', color='Category', 
                       title='Discount vs Profit (by Category)', opacity=0.6)
    fig2.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Profitable Products")
        top = filtered_df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
        st.dataframe(top)
    with col2:
        st.subheader("Top 10 Loss-Making Products")
        loss = filtered_df.groupby('Product Name')['Profit'].sum().sort_values().head(10)
        st.dataframe(loss)

# ================= PAGE 3: REGIONAL ANALYSIS =================
elif page == "Regional Analysis":
    st.title("Regional & Geographic Analysis")

    region_summary = filtered_df.groupby('Region')[['Sales','Profit']].sum().reset_index()
    fig = px.bar(region_summary, x='Region', y=['Sales','Profit'], barmode='group', title='Sales vs Profit by Region')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("State-wise Sales Map")
    state_summary = filtered_df.groupby('State')[['Sales','Profit']].sum().reset_index()
    fig2 = px.choropleth(state_summary, locations='State', locationmode='USA-states',
                          color='Sales', scope='usa', color_continuous_scale='Blues',
                          title='Sales by State')
    st.plotly_chart(fig2, use_container_width=True)

# ================= PAGE 4: RFM SEGMENTATION =================
elif page == "Customer Segmentation (RFM)":
    st.title("Customer Segmentation (RFM Analysis)")

    col1, col2 = st.columns(2)
    with col1:
        seg_count = rfm['Segment'].value_counts().reset_index()
        seg_count.columns = ['Segment', 'Count']
        fig = px.bar(seg_count, x='Segment', y='Count', title='Customer Segments', color='Segment')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(rfm, x='Recency', y='Monetary', color='Segment', size='Frequency',
                           title='Recency vs Monetary (bubble size = Frequency)')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("RFM Data Table")
    st.dataframe(rfm.sort_values('Monetary', ascending=False))

# ================= PAGE 5: FORECAST =================
elif page == "Sales Forecast":
    st.title("Sales Forecast (Next 6 Months)")
    st.info("Forecast generated using SARIMA model trained on monthly sales trend with seasonality.")

    historical = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    historical['Order Date'] = historical['Order Date'].dt.to_timestamp()
    historical.columns = ['Date', 'Sales']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historical['Date'], y=historical['Sales'],
                              mode='lines+markers', name='Actual Sales', line=dict(color='#00C2A8')))
    fig.add_trace(go.Scatter(x=pd.to_datetime(forecast['Date']), y=forecast['Forecast'],
                              mode='lines+markers', name='Forecasted Sales', line=dict(color='#F97316', dash='dash')))

    fig.update_layout(title='Actual vs Forecasted Sales', template='plotly_dark',
                       plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
                       xaxis_title='Date', yaxis_title='Sales')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(" Forecast Table")
    st.dataframe(forecast, use_container_width=True)
# ================= PAGE 6: TOP CUSTOMERS =================
elif page == "Top Customers":
    st.title("Top Customers")

    search = st.text_input("🔍 Search Customer Name")

    cust_summary = filtered_df.groupby(['Customer ID','Customer Name']).agg(
        Total_Sales=('Sales','sum'),
        Total_Profit=('Profit','sum'),
        Total_Orders=('Order ID','nunique')
    ).reset_index().sort_values('Total_Sales', ascending=False)

    if search:
        cust_summary = cust_summary[cust_summary['Customer Name'].str.contains(search, case=False, na=False)]

    st.dataframe(cust_summary, use_container_width=True)

    st.subheader("Top 15 Customers by Sales")
    top15 = cust_summary.head(15)
    fig = px.bar(top15, x='Customer Name', y='Total_Sales', color='Total_Profit',
                 title='Top 15 Customers', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)

# ================= PAGE 7: SHIPPING ANALYSIS =================
elif page == "Shipping Analysis":
    st.title("Shipping Performance Analysis")

    col1, col2 = st.columns(2)
    with col1:
        ship_mode_summary = filtered_df.groupby('Ship Mode')['Order ID'].nunique().reset_index()
        ship_mode_summary.columns = ['Ship Mode', 'Orders']
        fig = px.pie(ship_mode_summary, names='Ship Mode', values='Orders', title='Orders by Ship Mode')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        avg_ship_days = filtered_df.groupby('Ship Mode')['Shipping Days'].mean().reset_index()
        fig2 = px.bar(avg_ship_days, x='Ship Mode', y='Shipping Days', title='Avg Shipping Days by Mode',
                       color='Shipping Days', color_continuous_scale='Oranges')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Shipping Days Distribution")
    fig3 = px.histogram(filtered_df, x='Shipping Days', nbins=15, title='Distribution of Shipping Days')
    st.plotly_chart(fig3, use_container_width=True)

# ================= PAGE 8: PROFIT PREDICTOR (ML) =================
elif page == "Profit Predictor":
    st.title(" Profit Prediction Model")
    st.markdown("Predict expected profit for a hypothetical order using a trained regression model.")

    # Train simple model on the fly (cached)
    @st.cache_resource
    def train_model(data):
        model_df = data[['Sales','Quantity','Discount','Category','Sub-Category','Profit']].dropna()
        le_cat = LabelEncoder()
        le_sub = LabelEncoder()
        model_df['Category_enc'] = le_cat.fit_transform(model_df['Category'])
        model_df['SubCat_enc'] = le_sub.fit_transform(model_df['Sub-Category'])

        X = model_df[['Sales','Quantity','Discount','Category_enc','SubCat_enc']]
        y = model_df['Profit']

        reg = LinearRegression()
        reg.fit(X, y)
        return reg, le_cat, le_sub

    reg, le_cat, le_sub = train_model(df)

    col1, col2 = st.columns(2)
    with col1:
        input_sales = st.number_input("Sales Amount ($)", min_value=1.0, value=100.0)
        input_qty = st.number_input("Quantity", min_value=1, value=2)
        input_discount = st.slider("Discount", 0.0, 0.8, 0.1)
    with col2:
        input_cat = st.selectbox("Category", df['Category'].unique())
        input_subcat = st.selectbox("Sub-Category", df[df['Category']==input_cat]['Sub-Category'].unique())

    if st.button("Predict Profit"):
        cat_encoded = le_cat.transform([input_cat])[0]
        subcat_encoded = le_sub.transform([input_subcat])[0]
        pred = reg.predict([[input_sales, input_qty, input_discount, cat_encoded, subcat_encoded]])[0]

        if pred >= 0:
            st.success(f"Predicted Profit: ${pred:,.2f}")
        else:
            st.error(f"⚠️ Predicted Loss: ${pred:,.2f}")
        st.caption("Model: Linear Regression trained on Sales, Quantity, Discount, Category & Sub-Category")