import pandas as pd
import numpy as np

from supply_chain_analysis.scripts.demand_forecasting import synthetic_df
from supply_chain_analysis.scripts.inventory_optimization import inventory_df

def generate_replenishment_plan(synthetic_df, inventory_df, z_score=1.65):
    # Assume 30 days in a month for conversion
    DAYS_IN_MONTH = 30

    # Calculate average demand per SKU
    demand_summary = synthetic_df.groupby('SKU')['demand'].agg(['mean', 'std']).reset_index()
    demand_summary.rename(columns={'mean': 'Avg Monthly Demand', 'std': 'Demand Std'}, inplace=True)

    # Merge in lead times and current stock
    demand_summary = demand_summary.merge(
        inventory_df[['SKU', 'Total Lead Time', 'Current Stock', 'Safety Stock']],
        on='SKU',
        how='left'
    )

    # Convert lead time from days to months
    demand_summary['Lead Time (Months)'] = demand_summary['Total Lead Time'] / DAYS_IN_MONTH

    # Calculate Reorder Point (ROP)
    demand_summary['ROP'] = np.round((demand_summary['Avg Monthly Demand'] * demand_summary['Lead Time (Months)']) + demand_summary['Safety Stock'],0)

    # Calculate recommended reorder qty
    demand_summary['Reorder Qty'] = demand_summary['ROP'] - demand_summary['Current Stock']
    demand_summary['Reorder Qty'] = demand_summary['Reorder Qty'].apply(lambda x: max(0, round(x)))

    # Round Avg Monthly Demand and Lead Time (Months) in output only
    demand_summary['Avg Monthly Demand'] = demand_summary['Avg Monthly Demand'].round(0).astype(int)
    demand_summary['Lead Time (Months)'] = demand_summary['Lead Time (Months)'].round(3).astype(float)

    # Final output
    return demand_summary[demand_summary['Reorder Qty'] > 0][
        ['SKU', 'Reorder Qty', 'ROP', 'Current Stock', 'Safety Stock', 'Lead Time (Months)', 'Avg Monthly Demand']
    ]

replenishment_plan = generate_replenishment_plan(synthetic_df, inventory_df)

print(replenishment_plan[[
    'Reorder Qty', 'ROP'
]])

