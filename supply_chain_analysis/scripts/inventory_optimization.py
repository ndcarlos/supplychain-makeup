import pandas as pd
import numpy as np

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


print(df.head())