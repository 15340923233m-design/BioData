import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Support Chinese & English font display
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Page basic settings
st.set_page_config(
    page_title="ShopEasy Sales & Inventory Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom page style
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c5f8a;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 1rem;
        border-left: 5px solid #1f4e79;
    }
    .stAlert {
        border-radius: 8px;
    }
    .dataframe {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Load sales data with cache
@st.cache_data
def load_sales_data():
    try:
        df = pd.read_csv('sales_data.csv')
    except FileNotFoundError:
        # Generate sample data if file not found
        np.random.seed(42)
        products = ['Wireless Mouse', 'Mechanical Keyboard', 'USB-C Cable', 'Bluetooth Earbuds', 'Phone Case',
                    'T-Shirt', 'Jeans', 'Sneakers', 'Rice 5kg', 'Cooking Oil 1L',
                    'Dish Soap', 'Laundry Detergent', 'Tissues', 'Novel', 'Textbook',
                    'Yoga Mat', 'Dumbbell', 'Jump Rope', 'Basketball', 'Knee Pads']
        categories = ['Electronics']*5 + ['Clothing']*4 + ['Food']*2 + ['Home']*3 + ['Books']*2 + ['Sports']*4

        data = []
        for i in range(100):
            idx = i % len(products)
            data.append({
                'Product_Name': products[idx],
                'Category': categories[idx],
                'Sales_Quantity': np.random.randint(1, 50),
                'Unit_Price': round(np.random.uniform(10, 500), 2),
                'Sales_Date': (pd.Timestamp('2025-01-01') + pd.Timedelta(days=np.random.randint(0, 500))).strftime('%Y-%m-%d')
            })
        df = pd.DataFrame(data)

    df['Sales_Date'] = pd.to_datetime(df['Sales_Date'])
    df['Total_Revenue'] = df['Sales_Quantity'] * df['Unit_Price']
    return df

# Load inventory data with cache
@st.cache_data
def load_inventory_data():
    try:
        df = pd.read_csv('inventory_data.csv')
    except FileNotFoundError:
        # Generate sample inventory data if file not found
        np.random.seed(42)
        products = ['Wireless Mouse', 'Mechanical Keyboard', 'USB-C Cable', 'Bluetooth Earbuds', 'Phone Case',
                    'T-Shirt', 'Jeans', 'Sneakers', 'Rice 5kg', 'Cooking Oil 1L',
                    'Dish Soap', 'Laundry Detergent', 'Tissues', 'Novel', 'Textbook',
                    'Yoga Mat', 'Dumbbell', 'Jump Rope', 'Basketball', 'Knee Pads',
                    'Power Bank', 'Smart Watch', 'Tablet', 'Monitor', 'Router',
                    'Jacket', 'Dress', 'Socks', 'Hat', 'Scarf']
        categories = ['Electronics']*5 + ['Clothing']*4 + ['Food']*2 + ['Home']*3 + ['Books']*2 + ['Sports']*4 + ['Electronics']*5 + ['Clothing']*5

        data = []
        for i in range(min(len(products), 40)):
            data.append({
                'Product_Name': products[i],
                'Category': categories[i],
                'Stock_Quantity': np.random.randint(5, 100)
            })
        df = pd.DataFrame(data)
    return df

# Main Title
st.markdown('<div class="main-header">📊 ShopEasy Sales Analysis & Inventory Management Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# ==================== Sidebar Filters ====================
st.sidebar.markdown("## 🔍 Data Filters")
st.sidebar.markdown("---")

# Load datasets
sales_df = load_sales_data()
inventory_df = load_inventory_data()

# Category filter
categories = ['All'] + sorted(sales_df['Category'].unique().tolist())
selected_category = st.sidebar.selectbox("📂 Select Product Category", categories)

# Date range filter
min_date = sales_df['Sales_Date'].min().date()
max_date = sales_df['Sales_Date'].max().date()
start_date = st.sidebar.date_input("📅 Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("📅 End Date", max_date, min_value=min_date, max_value=max_date)

# Low stock threshold setting
st.sidebar.markdown("---")
st.sidebar.markdown("## ⚠️ Stock Alert Settings")
stock_threshold = st.sidebar.slider("🔴 Low Stock Threshold", min_value=5, max_value=50, value=20, step=5)

# ==================== Apply Filters ====================
filtered_df = sales_df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

filtered_df = filtered_df[
    (filtered_df['Sales_Date'].dt.date >= start_date) &
    (filtered_df['Sales_Date'].dt.date <= end_date)
]

# ==================== Sales Overview ====================
st.markdown('<div class="sub-header">📈 Sales Overview</div>', unsafe_allow_html=True)

# Key performance metrics
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['Total_Revenue'].sum()
total_units = filtered_df['Sales_Quantity'].sum()
avg_price = filtered_df['Unit_Price'].mean() if len(filtered_df) > 0 else 0
total_transactions = len(filtered_df)

with col1:
    st.metric("💰 Total Revenue", f"RM {total_revenue:,.2f}")
with col2:
    st.metric("📦 Total Units Sold", f"{total_units:,} units")
with col3:
    st.metric("💵 Average Unit Price", f"RM {avg_price:,.2f}")
with col4:
    st.metric("🛒 Total Transactions", f"{total_transactions:,}")

st.markdown("---")

# Sales detail table
st.markdown('<div class="sub-header">📋 Sales Data Details</div>', unsafe_allow_html=True)
if len(filtered_df) > 0:
    display_df = filtered_df[['Product_Name', 'Category', 'Sales_Quantity', 'Unit_Price', 'Total_Revenue', 'Sales_Date']].copy()
    display_df['Sales_Date'] = display_df['Sales_Date'].dt.strftime('%Y-%m-%d')
    display_df = display_df.sort_values('Sales_Date', ascending=False)
    st.dataframe(display_df, use_container_width=True, height=300)
else:
    st.warning("⚠️ No data available for current filters. Please adjust your selection.")

st.markdown("---")

# ==================== Data Visualization ====================
st.markdown('<div class="sub-header">📊 Data Visualization</div>', unsafe_allow_html=True)

viz_col1, viz_col2 = st.columns(2)

# Revenue by category bar chart
with viz_col1:
    st.markdown("##### 📊 Revenue by Category")
    if len(filtered_df) > 0:
        category_revenue = filtered_df.groupby('Category')['Total_Revenue'].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(category_revenue.index, category_revenue.values,
                      color=['#1f4e79', '#2c5f8a', '#3d7ab5', '#5a9bd5', '#7bb3e0', '#a3c9e8'])
        ax.set_xlabel('Product Category')
        ax.set_ylabel('Total Revenue (RM)')
        ax.set_title('Revenue Comparison by Category', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'RM{height:,.0f}', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No data to display")

# Monthly sales trend line chart
with viz_col2:
    st.markdown("##### 📈 Monthly Sales Trend")
    if len(filtered_df) > 0:
        monthly_sales = filtered_df.copy()
        monthly_sales['Year_Month'] = monthly_sales['Sales_Date'].dt.to_period('M').astype(str)
        monthly_trend = monthly_sales.groupby('Year_Month')['Total_Revenue'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(monthly_trend['Year_Month'], monthly_trend['Total_Revenue'],
                marker='o', linewidth=2.5, markersize=8, color='#1f4e79')
        ax.fill_between(monthly_trend['Year_Month'], monthly_trend['Total_Revenue'], alpha=0.3, color='#1f4e79')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Revenue (RM)')
        ax.set_title('Monthly Sales Trend Analysis', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No data to display")

# Sales share pie chart
st.markdown("---")
st.markdown("##### 🥧 Category Sales Share")

pie_col1, pie_col2 = st.columns([2, 1])
with pie_col1:
    if len(filtered_df) > 0:
        category_share = filtered_df.groupby('Category')['Total_Revenue'].sum()

        fig, ax = plt.subplots(figsize=(8, 6))
        colors_pie = ['#1f4e79', '#2c5f8a', '#3d7ab5', '#5a9bd5', '#7bb3e0', '#a3c9e8']
        wedges, texts, autotexts = ax.pie(category_share.values, labels=category_share.index,
                                          autopct='%1.1f%%', startangle=90, colors=colors_pie)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax.set_title('Category Sales Share Distribution', fontweight='bold')
        st.pyplot(fig)
    else:
        st.info("No data to display")

with pie_col2:
    if len(filtered_df) > 0:
        st.markdown("**Share Details:**")
        share_df = pd.DataFrame({
            'Category': category_share.index,
            'Revenue': category_share.values,
            'Share (%)': (category_share.values / category_share.sum() * 100).round(1)
        })
        st.dataframe(share_df, use_container_width=True)

st.markdown("---")

# ==================== Inventory Management ====================
st.markdown('<div class="sub-header">📦 Inventory Management</div>', unsafe_allow_html=True)

# Use functional programming to filter low stock products
low_stock_filter = filter(lambda x: x['Stock_Quantity'] < stock_threshold, inventory_df.to_dict('records'))
low_stock_list = list(low_stock_filter)

# Calculate stock shortage
low_stock_values = list(map(lambda x: {
    'Product_Name': x['Product_Name'],
    'Category': x['Category'],
    'Stock_Quantity': x['Stock_Quantity'],
    'Shortage': stock_threshold - x['Stock_Quantity']
}, low_stock_list))

# Calculate total shortage quantity
total_shortage = reduce(lambda acc, x: acc + x['Shortage'], low_stock_values, 0) if low_stock_values else 0

# Low stock alert message
if low_stock_values:
    st.error(f"🚨 Alert: {len(low_stock_values)} products are below {stock_threshold} units! Total Shortage: {total_shortage} units")
    low_stock_df = pd.DataFrame(low_stock_values)
    st.markdown("##### 🔴 Low Stock Product List")
    st.dataframe(low_stock_df, use_container_width=True)
else:
    st.success(f"✅ All products are well stocked (≥ {stock_threshold} units)")

# Full inventory table with highlight
st.markdown("##### 📋 Full Inventory List")

def highlight_low_stock(val):
    if isinstance(val, (int, float)) and val < stock_threshold:
        return 'background-color: #ffcccc; color: #cc0000; font-weight: bold'
    return ''

# Compatible with different Pandas versions
pd_version = pd.__version__.split('.')
major_version = int(pd_version[0])
minor_version = int(pd_version[1])

if major_version >= 2 or (major_version == 1 and minor_version >= 4):
    styled_inventory = inventory_df.style.map(highlight_low_stock, subset=['Stock_Quantity'])
else:
    styled_inventory = inventory_df.style.applymap(highlight_low_stock, subset=['Stock_Quantity'])

st.dataframe(styled_inventory, use_container_width=True, height=300)

# Inventory statistics by category
st.markdown("---")
st.markdown("##### 📊 Inventory Statistics by Category")

inv_col1, inv_col2 = st.columns(2)
with inv_col1:
    category_stock = inventory_df.groupby('Category')['Stock_Quantity'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(category_stock.index, category_stock.values, color=['#1f4e79', '#2c5f8a', '#3d7ab5', '#5a9bd5', '#7bb3e0', '#a3c9e8'])
    ax.set_xlabel('Total Stock Quantity')
    ax.set_ylabel('Product Category')
    ax.set_title('Total Stock by Category', fontweight='bold')
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2., f'{int(width)}', ha='left', va='center')
    plt.tight_layout()
    st.pyplot(fig)

with inv_col2:
    category_stats = inventory_df.groupby('Category').agg({
        'Stock_Quantity': ['sum', 'mean', 'count']
    }).round(1)
    category_stats.columns = ['Total Stock', 'Average Stock', 'Product Count']
    st.dataframe(category_stats, use_container_width=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem; margin-top: 2rem;">
    <hr>
    <p>ShopEasy Sdn Bhd | Sales Analysis & Inventory Management Dashboard | 2026</p>
</div>
""", unsafe_allow_html=True)