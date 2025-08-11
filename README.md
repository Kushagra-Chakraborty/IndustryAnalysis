# Industry Signal Generator

## Overview
The Industry Signal Generator is a Streamlit-based application that leverages K-Means clustering on fundamental and technical financial data to identify industry-level trade signals. It provides insights into market trends by categorizing industries into "Strong Long," "Strong Short," or "Neutral" signals.

## Features
- **Industry-Level Signals:** Identifies and displays trade signals for various industries based on their clustered financial profiles.
- **Stock-Level Drill-Down:** Allows users to select an industry and view the individual stock signals within that industry.
- **Interactive Cluster Visualization:** Provides a scatter plot showing how industries are clustered based on metrics like Return on Equity (ROE) and Debt to Equity, with interactive hover details.
- **Bloomberg-Style UI:** Features a custom user interface designed to mimic the aesthetic of Bloomberg terminals.

## Tech Stack
- Python
- Streamlit (for the web application framework)
- Pandas (for data manipulation and analysis)
- Plotly Express (for interactive visualizations)
- K-Means Clustering (implied by the application's core logic, likely from scikit-learn or similar library)

## Setup and Installation

To run this application locally, follow these steps:

1.  **Clone the repository** (if applicable, or ensure you have the project files).
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install streamlit pandas plotly
    ```
    *Note: Ensure that the `balloonberg.pipeline` module and its dependencies are correctly set up and accessible. This module is responsible for the data processing and clustering.*

## How to Run


```bash
streamlit run app.py
```

This will open the application in your default web browser.

## Usage

The application features two main tabs:

-   **Industry & Stock Signals:** View an overview of industry-level signals and drill down to see individual stock signals within selected industries.
-   **Cluster Analysis:** Explore an interactive scatter plot visualizing how industries are grouped into clusters based on their financial characteristics.

## Data Pipeline
The application relies on an internal data pipeline (`balloonberg.pipeline.run_pipeline`) which is responsible for fetching, processing, and clustering the financial data. Ensure this pipeline is correctly configured and has access to its required data sources.


