import pandas as pd

df = pd.read_csv("data/raw_sales_data.csv")

print("First rows of dataset:")
print(df.head())

print("\nColumn data types:")
print(df.dtypes)

