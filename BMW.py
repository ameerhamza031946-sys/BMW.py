import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="BMW Stock Dashboard", page_icon="🚗", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('BMW_Data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    return df

df = load_data()

# Title
st.title("🚗 BMW Stock Dashboard")
st.markdown("---")

# Sidebar for filters
st.sidebar.header("Filters")

# Date range selector
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Filter data based on date range
filtered_df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    latest_close = filtered_df['Close'].iloc[-1] if not filtered_df.empty else 0
    st.metric("Latest Close Price", f"${latest_close:.2f}")

with col2:
    avg_volume = filtered_df['Volume'].mean()
    st.metric("Average Volume", f"{avg_volume:,.0f}")

with col3:
    price_change = filtered_df['Close'].iloc[-1] - filtered_df['Close'].iloc[0] if len(filtered_df) > 1 else 0
    st.metric("Price Change", f"${price_change:.2f}", delta=f"{(price_change/filtered_df['Close'].iloc[0]*100):.2f}%" if len(filtered_df) > 1 else "0%")

with col4:
    max_high = filtered_df['High'].max()
    st.metric("Highest Price", f"${max_high:.2f}")

st.markdown("---")

# Price Chart
st.subheader("Stock Price Over Time")
fig_price = go.Figure()

fig_price.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Close'],
                              mode='lines', name='Close Price',
                              line=dict(color='blue', width=2)))

fig_price.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['High'],
                              mode='lines', name='High Price',
                              line=dict(color='green', width=1, dash='dot')))

fig_price.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Low'],
                              mode='lines', name='Low Price',
                              line=dict(color='red', width=1, dash='dot')))

fig_price.update_layout(
    title="BMW Stock Prices",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    hovermode="x unified"
)

st.plotly_chart(fig_price, use_container_width=True)

# Volume Chart
st.subheader("Trading Volume")
fig_volume = px.bar(filtered_df, x='Date', y='Volume',
                   title="Daily Trading Volume",
                   labels={'Volume': 'Volume', 'Date': 'Date'})

fig_volume.update_layout(
    xaxis_title="Date",
    yaxis_title="Volume"
)

st.plotly_chart(fig_volume, use_container_width=True)

# Candlestick Chart
st.subheader("Candlestick Chart")
fig_candle = go.Figure(data=[go.Candlestick(x=filtered_df['Date'],
                open=filtered_df['Open'],
                high=filtered_df['High'],
                low=filtered_df['Low'],
                close=filtered_df['Close'])])

fig_candle.update_layout(
    title="BMW Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price ($)"
)

st.plotly_chart(fig_candle, use_container_width=True)

# Data Table
st.subheader("Raw Data")
st.dataframe(filtered_df.tail(20))  # Show last 20 rows

# Statistics
st.subheader("Statistical Summary")
st.write(filtered_df.describe())