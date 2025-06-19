import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from supply_chain_analysis.scripts.replenishment_plan import synthetic_df, inventory_df

demand_summary = synthetic_df.groupby('SKU')['demand'].agg(['mean', 'std']).reset_index()

np.random.seed(42)
demand_summary['Lead Time Variability'] = np.random.uniform(0.5, 2.0, size=len(demand_summary))
demand_summary = pd.merge(demand_summary, inventory_df[['SKU', 'Total Lead Time', 'Current Stock']], on='SKU', how='left')

# Assuming 'inventory' or another DataFrame contains multiple lead times for each product
# Group by 'product_id' and calculate the standard deviation of the lead time
lead_time_variability = inventory_df.groupby('SKU')['Total Lead Time'].std().reset_index()
lead_time_variability.columns = ['SKU', 'Lead Time Variability']

# Merge the variability data back into the demand_summary DataFrame
supply_risk_df = pd.merge(demand_summary, lead_time_variability, on='SKU', how='left')
supply_risk_df = supply_risk_df.drop(columns=['Lead Time Variability_y'])
supply_risk_df = supply_risk_df.rename(columns={'Lead Time Variability_x' : 'Lead Time Variability'})

# Calculate medians for lead time variability and monthly demand
x_median = supply_risk_df['Lead Time Variability'].median()
y_median = supply_risk_df['mean'].median()

# Baseline plot: full view of SKU-level supply risk before segmentation
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=supply_risk_df,
    x='Lead Time Variability',
    y='mean',
    size='Current Stock',
    sizes=(50, 500),
    alpha=0.7,
    edgecolor='black',
    linewidth=0.5
)

# Draw horizontal and vertical lines to define risk quadrants
# (based on median lead time variability and demand)
plt.axvline(x=x_median, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=y_median, color='gray', linestyle='--', linewidth=1)

plt.title('Supply Risk Matrix: Variability vs Demand', fontsize=16)
plt.xlabel('Lead Time Variability (days)')
plt.ylabel('Average Monthly Demand (units)')
plt.grid(True)
plt.tight_layout()
plt.show()






# Calculate medians for lead time variability and monthly demand
lead_time_median = supply_risk_df['Lead Time Variability'].median()
sales_median = supply_risk_df['mean'].median()

# Filter for high-risk SKUs:
# Products with above-median lead time variability and demand
critical_df = supply_risk_df[
    (supply_risk_df['Lead Time Variability'] > lead_time_median) &
    (supply_risk_df['mean'] > sales_median)
]

# Filter for low-risk, low-demand SKUs:
# Products unlikely to stock out but may tie up excess capital
low_demand_low_risk_df = supply_risk_df[
    (supply_risk_df['Lead Time Variability'] < lead_time_median) &
    (supply_risk_df['mean'] < sales_median)
]

# Combine both segments to create a focused, actionable view
critical_and_low_risk = pd.concat([critical_df, low_demand_low_risk_df], ignore_index = True)

fig, ax = plt.subplots(figsize=(10, 6))
scatter = sns.scatterplot(
    data=critical_and_low_risk,
    x='Lead Time Variability',
    y='mean',
    hue='Current Stock',
    palette='viridis',
    s=200,
    alpha=0.8,
    edgecolor='black',
    linewidth=0.5,
    ax=ax,
    legend=False
)

# Draw horizontal and vertical lines to define risk quadrants
# (based on median lead time variability and demand)
plt.axvline(x=x_median, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=y_median, color='gray', linestyle='--', linewidth=1)

# Use color (instead of point size) to represent current stock levels
# Create a color scale based on current stock values
norm = plt.Normalize(critical_and_low_risk['Current Stock'].min(),
                     critical_and_low_risk['Current Stock'].max())
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
sm.set_array([])

# Add the colorbar to visualize the stock level gradient
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Current Stock')

# Final plot styling and axis labeling
ax.set_title('Supply Risk Matrix: Variability vs Demand', fontsize=16)
ax.set_xlabel('Lead Time Variability (days)')
ax.set_ylabel('Average Monthly Demand (units)')
plt.grid(True)
plt.tight_layout()
plt.show()

