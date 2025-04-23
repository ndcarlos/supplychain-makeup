
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing


from supply_chain_analysis.scripts.inventory_optimization import inventory_df
from supply_chain_analysis.scripts.inventory_optimization import inventory_summary

synthetic_demand = pd.read_csv('supply_chain_analysis/data/processed/synthetic_monthly.csv')

head(synthetic_demand)








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