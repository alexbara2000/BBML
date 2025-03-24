import pandas as pd

file1 = pd.read_csv("results/predictions_500_base.csv")
file2 = pd.read_csv("results/processed_data_20k.csv")

# Perform an inner merge on 'domain' and 'scripts'
merged = pd.merge(file2, file1[['domain', 'scripts']], on=['domain', 'scripts'], how='inner')
merged = merged.drop_duplicates()
merged.to_csv("results/processed_data_500_base.csv", index=False)
