import pandas as pd
import numpy as np
import os

from pandas.core.interchange.dataframe_protocol import DataFrame

from supply_chain_analysis.scripts.inventory_optimization import inventory_df


def generate_synthetic_data(df, seed=None):
    # Set seed if inputted
    if seed is not None:
        np.random.seed(seed)

    # Define date range (12 months)
    months = pd.date_range(start='2024-01-01', periods=12, freq='MS')

    # Establish synthetic demand rows
    synthetic_demand = []

    for _, row in df.iterrows():
        sku = row['SKU']
        base_demand = row['Monthly Demand']

        for month in months:
            # Simulate with 10% noise
            simulated = base_demand + np.random.normal(0, base_demand * 0.1)
            synthetic_demand.append({
                "SKU": sku,
                "date": month,
                "demand": max(0, round(simulated))  # No negative demand
            })

    # Create synthetic df
    synthetic_df = pd.DataFrame(synthetic_demand)

    return synthetic_df

# create csv
synthetic_df = generate_synthetic_data(inventory_df)

# save as csv
output_path = "../data/processed/synthetic_monthly.csv"


if __name__ == "__main__":
    if not os.path.exists(output_path):
        df = generate_synthetic_data()
        df.to_csv(output_path, index=False)
        print("Data generated and saved.")
    else:
        print("File already exists, skipping generation.")


