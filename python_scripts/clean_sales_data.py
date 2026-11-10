
import pandas as pd
from pathlib import Path

# STEP 1: Locate project folders
project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "raw" / "retail_sales_test.csv"

output_folder = project_folder / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "clean_sales_data.csv"

# STEP 2: EXTRACT - Read raw data
df = pd.read_csv(input_file)

print("===== ETL PIPELINE STARTED =====")
print("Original Records:", len(df))

# STEP 3: Remove duplicate orders
before = len(df)

df = df.drop_duplicates(subset=["Order_ID"], keep="first")

duplicates_removed = before - len(df)

print("\nDuplicates Removed:", duplicates_removed)

# STEP 4: Handle missing values
before = len(df)

df = df.dropna(subset=["Customer_Name", "Product"])

missing_removed = before - len(df)

print("Missing Records Removed:", missing_removed)

# STEP 5: Validate order dates
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

before = len(df)

df = df.dropna(subset=["Order_Date"])

invalid_dates_removed = before - len(df)

print("Invalid Dates Removed:", invalid_dates_removed)

# STEP 6: Validate numerical columns
df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)

df["Unit_Price"] = pd.to_numeric(
    df["Unit_Price"],
    errors="coerce"
)

before = len(df)

df = df.dropna(subset=["Quantity", "Unit_Price"])

df = df[
    (df["Quantity"] > 0) &
    (df["Unit_Price"] > 0)
]

invalid_numbers_removed = before - len(df)

print("Invalid Numerical Records Removed:", invalid_numbers_removed)

# STEP 7: Recalculate sales amount
df["Sales_Amount"] = df["Quantity"] * df["Unit_Price"]

# STEP 8: Sort data by order date
df = df.sort_values(by="Order_Date")

# STEP 9: LOAD - Save clean data
df.to_csv(output_file, index=False)

# STEP 10: Final report
print("\n===== ETL PIPELINE COMPLETED =====")

print("Final Clean Records:", len(df))
print("Total Records Removed:",
      duplicates_removed +
      missing_removed +
      invalid_dates_removed +
      invalid_numbers_removed)

print("Total Sales:", df["Sales_Amount"].sum())

print("Clean File Saved At:", output_file)

print("\nData Cleaning Successful!")
