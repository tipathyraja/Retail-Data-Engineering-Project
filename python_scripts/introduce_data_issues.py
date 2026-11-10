
import pandas as pd
from pathlib import Path

# Step 1: Locate project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: Read original sales data
input_file = project_folder / "data" / "raw" / "retail_sales.csv"

df = pd.read_csv(input_file)

print("Original Records:", len(df))

# Step 3: Introduce missing values
df.loc[0, "Customer_Name"] = None
df.loc[1, "Product"] = None

# Step 4: Introduce invalid quantity
df.loc[2, "Quantity"] = -5

# Step 5: Introduce incorrect sales amount
df.loc[3, "Sales_Amount"] = 999

# Step 6: Introduce invalid date
df.loc[4, "Order_Date"] = "not_a_date"

# Step 7: Add a duplicate record
df = pd.concat([df, df.iloc[[5]]], ignore_index=True)

# Step 8: Save test dataset
output_file = project_folder / "data" / "raw" / "retail_sales_test.csv"

df.to_csv(output_file, index=False)

print("\nData quality issues introduced successfully!")
print("Total Records:", len(df))
print("Test File:", output_file)
