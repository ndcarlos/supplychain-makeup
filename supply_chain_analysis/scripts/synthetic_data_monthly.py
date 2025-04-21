import pandas as pd
import numpy as np

from supply_chain_analysis.scripts.inventory_optimization import inventory_df

# Define date range (12 months)
months = pd.date_range(start='2024-01-01', periods=12, freq='M')

# Establish synthetic demand rows
synthetic_demand = []

for _, row in inventory_df.itrrows():
    sku = row['SKU']
    base_demand = row['number_of_products_sold']

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

synthetic_df.head()