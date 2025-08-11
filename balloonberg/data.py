
import pandas as pd
from balloonberg import config
import numpy as np

def load_portfolio_data() -> pd.DataFrame:
    """Loads the portfolio data from the path specified in the config."""
    try:
        df = pd.read_csv(config.PORTFOLIO_DATA_PATH)
        print(f"Successfully loaded data from {config.PORTFOLIO_DATA_PATH}")
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {config.PORTFOLIO_DATA_PATH}")
        return pd.DataFrame()

def aggregate_by_industry(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates stock data by industry, calculating the mean for numeric features.
    """
    # Select only numeric columns for aggregation
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # Ensure features from config are present and numeric
    features_to_agg = [f for f in config.ALL_FEATURES if f in numeric_cols]
    
    if not features_to_agg:
        print("Error: No numeric features found for aggregation.")
        return pd.DataFrame()

    # Group by industry and calculate the mean
    industry_df = df.groupby("Industry")[features_to_agg].mean()
    
    print(f"Aggregated data into {len(industry_df)} industries.")
    return industry_df.reset_index()

