

import sys
from pathlib import Path
import pandas as pd

# Add the project root to the Python path to enable module imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from balloonberg.data import load_portfolio_data, aggregate_by_industry
from balloonberg.analysis import perform_clustering, generate_cluster_signals

def run_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    # 1. Load data
    stock_df = load_portfolio_data()
    if stock_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # 2. Aggregate by industry
    industry_df = aggregate_by_industry(stock_df)
    if industry_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # 3. Perform clustering
    try:
        clustered_df = perform_clustering(industry_df)
    except ValueError as e:
        print(f"Error during clustering: {e}")
        return pd.DataFrame(), pd.DataFrame()

    # 4. Generate signals
    industry_signals_df = generate_cluster_signals(clustered_df)

    # 5. Merge signals back to original stock data
    stock_df_with_signals = pd.merge(
        stock_df,
        industry_signals_df[["Industry", "Signal", "Cluster"]],
        on="Industry",
        how="left"
    )

    print("\n--- Pipeline Complete ---")
    
    return industry_signals_df, stock_df_with_signals

if __name__ == "__main__":
    industry_results, stock_results = run_pipeline()
    if not industry_results.empty:
        print("\n--- Final Industry Signals ---")
        print(industry_results[["Industry", "Signal", "Cluster", "ROE", "Debt to Equity"]])
        print("\n--- Stocks with Signals (Sample) ---")
        print(stock_results.head())


