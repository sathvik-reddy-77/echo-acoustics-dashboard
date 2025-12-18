import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Echo Friendly Acoustics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 14px;
            opacity: 0.9;
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_project_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()

# Title
st.title("🎵 Echo Friendly Acoustics - Interactive Dashboard")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Date range filter
date_range = st.sidebar.slider(
    "📅 Select Date Range",
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date(),
    value=(df["Date"].min().date(), df["Date"].max().date()),
    format="YYYY-MM-DD",
)

# Client Sector filter
sectors = st.sidebar.multiselect(
    "🏢 Select Client Sectors",
    options=df["Client Sector"].unique(),
    default=df["Client Sector"].unique(),
)

# Status filter
statuses = st.sidebar.multiselect(
    "✅ Select Project Status",
    options=df["Status"].unique(),
    default=df["Status"].unique(),
)

# Apply filters
df_filtered = df[
    (df["Date"].dt.date >= date_range[0])
    & (df["Date"].dt.date <= date_range[1])
    & (df["Client Sector"].isin(sectors))
    & (df["Status"].isin(statuses))
]

# Calculate KPIs
total_projects = len(df_filtered)
total_bottles = df_filtered["PET Bottles Diverted"].sum()
total_revenue = df_filtered["Sale Price (INR)"].sum()
total_profit = df_filtered["Profit (INR)"].sum()
avg_nrc = df_filtered["NRC Rating"].mean()

# Display KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📊 Total Projects", f"{total_projects}")

with col2:
    st.metric("♻️ PET Bottles Diverted", f"{total_bottles:,.0f}")

with col3:
    st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")

with col4:
    st.metric("📈 Total Profit", f"₹{total_profit:,.0f}")

with col5:
    st.metric("🔊 Avg NRC Rating", f"{avg_nrc:.2f}")

st.markdown("---")

# Chart 1: Revenue vs Profit by Project
st.subheader("💵 Revenue vs Profit by Project")
chart1_data = df_filtered[
    ["Project Name", "Sale Price (INR)", "Profit (INR)"]
].sort_values("Sale Price (INR)", ascending=True)
fig1 = go.Figure()
fig1.add_trace(
    go.Bar(
        x=chart1_data["Sale Price (INR)"],
        y=chart1_data["Project Name"],
        name="Revenue",
        orientation="h",
        marker_color="#667eea",
    )
)
fig1.add_trace(
    go.Bar(
        x=chart1_data["Profit (INR)"],
        y=chart1_data["Project Name"],
        name="Profit",
        orientation="h",
        marker_color="#764ba2",
    )
)
fig1.update_layout(
    barmode="group",
    height=400,
    showlegend=True,
    hovermode="closest",
)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Revenue by Client Sector
st.subheader("🏢 Revenue by Client Sector")
chart2_data = (
    df_filtered.groupby("Client Sector")["Sale Price (INR)"]
    .sum()
    .sort_values(ascending=True)
)
fig2 = go.Figure(
    data=[
        go.Bar(
            x=chart2_data.values,
            y=chart2_data.index,
            orientation="h",
            marker_color="#667eea",
        )
    ]
)
fig2.update_layout(
    height=350,
    showlegend=False,
    hovermode="closest",
)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: PET Bottles Diverted by Sector
st.subheader("♻️ PET Bottles Diverted by Sector")
chart3_data = (
    df_filtered.groupby("Client Sector")["PET Bottles Diverted"]
    .sum()
    .sort_values(ascending=True)
)
fig3 = go.Figure(
    data=[
        go.Bar(
            x=chart3_data.values,
            y=chart3_data.index,
            orientation="h",
            marker_color="#764ba2",
        )
    ]
)
fig3.update_layout(
    height=350,
    showlegend=False,
    hovermode="closest",
)
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: NRC Ratings
st.subheader("🔊 NRC Performance Ratings")
chart4_data = df_filtered[["Project Name", "NRC Rating"]].sort_values(
    "NRC Rating", ascending=True
)
fig4 = go.Figure(
    data=[
        go.Bar(
            x=chart4_data["NRC Rating"],
            y=chart4_data["Project Name"],
            orientation="h",
            marker_color="#667eea",
        )
    ]
)
fig4.update_layout(
    height=400,
    showlegend=False,
    hovermode="closest",
)
st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Revenue by Lead Source
st.subheader("🎯 Revenue by Lead Source")
chart5_data = (
    df_filtered.groupby("Lead Source")["Sale Price (INR)"]
    .sum()
    .sort_values(ascending=True)
)
fig5 = go.Figure(
    data=[
        go.Bar(
            x=chart5_data.values,
            y=chart5_data.index,
            orientation="h",
            marker_color="#764ba2",
        )
    ]
)
fig5.update_layout(
    height=350,
    showlegend=False,
    hovermode="closest",
)
st.plotly_chart(fig5, use_container_width=True)

# Chart 6: Square Footage Installed
st.subheader("📐 Square Footage Installed")
chart6_data = df_filtered[
    ["Project Name", "Square Footage Installed"]
].sort_values("Square Footage Installed", ascending=True)
fig6 = go.Figure(
    data=[
        go.Bar(
            x=chart6_data["Square Footage Installed"],
            y=chart6_data["Project Name"],
            orientation="h",
            marker_color="#667eea",
        )
    ]
)
fig6.update_layout(
    height=400,
    showlegend=False,
    hovermode="closest",
)
st.plotly_chart(fig6, use_container_width=True)

# Data Table
st.markdown("---")
st.subheader("📋 Project Details")
st.dataframe(df_filtered, use_container_width=True, height=400)

# Footer
st.markdown("---")
st.markdown(
    "### 🎵 Echo Friendly Acoustics Dashboard | Real-time Interactive Reporting"
)
