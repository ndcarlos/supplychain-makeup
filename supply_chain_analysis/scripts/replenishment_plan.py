import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Select top 10 SKUs with largest reorder qty
top_replenish = replenishment_plan.sort_values(by='Reorder Qty', ascending=False).head(10)

# Create "after replenishment" stock level
top_replenish['Recommended Stock Level'] = top_replenish['ROP'] + top_replenish['Reorder Qty']

# Melt dataframe for plotting
plot_df = top_replenish.melt(
    id_vars='SKU',
    value_vars=['Current Stock', 'Recommended Stock Level'],
    var_name='Stock Type',
    value_name='Units'
)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=plot_df, x='SKU', y='Units', hue='Stock Type', palette='Blues')

plt.title('Inventory Levels: Before vs After Replenishment')
plt.xlabel('SKU')
plt.ylabel('Units in Stock')
plt.xticks(rotation=45)
plt.legend(title='')

plt.tight_layout()
plt.show()



