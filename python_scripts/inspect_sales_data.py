import pandas as pd
from pathlib import Path

# Step 1: Locate raw sales data
project_folder = Path(__file__).resolve().parent.parent

file_path = project_folder / "data" / "raw" / "retail_sales.csv"

# Step 2: Read CSV file
df = pd.read_csv(file_path)

# Step 3: Display dataset information
print("\nDATASET OVERVIEW")
print("--------------------")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

# Step 4: Display column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# Step 5: Display first 5 records
print("\nFIRST 5 RECORDS")
print(df.head())

# Step 6: Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Step 7: Check duplicate records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# Step 8: Display data types
print("\nDATA TYPES")
print(df.dtypes)

# Step 9: Statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())