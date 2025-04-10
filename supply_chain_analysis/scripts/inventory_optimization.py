import pandas as pd

df = pd.read_csv('/Users/noahcarlos/Documents/Projects/Python/SCA_makeupstartup/supply_chain_analysis/data/processed/cleaned_data.csv')

# assume time period = 360 days
time_period = 360

# assume buffer days = 7
buffer_days = 7


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

print(df.head())