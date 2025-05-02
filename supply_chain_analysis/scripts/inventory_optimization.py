import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import quantile_test

sns.set_theme(style = 'whitegrid')

df = pd.read_csv('/Users/noahcarlos/Documents/Projects/Python/SCA_makeupstartup/supply_chain_analysis/data/processed/cleaned_data.csv')

# assume monthly time period (avg 30 days)
time_period = 30

# assume buffer days = 7
buffer_days = 7

# assume order cost = $50
order_cost = 50

# assume annual holding rate = 25%
monthly_holding_rate = 0.25/12

# calculate total lead times
df['Total Lead Time'] = (
    df['Shipping times'].fillna(0) +
    df['Manufacturing lead time'].fillna(0)
)

# calculate sales velocity
df['Sales Velocity'] = df['Number of products sold'] / time_period

# calculate safety_stock
df['Safety Stock'] = df['Sales Velocity'] * buffer_days

# leading us to our reorder point
df['Reorder Point'] = df['Sales Velocity'] * df['Total Lead Time'] + df['Safety Stock']

# unit manufacturing and shipping costs
df['Unit Manufacturing Cost'] = df['Manufacturing costs']/df['Order quantities']
df['Unit Shipping Cost'] = df['Shipping costs']/df['Order quantities']

# unit cost
df['Unit Cost'] = df['Unit Manufacturing Cost'] + df['Unit Shipping Cost']

# holding cost
df['Holding Cost'] = df['Unit Cost'] * monthly_holding_rate

# economic order quantity
df['Economic Order Quantity'] = np.sqrt((2 * (df['Number of products sold']/time_period) * order_cost) / df['Holding Cost'])


inventory_df = df[[
    'SKU',
    'Availability',
    'Number of products sold',
    'Order quantities',
    'Total Lead Time',
    'Unit Manufacturing Cost',
    'Unit Shipping Cost',
    'Unit Cost',
    'Sales Velocity',
    'Safety Stock',
    'Reorder Point',
    'Holding Cost',
    'Economic Order Quantity'
]]

inventory_df = inventory_df.rename(columns = {
    'Availability': 'Current Stock',
    'Number of products sold': 'Monthly Demand',
})


# Compare current stock level demands
inventory_df['Expected Need'] = inventory_df['Monthly Demand'] + inventory_df['Safety Stock']
inventory_df['Overstock Amount'] = inventory_df['Current Stock'] - inventory_df['Expected Need']

# Generate an inventory summary
inventory_summary = inventory_df.groupby('SKU').agg({
    "Monthly Demand":"sum",
    "Order quantities":"mean",
    "Current Stock":"mean",
    "Overstock Amount":"mean"
}).reset_index()

# Find inventory turnover
inventory_summary['Inventory Turnover'] = inventory_summary['Monthly Demand']/inventory_summary['Current Stock']

# Days of inventory on hand
average_daily_demand = inventory_summary['Monthly Demand'] / 30
inventory_summary['Days On Hand'] = inventory_summary['Current Stock'] / average_daily_demand

# Adding EOQ column
eoq_df = inventory_df[['SKU', 'Economic Order Quantity']]



inventory_summary = inventory_summary.merge(eoq_df, on='SKU', how='left')
inventory_summary['Order Quantity Difference'] = inventory_df['Order quantities'] - inventory_summary['Economic Order Quantity']

# Creating overstocked/understocked classifier
inventory_summary['Stock Status'] = np.where(inventory_summary['Current Stock'] > inventory_summary['Economic Order Quantity'], 'overstocked', 'understocked')
plt_df = inventory_summary.sort_values("Overstock Amount", ascending=False).head(10)
bar_colors = ['seagreen' if x > 0 else 'tomato' for x in plt_df["Overstock Amount"]]

# Plot of over/under stocked skus
sns.barplot(data=plt_df,
            x="Overstock Amount",
            y="SKU",
            legend=False,
            dodge=False,
            palette=bar_colors
)
plt.title("Top 10 Inventory Imbalances by SKU")
plt.xlabel("Average Unit Deviation from Optimal Stock")
plt.ylabel("")
plt.axvline(0, color='gray', linestyle='--')
plt.xticks(ticks=range(-50, 60, 10))
plt.tight_layout()
plt.show()


