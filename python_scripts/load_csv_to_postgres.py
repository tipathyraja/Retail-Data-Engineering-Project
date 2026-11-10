
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from getpass import getpass

# STEP 1: Find project folder
project_folder = Path(__file__).resolve().parent.parent

# STEP 2: Locate clean CSV
csv_file = project_folder / "data" / "processed" / "clean_sales_data.csv"

# STEP 3: Ask for PostgreSQL password securely
password = getpass("Enter your PostgreSQL password: ")

# STEP 4: Create database connection
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="retail_sales_db"
)

engine = create_engine(connection_url)

try:
    # STEP 5: Read CSV
    df = pd.read_csv(csv_file)

    print("CSV records:", len(df))

    # STEP 6: Convert column names to lowercase
    df.columns = df.columns.str.lower()

    # STEP 7: Convert order date
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date

    # STEP 8: Load data into PostgreSQL
    df.to_sql(
        name="sales",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500
    )

    print("Data loaded successfully!")
    print("Records loaded:", len(df))

except Exception as e:
    print("ERROR:", e)

finally:
    engine.dispose()
