import pandas as pd
import numpy as np
from pathlib import Path

# Step 1: Create sample data
np.random.seed(42)

total_records = 1000

# Step 2: Define sample business information
customers = [
    "Rahul", "Amit", "Priya", "Sneha", "Rohit",
    "Neha", "Vikas", "Anjali", "Karan", "Pooja"
]

products = [
    "Laptop", "Mobile", "Keyboard",
    "Mouse", "Monitor", "Printer"
]

categories = [
    "Electronics", "Accessories", "Office Equipment"
]

regions = [
    "North", "South", "East", "West"
]

# Step 3: Generate sales records
data = {
    "Order_ID": [f"ORD{i:04d}" for i in range(1, total_records + 1)],
    "Order_Date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2026-01-01", "2026-10-31"),
            total_records
        )
    ),
    "Customer_Name": np.random.choice(customers, total_records),
    "Product": np.random.choice(products, total_records),
    "Category": np.random.choice(categories, total_records),
    "Quantity": np.random.randint(1, 11, total_records),
    "Unit_Price": np.random.randint(500, 50001, total_records),
    "Region": np.random.choice(regions, total_records)
}

# Step 4: Create DataFrame
df = pd.DataFrame(data)

# Step 5: Calculate sales amount
df["Sales_Amount"] = df["Quantity"] * df["Unit_Price"]

# Step 6: Save CSV file
project_folder = Path(__file__).resolve().parent.parent

output_folder = project_folder / "data" / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "retail_sales.csv"

df.to_csv(output_file, index=False)

# Step 7: Display results
print("Retail Sales Dataset Created Successfully!")
print("-------------------------------------------")
print("Total Records:", len(df))
print("Total Columns:", len(df.columns))
print("Total Sales Amount:", df["Sales_Amount"].sum())
print("File Location:", output_file)

print("\nFirst 5 Records:")
print(df.head())