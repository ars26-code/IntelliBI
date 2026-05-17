"""
IntelliBI – AI-Driven Business Intelligence and Visualization Platform
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import re
import io
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IntelliBI – AI Business Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #00F5A0;
        --accent: #00D4FF;
        --bg-dark: #0A0E1A;
        --bg-card: #111827;
        --bg-card2: #1A2236;
        --text: #E8EDF5;
        --text-muted: #8892A4;
        --border: #1E2D45;
        --danger: #FF4D6D;
        --warning: #FFB347;
    }

    .stApp {
        background: var(--bg-dark);
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    /* Hide default streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }

    /* Top Banner */
    .intellibi-banner {
        background: linear-gradient(135deg, #0A0E1A 0%, #111827 50%, #0D1B2A 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .intellibi-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(0,245,160,0.06) 0%, transparent 70%);
        border-radius: 50%;
    }
    .intellibi-banner::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: 20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0,212,255,0.04) 0%, transparent 70%);
        border-radius: 50%;
    }
    .banner-title {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00F5A0, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .banner-sub {
        font-size: 0.9rem;
        color: var(--text-muted);
        margin-top: 6px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    .banner-badge {
        display: inline-block;
        background: rgba(0,245,160,0.1);
        border: 1px solid rgba(0,245,160,0.3);
        color: var(--primary);
        font-size: 0.7rem;
        font-family: 'Space Mono', monospace;
        padding: 3px 10px;
        border-radius: 20px;
        margin-top: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); border-color: rgba(0,245,160,0.3); }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
    }
    .kpi-card.green::before { background: linear-gradient(90deg, #00F5A0, #00D4FF); }
    .kpi-card.blue::before { background: linear-gradient(90deg, #00D4FF, #7B61FF); }
    .kpi-card.red::before { background: linear-gradient(90deg, #FF4D6D, #FF8C42); }
    .kpi-card.yellow::before { background: linear-gradient(90deg, #FFB347, #FFD700); }
    .kpi-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-family: 'Space Mono', monospace;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        margin-top: 6px;
        font-family: 'Space Mono', monospace;
        letter-spacing: -1px;
    }
    .kpi-delta {
        font-size: 0.78rem;
        margin-top: 4px;
        font-weight: 500;
    }
    .kpi-icon {
        position: absolute;
        top: 16px; right: 18px;
        font-size: 1.6rem;
        opacity: 0.3;
    }

    /* Section Headers */
    .section-header {
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--primary);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* Chart Container */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Insight Cards */
    .insight-card {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--primary);
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        line-height: 1.6;
        color: var(--text);
    }
    .insight-card.warning { border-left-color: var(--warning); }
    .insight-card.danger { border-left-color: var(--danger); }

    /* Chat Bubble */
    .chat-user {
        background: rgba(0,212,255,0.08);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 12px 12px 4px 12px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.88rem;
        color: #B0E0FF;
        max-width: 75%;
        margin-left: auto;
        text-align: right;
    }
    .chat-bot {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-radius: 12px 12px 12px 4px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.88rem;
        color: var(--text);
        max-width: 85%;
        line-height: 1.6;
    }
    .chat-bot strong { color: var(--primary); }
    .chat-label {
        font-size: 0.68rem;
        color: var(--text-muted);
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
    }
    .sidebar-logo {
        font-family: 'Space Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00F5A0, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 10px 0;
    }

    /* Streamlit overrides */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: var(--bg-card2) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }
    .stTextInput > div > div > input {
        background: var(--bg-card2) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }
    .stDataFrame { background: var(--bg-card) !important; }
    .stButton > button {
        background: linear-gradient(135deg, #00F5A0, #00D4FF) !important;
        color: #0A0E1A !important;
        border: none !important;
        font-weight: 700 !important;
        font-family: 'Space Mono', monospace !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.5px !important;
        padding: 8px 20px !important;
    }
    .stButton > button:hover {
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
    }
    div[data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 16px;
    }
    .status-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--primary);
        display: inline-block;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
</style>
""", unsafe_allow_html=True)

