
import pandas as pd
from pathlib import Path

# STEP 1: Project paths
project = Path(__file__).resolve().parent.parent

input_file = project / "data" / "raw" / "retail_sales_test.csv"

output_folder = project / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

rejected_file = output_folder / "rejected_sales_records.csv"
report_file = output_folder / "data_quality_report.txt"

# STEP 2: Read raw data
df = pd.read_csv(input_file)

original_count = len(df)
reasons = [[] for _ in range(len(df))]

# STEP 3: Check duplicate orders
duplicate_mask = df.duplicated(
    subset=["Order_ID"],
    keep="first"
)

for i in range(len(df)):
    if duplicate_mask.iloc[i]:
        reasons[i].append("Duplicate Order ID")

# STEP 4: Check missing values
for column in ["Customer_Name", "Product"]:
    missing_mask = df[column].isna()

    for i in range(len(df)):
        if missing_mask.iloc[i]:
            reasons[i].append("Missing " + column)

# STEP 5: Check dates
dates = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

for i in range(len(df)):
    if pd.isna(dates.iloc[i]):
        reasons[i].append("Invalid Order Date")

# STEP 6: Check numerical values
quantity = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)

price = pd.to_numeric(
    df["Unit_Price"],
    errors="coerce"
)

for i in range(len(df)):
    if pd.isna(quantity.iloc[i]):
        reasons[i].append("Invalid Quantity")
    elif quantity.iloc[i] <= 0:
        reasons[i].append("Quantity must be positive")

    if pd.isna(price.iloc[i]):
        reasons[i].append("Invalid Unit Price")
    elif price.iloc[i] <= 0:
        reasons[i].append("Unit Price must be positive")

# STEP 7: Separate accepted and rejected records
df["Rejection_Reason"] = [
    "; ".join(reason) for reason in reasons
]

rejected = df[df["Rejection_Reason"] != ""].copy()
accepted = df[df["Rejection_Reason"] == ""].copy()

# STEP 8: Save rejected records
rejected.to_csv(rejected_file, index=False)

# STEP 9: Create quality report
report = [
    "===== DATA QUALITY REPORT =====",
    f"Original records: {original_count}",
    f"Accepted records: {len(accepted)}",
    f"Rejected records: {len(rejected)}",
    f"Duplicate records: {duplicate_mask.sum()}",
    f"Missing customer records: {df['Customer_Name'].isna().sum()}",
    f"Missing product records: {df['Product'].isna().sum()}",
    f"Invalid date records: {dates.isna().sum()}",
    f"Rejected records saved: {rejected_file}"
]

report_text = "\n".join(report)

report_file.write_text(report_text, encoding="utf-8")

print(report_text)
print("\nData quality report created successfully!")
