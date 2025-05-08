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

print(supply_risk_df.columns)

# Plot Supply Risk Matrix
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=supply_risk_df,  # full dataset here
    x='Lead Time Variability',
    y='mean',
    size='Current Stock',
    color='blue',  # single color since we're not using hue anymore
    sizes=(50, 500),
    alpha=0.7,
    edgecolor='black',
    linewidth=0.5
)

plt.title('Supply Risk Matrix: Variability vs Demand', fontsize=16)
plt.xlabel('Lead Time Variability (days)')
plt.ylabel('Average Monthly Demand (units)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculate medians
x_median = supply_risk_df['Lead Time Variability'].median()
y_median = supply_risk_df['mean'].median()

plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=supply_risk_df,
    x='Lead Time Variability',
    y='mean',
    size='Current Stock',
    color='tomato',
    sizes=(50, 500),
    alpha=0.7,
    edgecolor='black',
    linewidth=0.5
)

# Add quadrant lines
plt.axvline(x=x_median, color='gray', linestyle='--', linewidth=1)
plt.axhline(y=y_median, color='gray', linestyle='--', linewidth=1)

plt.title('Supply Risk Matrix: Variability vs Demand', fontsize=16)
plt.xlabel('Lead Time Variability (days)')
plt.ylabel('Average Monthly Demand (units)')
plt.grid(True)
plt.tight_layout()
plt.show()



# Calculate thresholds
variability_threshold = supply_risk_df['Lead Time Variability'].quantile(0.7)  # top 30%
stock_threshold = supply_risk_df['Current Stock'].quantile(0.3)  # bottom 30%

# Filter the DataFrame
critical_df = supply_risk_df[
    (supply_risk_df['Lead Time Variability'] >= variability_threshold) &
    (supply_risk_df['Current Stock'] <= stock_threshold)
]

# Print number of critical SKUs
print(f"Number of critical SKUs: {len(critical_df)}")


plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=critical_df,  # or supply_risk_df for full view
    x='Lead Time Variability',
    y='mean',
    size='Current Stock',
    color='blue',  # single color now that hue is removed
    sizes=(50, 500),
    alpha=0.7,
    edgecolor='black',
    linewidth=0.5
)

plt.title('Supply Risk Matrix: Variability vs Demand', fontsize=16)
plt.xlabel('Lead Time Variability (days)')
plt.ylabel('Average Monthly Demand (units)')
plt.grid(True)
plt.tight_layout()
plt.show()