# ─── DATA FETCH ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_api_data():
    """Fetch products from FakeStore API with caching (60s TTL)."""
    try:
        resp = requests.get("https://fakestoreapi.com/products", timeout=10)
        resp.raise_for_status()
        products = resp.json()
        df = pd.DataFrame(products)
        df = df.rename(columns={"id": "product_id", "title": "product_name",
                                  "price": "price", "category": "category",
                                  "description": "description"})
        # Simulate quantity and date fields
        np.random.seed(42)
        df["quantity"] = np.random.randint(10, 200, size=len(df))
        base_date = datetime(2024, 1, 1)
        df["date"] = [base_date + timedelta(days=int(i*10)) for i in range(len(df))]
        return df, None
    except Exception as e:
        return None, str(e)

# ─── PREPROCESSING ───────────────────────────────────────────────────────────────
def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean, validate, and enrich a dataframe with business metrics."""
    df = df.copy()

    # Lowercase columns
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Coerce numeric columns
    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass

    # Fill missing numerics with median
    num_cols = df.select_dtypes(include=np.number).columns
    for col in num_cols:
        df[col].fillna(df[col].median(), inplace=True)

    # Fill missing strings with 'Unknown'
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col].fillna("Unknown", inplace=True)

    # Derive price
    if "price" not in df.columns:
        if "unit_price" in df.columns:
            df["price"] = df["unit_price"]
        elif "amount" in df.columns:
            df["price"] = df["amount"]
        else:
            df["price"] = np.random.uniform(10, 500, size=len(df))

    # Derive quantity
    if "quantity" not in df.columns:
        if "qty" in df.columns:
            df["quantity"] = df["qty"]
        elif "units" in df.columns:
            df["quantity"] = df["units"]
        else:
            df["quantity"] = np.random.randint(10, 200, size=len(df))

    # Derive financials
    if "sales" not in df.columns:
        df["sales"] = df["price"] * df["quantity"]
    if "cost" not in df.columns:
        df["cost"] = df["sales"] * 0.7
    if "profit" not in df.columns:
        df["profit"] = df["sales"] - df["cost"]
    if "profit_margin" not in df.columns:
        df["profit_margin"] = (df["profit"] / df["sales"].replace(0, np.nan) * 100).fillna(0)

    # Detect category column
    if "category" not in df.columns:
        cat_candidates = [c for c in df.columns if c in ["type", "department", "segment", "group"]]
        if cat_candidates:
            df["category"] = df[cat_candidates[0]]
        else:
            df["category"] = "General"

    # Detect product name column
    if "product_name" not in df.columns:
        name_candidates = [c for c in df.columns if c in ["name", "product", "item", "title"]]
        if name_candidates:
            df["product_name"] = df[name_candidates[0]]
        else:
            df["product_name"] = [f"Product {i+1}" for i in range(len(df))]

    # Parse date column if available
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce").fillna(0)
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(0)

    return df

# ─── INSIGHTS ENGINE ─────────────────────────────────────────────────────────────
def generate_insights(df: pd.DataFrame) -> dict:
    """Generate AI-style business insights from the processed dataframe."""
    insights = {}

    # Top / Bottom products
    prod_group = df.groupby("product_name").agg(
        sales=("sales", "sum"), profit=("profit", "sum"),
        margin=("profit_margin", "mean")
    ).reset_index()

    insights["top5_profit"] = prod_group.nlargest(5, "profit")
    insights["bottom5_profit"] = prod_group.nsmallest(5, "profit")

    # Category analysis
    cat_group = df.groupby("category").agg(
        sales=("sales", "sum"), profit=("profit", "sum"),
        margin=("profit_margin", "mean"), products=("product_name", "count")
    ).reset_index().sort_values("sales", ascending=False)

    insights["best_category"] = cat_group.iloc[0]["category"] if len(cat_group) > 0 else "N/A"
    insights["worst_category"] = cat_group.iloc[-1]["category"] if len(cat_group) > 0 else "N/A"
    insights["category_analysis"] = cat_group

    # KPIs
    insights["total_sales"] = df["sales"].sum()
    insights["total_profit"] = df["profit"].sum()
    insights["total_cost"] = df["cost"].sum() if "cost" in df.columns else 0
    insights["total_loss"] = abs(df[df["profit"] < 0]["profit"].sum())
    insights["avg_margin"] = df["profit_margin"].mean()
    insights["profitable_count"] = (df["profit"] > 0).sum()
    insights["loss_count"] = (df["profit"] < 0).sum()

    # Outlier detection (IQR method)
    Q1 = df["sales"].quantile(0.25)
    Q3 = df["sales"].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df["sales"] < Q1 - 1.5 * IQR) | (df["sales"] > Q3 + 1.5 * IQR)]
    insights["outliers"] = outliers
    insights["outlier_count"] = len(outliers)

    # Trend data (if date available)
    if "date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["date"]):
        df_dated = df.dropna(subset=["date"])
        if len(df_dated) > 0:
            trend = df_dated.groupby(df_dated["date"].dt.to_period("M")).agg(
                sales=("sales", "sum"), profit=("profit", "sum")
            ).reset_index()
            trend["date"] = trend["date"].astype(str)
            insights["trend"] = trend
        else:
            insights["trend"] = None
    else:
        insights["trend"] = None

    return insights

# ─── CHART HELPERS ───────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(17,24,39,0)",
    plot_bgcolor="rgba(17,24,39,0)",
    font=dict(family="DM Sans", color="#E8EDF5"),
    margin=dict(l=20, r=20, t=40, b=20),
)

def chart_bar_category(df):
    cat = df.groupby("category")["sales"].sum().reset_index().sort_values("sales", ascending=False)
    fig = px.bar(cat, x="category", y="sales", color="sales",
                 color_continuous_scale=["#00D4FF", "#00F5A0"],
                 title="📊 Category vs Total Sales")
    fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                      title_font_size=14, title_font_color="#00F5A0")
    fig.update_traces(marker_line_width=0)
    return fig

def chart_profit_bar(df):
    cat = df.groupby("category")["profit"].sum().reset_index().sort_values("profit", ascending=False)
    colors = ["#00F5A0" if v >= 0 else "#FF4D6D" for v in cat["profit"]]
    fig = go.Figure(go.Bar(x=cat["category"], y=cat["profit"],
                           marker_color=colors, marker_line_width=0))
    fig.update_layout(**PLOTLY_THEME, title="💰 Category vs Profit",
                      title_font_size=14, title_font_color="#00F5A0")
    return fig

def chart_pie_distribution(df):
    cat = df.groupby("category")["sales"].sum().reset_index()
    fig = px.pie(cat, values="sales", names="category",
                 color_discrete_sequence=px.colors.sequential.Teal,
                 hole=0.45, title="🍩 Sales Distribution by Category")
    fig.update_layout(**PLOTLY_THEME, title_font_size=14, title_font_color="#00F5A0")
    fig.update_traces(textfont_color="white")
    return fig

def chart_trend(trend_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=trend_df["date"], y=trend_df["sales"],
                         name="Sales", marker_color="rgba(0,212,255,0.6)"), secondary_y=False)
    fig.add_trace(go.Scatter(x=trend_df["date"], y=trend_df["profit"],
                             name="Profit", line=dict(color="#00F5A0", width=2.5),
                             mode="lines+markers"), secondary_y=True)
    fig.update_layout(**PLOTLY_THEME, title="📈 Monthly Sales & Profit Trend",
                      title_font_size=14, title_font_color="#00F5A0",
                      legend=dict(orientation="h", y=1.1))
    return fig

def chart_scatter_outliers(df):
    df2 = df.copy()
    Q1, Q3 = df2["sales"].quantile(0.25), df2["sales"].quantile(0.75)
    IQR = Q3 - Q1
    df2["is_outlier"] = ((df2["sales"] < Q1 - 1.5*IQR) | (df2["sales"] > Q3 + 1.5*IQR))
    color_map = {True: "#FF4D6D", False: "#00D4FF"}
    fig = px.scatter(df2, x="price", y="sales", color="is_outlier",
                     color_discrete_map=color_map,
                     hover_data=["product_name", "category"],
                     title="🔍 Sales Outlier Detection",
                     labels={"is_outlier": "Outlier"})
    fig.update_layout(**PLOTLY_THEME, title_font_size=14, title_font_color="#00F5A0")
    return fig

def chart_top_products(insights):
    top5 = insights["top5_profit"]
    fig = px.bar(top5, x="profit", y="product_name", orientation="h",
                 color="profit", color_continuous_scale=["#00D4FF", "#00F5A0"],
                 title="🏆 Top 5 Profitable Products")
    fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                      yaxis=dict(autorange="reversed"),
                      title_font_size=14, title_font_color="#00F5A0")
    return fig

# ─── CHAT ENGINE ─────────────────────────────────────────────────────────────────
def chat_respond(query: str, df: pd.DataFrame, insights: dict) -> str:
    """Rule-based NLP chat engine that maps natural language to pandas operations."""
    q = query.lower().strip()

    # ── Total metrics ──
    if re.search(r"total.sales|sales.total|sum.sales|overall.sales", q):
        return f"**Total Sales:** ${insights['total_sales']:,.2f}"

    if re.search(r"total.profit|profit.total|sum.profit|overall.profit", q):
        return f"**Total Profit:** ${insights['total_profit']:,.2f}"

    if re.search(r"total.loss|loss.total|sum.loss", q):
        return f"**Total Loss:** ${insights['total_loss']:,.2f}"

    if re.search(r"profit.margin|avg.margin|average.margin|margin", q):
        return f"**Average Profit Margin:** {insights['avg_margin']:.1f}%"

    # ── Best / Worst ──
    if re.search(r"highest.profit|most.profit|best.product|top.product", q):
        row = insights["top5_profit"].iloc[0]
        return f"**Highest Profit Product:** {row['product_name']}\n\n💰 Profit: **${row['profit']:,.2f}** | Sales: **${row['sales']:,.2f}**"

    if re.search(r"lowest.profit|worst.product|least.profit|loss.product", q):
        row = insights["bottom5_profit"].iloc[0]
        return f"**Lowest Profit Product:** {row['product_name']}\n\n📉 Profit: **${row['profit']:,.2f}** | Sales: **${row['sales']:,.2f}**"

    if re.search(r"best.categor|top.categor|highest.categor", q):
        return f"**Best Performing Category:** {insights['best_category']}"

    if re.search(r"worst.categor|bottom.categor|lowest.categor", q):
        return f"**Worst Performing Category:** {insights['worst_category']}"

    # ── Top N products ──
    m = re.search(r"top\s*(\d+)\s*product", q)
    if m:
        n = int(m.group(1))
        top = insights["top5_profit"].head(n)
        lines = "\n".join([f"{i+1}. **{r['product_name']}** — Profit: ${r['profit']:,.2f}" for i, r in top.iterrows()])
        return f"**Top {n} Products by Profit:**\n\n{lines}"

    # ── Top N categories ──
    m = re.search(r"top\s*(\d+)\s*categor", q)
    if m:
        n = int(m.group(1))
        top = insights["category_analysis"].head(n)
        lines = "\n".join([f"{i+1}. **{r['category']}** — Sales: ${r['sales']:,.2f}" for i, r in top.iterrows()])
        return f"**Top {n} Categories by Sales:**\n\n{lines}"

    # ── Count queries ──
    if re.search(r"how many.product|number of product|count.product|total product", q):
        n = df["product_name"].nunique()
        return f"**Total Products:** {n}"

    if re.search(r"how many.categor|number of categor|count.categor|total categor", q):
        n = df["category"].nunique()
        return f"**Total Categories:** {n}"

    if re.search(r"how many.row|how many.record|total record|dataset size|number of row", q):
        return f"**Dataset Size:** {len(df):,} rows × {len(df.columns)} columns"

    # ── Outliers ──
    if re.search(r"outlier|anomal|unusual", q):
        n = insights["outlier_count"]
        return f"**Anomaly Detection Result:** {n} outlier(s) detected in sales data using the IQR method."

    # ── Category-specific ──
    for cat in df["category"].unique():
        if cat.lower() in q:
            sub = df[df["category"].str.lower() == cat.lower()]
            s = sub["sales"].sum()
            p = sub["profit"].sum()
            m_pct = sub["profit_margin"].mean()
            return (f"**Category: {cat}**\n\n"
                    f"• Sales: **${s:,.2f}**\n"
                    f"• Profit: **${p:,.2f}**\n"
                    f"• Avg Margin: **{m_pct:.1f}%**\n"
                    f"• Products: **{sub['product_name'].nunique()}**")

    # ── Price queries ──
    if re.search(r"avg.price|average.price|mean.price", q):
        return f"**Average Price:** ${df['price'].mean():,.2f}"

    if re.search(r"max.price|highest.price|most.expensive", q):
        row = df.loc[df["price"].idxmax()]
        return f"**Most Expensive:** {row.get('product_name', 'N/A')} at **${row['price']:,.2f}**"

    if re.search(r"min.price|lowest.price|cheapest", q):
        row = df.loc[df["price"].idxmin()]
        return f"**Cheapest:** {row.get('product_name', 'N/A')} at **${row['price']:,.2f}**"

    # ── Summary ──
    if re.search(r"summary|overview|report|tell me about|insight", q):
        return (f"**📊 Dataset Summary**\n\n"
                f"• Records: **{len(df):,}** | Categories: **{df['category'].nunique()}**\n"
                f"• Total Sales: **${insights['total_sales']:,.2f}**\n"
                f"• Total Profit: **${insights['total_profit']:,.2f}**\n"
                f"• Avg Margin: **{insights['avg_margin']:.1f}%**\n"
                f"• Best Category: **{insights['best_category']}**\n"
                f"• Profitable Products: **{insights['profitable_count']}** | Loss-making: **{insights['loss_count']}**")

    # ── Columns ──
    if re.search(r"column|field|attribute|variable", q):
        cols = ", ".join(df.columns.tolist())
        return f"**Available Columns ({len(df.columns)}):**\n\n{cols}"

    # ── Fallback ──
    return ("🤖 I didn't quite catch that. Try asking:\n\n"
            "• *\"What is total sales?\"*\n"
            "• *\"Which product has highest profit?\"*\n"
            "• *\"Show top 3 categories\"*\n"
            "• *\"What is the profit margin?\"*\n"
            "• *\"How many products are there?\"*\n"
            "• *\"Give me a summary\"*")

# ─── KPI HTML ────────────────────────────────────────────────────────────────────
def kpi_card(label, value, delta=None, color="green", icon="💡"):
    delta_html = f'<div class="kpi-delta" style="color:{"#00F5A0" if delta and "▲" in delta else "#FF4D6D" if delta else "#8892A4"}">{delta or ""}</div>' if delta else ""
    return f"""
    <div class="kpi-card {color}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

