
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent

file_path = project / "data" / "processed" / "clean_sales_data.csv"

df = pd.read_csv(file_path)

print("===== DATA VALIDATION RESULTS =====")

print("Total records:", len(df))

print("Missing values:")
print(df.isnull().sum())

print("Duplicate Order IDs:", df["Order_ID"].duplicated().sum())

print("Invalid quantities:", (df["Quantity"] <= 0).sum())

print("Invalid prices:", (df["Unit_Price"] <= 0).sum())

print("Invalid sales amounts:",
      (df["Sales_Amount"] != df["Quantity"] * df["Unit_Price"]).sum())

print("\nValidation completed!")
