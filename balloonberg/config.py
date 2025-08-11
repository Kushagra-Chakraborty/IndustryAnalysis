
from pathlib import Path

# --- Directories ---
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output" # For saving results

# --- File Paths ---
PORTFOLIO_DATA_PATH = DATA_DIR / "nifty_500_validated_v19.csv"

# --- Analysis Features ---
# Features to be used for clustering
FUNDAMENTAL_FEATURES = [
    "Stock P/E",
    "ROE",
    "Debt to Equity",
    "Market Cap",
    "Dividend Yield",
    "ROCE"
]

TECHNICAL_FEATURES = [
    "Volatility",
    "Return 3M"
]

# Combine features
ALL_FEATURES = FUNDAMENTAL_FEATURES + TECHNICAL_FEATURES

# --- Model Parameters ---
N_CLUSTERS = 6  # Using 6 as a starting point, can be tuned
RANDOM_STATE = 42

