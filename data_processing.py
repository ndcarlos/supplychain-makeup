import pandas as pd
import numpy as np

raw_data = pd.read_csv('/Users/noahcarlos/Documents/Projects/Python/SCA_makeupstartup/supply_chain_analysis/data/raw/supply_chain_data.csv')

# remove duplicates and check for nulls
raw_data.drop_duplicates()
raw_data.isnull().sum()

# convert relevant columns to numeric or datetime
raw_data['Lead time'] = pd.to_numeric(raw_data['Lead time'], errors='coerce')
raw_data['Defect rates'] = pd.to_numeric(raw_data['Defect rates'], errors='coerce')
raw_data['Manufacturing costs'] = pd.to_numeric(raw_data['Manufacturing costs'], errors='coerce')

raw_data.to_csv('/Users/noahcarlos/Documents/Projects/Python/SCA_makeupstartup/supply_chain_analysis/data/processed/cleaned_data.csv', index=False)
