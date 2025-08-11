
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add the project root to the Python path to enable module imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from balloonberg.pipeline import run_pipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="Industry Signal Generator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Bloomberg-style CSS ---
def apply_bloomberg_style():
    st.markdown("""
    <style>
    .stApp {
        background-color: #1A2525;
        color: white;
    }
    h1, h2, h3, h4 {
        color: #FFC107;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .card {
        background-color: #1E2C2C;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #2A3535;
    }
    .stDataFrame {
        font-family: monospace;
        font-size: 14px;
    }
    .metric-container {
        background-color: #1E2C2C;
        border-radius: 5px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #2A3535;
        text-align: center;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #AAAAAA;
    }
    .metric-value {
        font-size: 1.5rem;
        font-family: monospace;
        font-weight: bold;
    }
    .success { color: #00FF00; }
    .danger { color: #FF4500; }
    .neutral { color: #AAAAAA; }
    </style>
    """, unsafe_allow_html=True)

apply_bloomberg_style()

# --- Header ---
st.title("Industry Signal Generator")
st.markdown("Utilizing K-Means clustering on fundamental and technical data to identify industry-level trade signals.")

# --- Data Pipeline ---
@st.cache_data
def get_data():
    """Runs the analysis pipeline and caches the results."""
    industry_df, stock_df = run_pipeline()
    return industry_df, stock_df

industry_signals_df, stock_signals_df = get_data()

if industry_signals_df.empty:
    st.error("The analysis pipeline failed to produce results. Please check the console for errors.")
else:
    # --- UI Tabs ---
    tab1, tab2 = st.tabs(["Industry & Stock Signals", "Cluster Analysis"])

    # --- Industry Signals Tab ---
    with tab1:
        st.header("Industry Signal Overview")
        
        col1, col2, col3 = st.columns(3)
        signal_counts = industry_signals_df["Signal"].value_counts()
        
        with col1:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Strong Longs</div><div class='metric-value success'>{signal_counts.get('Strong Long', 0)}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Strong Shorts</div><div class='metric-value danger'>{signal_counts.get('Strong Short', 0)}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Neutral</div><div class='metric-value neutral'>{signal_counts.get('Neutral', 0)}</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        
        st.subheader("Industry-Level Signals")
        
        def style_signals(val):
            if val == "Strong Long":
                return 'color: #00FF00'
            elif val == "Strong Short":
                return 'color: #FF4500'
            else:
                return 'color: #AAAAAA'

        display_cols_industry = ["Industry", "Signal", "Cluster", "ROE", "Debt to Equity", "Volatility", "Return 3M"]
        st.dataframe(
            industry_signals_df[display_cols_industry].style.applymap(style_signals, subset=['Signal']),
            use_container_width=True
        )
        
        st.markdown("---")
        st.header("Stock-Level Drill-Down")
        
        # Dropdown to select an industry
        industries = ["All"] + sorted(industry_signals_df["Industry"].unique().tolist())
        selected_industry = st.selectbox("Select an Industry to see its companies:", industries)
        
        # Filter stocks based on selection
        if selected_industry == "All":
            display_stocks = stock_signals_df
        else:
            display_stocks = stock_signals_df[stock_signals_df["Industry"] == selected_industry]
        
        st.subheader(f"Displaying Companies for: {selected_industry}")
        display_cols_stocks = ["Symbol", "Industry", "Signal", "Current Price", "Market Cap", "ROE", "Debt to Equity", "Volatility"]
        st.dataframe(
            display_stocks[display_cols_stocks].style.applymap(style_signals, subset=['Signal']),
            use_container_width=True
        )


    # --- Cluster Analysis Tab ---
    with tab2:
        st.header("Industry Cluster Visualization")
        st.markdown("This plot shows how industries are clustered based on their financial profiles. Hover over a point to see the industry name.")

        fig = px.scatter(
            industry_signals_df,
            x="ROE",
            y="Debt to Equity",
            color="Cluster",
            size="Market Cap",
            hover_name="Industry",
            text="Industry",
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Industry Clusters: ROE vs. Debt to Equity"
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#1E2C2C",
            font_color="white",
            xaxis_title="Return on Equity (ROE %)",
            yaxis_title="Debt to Equity Ratio"
        )
        st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown(
    "<footer style='margin-top:20px;padding:10px;border-top:1px solid #2A3535;font-size:12px;color:#AAAAAA;text-align:center;'>"
    "Powered by a K-Means Clustering Model | August 2025"
    "</footer>",
    unsafe_allow_html=True
)
