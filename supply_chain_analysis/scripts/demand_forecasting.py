
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing


from supply_chain_analysis.scripts.inventory_optimization import inventory_df
from supply_chain_analysis.scripts.inventory_optimization import inventory_summary

synthetic_df = pd.read_csv('/Users/noahcarlos/Documents/Projects/Python/SCA_makeupstartup/supply_chain_analysis/data/processed/synthetic_monthly.csv')

# Create a mapping from SKU to Lead Time
lead_time_map = inventory_df.set_index('SKU')['Total Lead Time'].to_dict()

# Add the column to synthetic_df
synthetic_df['Total Lead Time'] = synthetic_df['SKU'].map(lead_time_map)


# Selecting a representative set of skus
sku_summary = synthetic_df.groupby('SKU')['demand'].agg(
    avg_demand='mean',
    std_demand='std',
    total_units_sold='sum'
).reset_index()

# finding representative set of skus
steady_sku = sku_summary.sort_values("std_demand").iloc[0]["SKU"]
high_demand_sku = sku_summary.sort_values("avg_demand", ascending=False).iloc[0]["SKU"]
low_demand_sku = sku_summary.sort_values("avg_demand").iloc[1]["SKU"]
erratic_sku = sku_summary.sort_values("std_demand", ascending=False).iloc[0]["SKU"]
overstocked_sku = inventory_summary.sort_values("Overstock Amount", ascending=False).iloc[0]["SKU"]

sample_skus = list({steady_sku, high_demand_sku, low_demand_sku, erratic_sku, overstocked_sku})

sample_df = synthetic_df[synthetic_df["SKU"].isin(sample_skus)]


# Set up facet grid to plot sample SKUs
g = sns.FacetGrid(sample_df, col="SKU", col_wrap=3, height=4, sharey=False)
g.map_dataframe(sns.lineplot, x="date", y="demand")

# Add titles and formatting
g.set_titles(col_template="{col_name}")
g.set_axis_labels("Date", "Demand")
for ax in g.axes.flat:
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()


# sku0_to_forecast = synthetic_df['SKU'].iloc[0]
#
# sku0_df = synthetic_df[synthetic_df['SKU'] == sku0_to_forecast].copy()
#
# sku0_df["moving_avg"] = sku0_df["demand"].rolling(window=3).mean()
#
# plt.figure(figsize=(10, 5))
# sns.lineplot(data=sku0_df, x="date", y="demand", label="Actual Demand")
# sns.lineplot(data=sku0_df, x="date", y="moving_avg", label="3-Month Moving Avg", linestyle="--")
#
# plt.title(f"Monthly Demand Forecast for {sku0_to_forecast}")
# plt.xlabel("Date")
# plt.ylabel("Units")
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()
#
#
#
# sku0_df.set_index("date", inplace=True)
#
# model = ExponentialSmoothing(
#     sku0_df['demand'],
#     trend='add',
#     seasonal='add',
#     seasonal_periods=4
# )
#
# hw_fit = model.fit()
#
# forecast = hw_fit.forecast(6)
#
# plt.figure(figsize=(10, 5))
# sns.lineplot(data=sku0_df, x=sku0_df.index, y="demand", label="Actual Demand")
# sns.lineplot(x=forecast.index, y=forecast.values, label="Forecast", linestyle="--")
#
# plt.title("Holt-Winters Forecast with 2-Month Seasonality")
# plt.xlabel("Date")
# plt.ylabel("Demand")
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()
#
#
#
# plt.figure(figsize=(12, 6))
#
# # Actual demand
# sns.lineplot(data=sku0_df, x=sku0_df.index, y="demand", label="Actual Demand")
#
# # 3-period moving average
# sns.lineplot(data=sku0_df, x=sku0_df.index, y="moving_avg", label="3-Period Moving Avg", linestyle="--")
#
# # Holt-Winters forecast
# sns.lineplot(x=forecast.index, y=forecast.values, label="Holt-Winters Forecast", linestyle="--", color="orange")
#
# plt.title("Demand Forecast Comparison")
# plt.xlabel("Date")
# plt.ylabel("Units")
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()