# ─── MAIN APP ────────────────────────────────────────────────────────────────────
def main():
    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🧠 IntelliBI</div>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### 📡 Data Source")
        source = st.selectbox("Choose Source", ["🌐 FakeStore API (Live)", "📁 Upload CSV"])

        df_raw = None
        api_error = None

        if source == "🌐 FakeStore API (Live)":
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()
            df_raw, api_error = fetch_api_data()
        else:
            uploaded = st.file_uploader("Upload CSV", type=["csv"])
            if uploaded:
                try:
                    df_raw = pd.read_csv(uploaded)
                    st.success(f"✅ Loaded {len(df_raw)} rows")
                except Exception as e:
                    st.error(f"❌ Error reading CSV: {e}")

        if df_raw is None and api_error is None and source.startswith("📁"):
            st.info("Please upload a CSV file to begin.")

        st.markdown("---")

        # Filters (shown after data load)
        df_filtered = None
        if df_raw is not None:
            df_proc = preprocess_dataframe(df_raw)

            st.markdown("### 🔍 Filters")
            categories = ["All"] + sorted(df_proc["category"].unique().tolist())
            selected_cats = st.multiselect("Category", categories[1:], default=categories[1:])

            price_min = float(df_proc["price"].min())
            price_max = float(df_proc["price"].max())
            price_range = st.slider("Price Range ($)", price_min, price_max,
                                    (price_min, price_max), step=0.5)

            # Apply filters
            df_filtered = df_proc.copy()
            if selected_cats:
                df_filtered = df_filtered[df_filtered["category"].isin(selected_cats)]
            df_filtered = df_filtered[
                (df_filtered["price"] >= price_range[0]) &
                (df_filtered["price"] <= price_range[1])
            ]

            st.markdown("---")
            st.markdown("### 💾 Export")
            csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv_bytes, "intellibi_data.csv", "text/csv")

    # ── MAIN AREA ──
    # Banner
    st.markdown("""
    <div class="intellibi-banner">
        <p class="banner-title">🧠 IntelliBI</p>
        <p class="banner-sub">AI-Driven Business Intelligence & Visualization Platform</p>
        <span class="banner-badge"><span class="status-dot"></span> Live Analytics Engine</span>
    </div>
    """, unsafe_allow_html=True)

    if api_error:
        st.error(f"⚠️ API Error: {api_error}. Try uploading a CSV instead.")
        return

    if df_raw is None:
        st.markdown("""
        <div style="text-align:center; padding: 80px 20px; color: #8892A4;">
            <div style="font-size:4rem;">📊</div>
            <h2 style="color:#E8EDF5; font-family:'Space Mono',monospace;">Welcome to IntelliBI</h2>
            <p>Select a data source from the sidebar to start your analysis.</p>
            <p style="font-size:0.85rem;">✅ Live API data  &nbsp;|&nbsp; ✅ CSV upload  &nbsp;|&nbsp; ✅ AI insights  &nbsp;|&nbsp; ✅ Natural language chat</p>
        </div>
        """, unsafe_allow_html=True)
        return

    if df_filtered is None or len(df_filtered) == 0:
        st.warning("No data matches your current filters. Please adjust the sidebar filters.")
        return

    insights = generate_insights(df_filtered)

    # ── KPI CARDS ──
    st.markdown('<div class="section-header">📌 Key Performance Indicators</div>', unsafe_allow_html=True)
    kpis_html = f"""
    <div class="kpi-grid">
        {kpi_card("Total Sales", f"${insights['total_sales']:,.0f}", "▲ All Products", "green", "💵")}
        {kpi_card("Total Profit", f"${insights['total_profit']:,.0f}", "▲ Net Gain", "blue", "📈")}
        {kpi_card("Total Loss", f"${insights['total_loss']:,.0f}", "▼ Loss-making SKUs", "red", "📉")}
        {kpi_card("Avg Margin", f"{insights['avg_margin']:.1f}%", "▲ Profit Margin", "yellow", "🎯")}
    </div>
    """
    st.markdown(kpis_html, unsafe_allow_html=True)

    # ── CHARTS ROW 1 ──
    st.markdown('<div class="section-header">📊 Sales Analytics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(chart_bar_category(df_filtered), use_container_width=True)
    with col2:
        st.plotly_chart(chart_profit_bar(df_filtered), use_container_width=True)

    # ── CHARTS ROW 2 ──
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(chart_pie_distribution(df_filtered), use_container_width=True)
    with col4:
        if insights["trend"] is not None and len(insights["trend"]) > 1:
            st.plotly_chart(chart_trend(insights["trend"]), use_container_width=True)
        else:
            st.plotly_chart(chart_scatter_outliers(df_filtered), use_container_width=True)

    # ── CHARTS ROW 3 ──
    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(chart_top_products(insights), use_container_width=True)
    with col6:
        # Bottom 5
        bot5 = insights["bottom5_profit"]
        fig = px.bar(bot5, x="profit", y="product_name", orientation="h",
                     color="profit", color_continuous_scale=["#FF4D6D", "#FFB347"],
                     title="⚠️ Bottom 5 Loss-Making Products")
        fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                          yaxis=dict(autorange="reversed"),
                          title_font_size=14, title_font_color="#FF4D6D")
        st.plotly_chart(fig, use_container_width=True)

    # ── AI INSIGHTS ──
    st.markdown('<div class="section-header">🤖 AI-Generated Insights</div>', unsafe_allow_html=True)

    cat_df = insights["category_analysis"]
    best_cat_row = cat_df.iloc[0] if len(cat_df) > 0 else None
    worst_cat_row = cat_df.iloc[-1] if len(cat_df) > 0 else None

    insight_items = [
        ("green", f"🏆 <b>Top Product:</b> {insights['top5_profit'].iloc[0]['product_name']} with profit of ${insights['top5_profit'].iloc[0]['profit']:,.2f} and {insights['top5_profit'].iloc[0]['margin']:.1f}% margin."),
        ("green", f"📦 <b>Best Category:</b> {insights['best_category']} leads in overall sales performance across the portfolio." if best_cat_row is not None else ""),
        ("warning", f"⚠️ <b>Worst Category:</b> {insights['worst_category']} is underperforming. Consider reviewing pricing or product mix." if worst_cat_row is not None else ""),
        ("green", f"💰 <b>Profitability:</b> {insights['profitable_count']} products are profitable while {insights['loss_count']} are loss-making."),
        ("warning" if insights["outlier_count"] > 0 else "green",
         f"🔍 <b>Anomalies:</b> {insights['outlier_count']} outlier(s) detected in sales data via IQR analysis — review for data integrity or business opportunities."),
        ("green", f"📊 <b>Margin Health:</b> Average profit margin is {insights['avg_margin']:.1f}%. {'Strong performance!' if insights['avg_margin'] > 25 else 'Room for margin improvement.' if insights['avg_margin'] > 10 else 'Margins need attention.'}"),
    ]

    for style, text in insight_items:
        if text:
            st.markdown(f'<div class="insight-card {style if style != "green" else ""}">{text}</div>', unsafe_allow_html=True)

    # ── DATA PREVIEW ──
    st.markdown('<div class="section-header">🗂️ Data Preview</div>', unsafe_allow_html=True)
    preview_cols = [c for c in ["product_name", "category", "price", "quantity", "sales", "profit", "profit_margin"] if c in df_filtered.columns]
    display_df = df_filtered[preview_cols].copy()
    for col in ["sales", "profit", "price"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
    if "profit_margin" in display_df.columns:
        display_df["profit_margin"] = display_df["profit_margin"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(display_df.head(50), use_container_width=True, height=280)

    # ── CHAT SECTION ──
    st.markdown("---")
    st.markdown('<div class="section-header">💬 AI Data Chat</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(0,212,255,0.04); border:1px solid rgba(0,212,255,0.15); border-radius:10px; padding:12px 16px; margin-bottom:16px; font-size:0.82rem; color:#8892A4;">
        💡 Ask questions like: <em>"What is total sales?"</em> &nbsp;|&nbsp; <em>"Which product has highest profit?"</em> &nbsp;|&nbsp; <em>"Show top 3 categories"</em> &nbsp;|&nbsp; <em>"Give me a summary"</em>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-label" style="text-align:right; margin-right:4px;">You</div><div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-label" style="margin-left:4px;">🧠 IntelliBI</div><div class="chat-bot">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input("", placeholder="Ask anything about your data...",
                                   label_visibility="collapsed", key="chat_input")
    with col_send:
        send_clicked = st.button("Send ➤")

    if send_clicked and user_input.strip():
        response = chat_respond(user_input, df_filtered, insights)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "bot", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    # ── FOOTER ──
    st.markdown("""
    <div style="text-align:center; padding: 30px 0 10px; font-size:0.75rem; color:#3A4A5C; font-family:'Space Mono',monospace; letter-spacing:1px;">
        INTELLIBI © 2025 &nbsp;|&nbsp; AI-POWERED BUSINESS INTELLIGENCE &nbsp;|&nbsp; BUILT WITH STREAMLIT
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
