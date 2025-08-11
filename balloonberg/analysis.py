
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from balloonberg import config

def perform_clustering(industry_df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs K-Means clustering on the aggregated industry data.
    """
    if "Industry" not in industry_df.columns:
        raise ValueError("Input DataFrame must contain an 'Industry' column.")

    # Prepare the data for clustering
    features = config.ALL_FEATURES
    df_cluster = industry_df.dropna(subset=features).copy()

    if len(df_cluster) < config.N_CLUSTERS:
        raise ValueError("Not enough data points to form the desired number of clusters after dropping NaNs.")

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster[features])

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=config.N_CLUSTERS, random_state=config.RANDOM_STATE, n_init=10)
    df_cluster["Cluster"] = kmeans.fit_predict(X_scaled)

    print(f"Successfully clustered industries into {config.N_CLUSTERS} clusters.")
    
    return df_cluster

def generate_cluster_signals(clustered_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes cluster characteristics and generates Long/Short/Neutral signals.
    """
    if "Cluster" not in clustered_df.columns:
        raise ValueError("Input DataFrame must contain a 'Cluster' column.")

    # Calculate the mean of features for each cluster
    cluster_summary = clustered_df.groupby("Cluster")[config.ALL_FEATURES].mean()
    print("\nCluster Summary (Averages):")
    print(cluster_summary)

    # Define signal personas based on quantiles
    roe_threshold_top = cluster_summary["ROE"].quantile(0.66)
    roe_threshold_bottom = cluster_summary["ROE"].quantile(0.33)
    debt_threshold_top = cluster_summary["Debt to Equity"].quantile(0.66)
    debt_threshold_bottom = cluster_summary["Debt to Equity"].quantile(0.33)

    def assign_signal(cluster_id):
        summary = cluster_summary.loc[cluster_id]
        if summary["ROE"] > roe_threshold_top and summary["Debt to Equity"] < debt_threshold_bottom:
            return "Strong Long"
        elif summary["ROE"] < roe_threshold_bottom and summary["Debt to Equity"] > debt_threshold_top:
            return "Strong Short"
        else:
            return "Neutral"

    # Map the signal to each cluster
    signal_map = {cluster_id: assign_signal(cluster_id) for cluster_id in cluster_summary.index}
    clustered_df["Signal"] = clustered_df["Cluster"].map(signal_map)

    print("\nAssigned signals to industries based on cluster profiles.")
    
    return clustered_df

