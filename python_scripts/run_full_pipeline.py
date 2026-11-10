
import os
import pandas as pd
import logging
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# PROJECT PATHS
project = Path(__file__).resolve().parent.parent

raw_file = project / "data" / "raw" / "retail_sales_test.csv"
clean_file = project / "data" / "processed" / "clean_sales_data.csv"
log_folder = project / "logs"

log_folder.mkdir(exist_ok=True)
clean_file.parent.mkdir(exist_ok=True)

# LOGGING SETUP
logging.basicConfig(
    filename=log_folder / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

engine = None

try:
    print("===== AUTOMATED ETL STARTED =====")
    logging.info("ETL pipeline started")

    # EXTRACT
    df = pd.read_csv(raw_file)
    original_count = len(df)

    print("Original records:", original_count)
    logging.info("Extracted %s records", original_count)

    # TRANSFORM
    df = df.drop_duplicates(
        subset=["Order_ID"],
        keep="first"
    )

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["Unit_Price"] = pd.to_numeric(
        df["Unit_Price"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "Customer_Name",
            "Product",
            "Order_Date",
            "Quantity",
            "Unit_Price"
        ]
    )

    df = df[
        (df["Quantity"] > 0) &
        (df["Unit_Price"] > 0)
    ].copy()

    df["Sales_Amount"] = (
        df["Quantity"] * df["Unit_Price"]
    )

    df = df.sort_values("Order_Date")

    duplicates_removed = original_count - len(
        pd.read_csv(raw_file)
    )
    # Final count and quality summary
    final_count = len(df)
    removed_count = original_count - final_count

    # LOAD CLEAN CSV
    df.to_csv(clean_file, index=False)

    print("Final clean records:", final_count)
    print("Records removed:", removed_count)
    logging.info("Cleaned records: %s", final_count)

 
    # DATABASE CONNECTION
    import os

    os.environ["PGPASSFILE"] = str(
        Path.home() / "AppData" / "Roaming" /
        "postgresql" / "pgpass.conf"
    )

    url = URL.create(
        "postgresql+psycopg2",
        username="postgres",
        host="localhost",
        port=5432,
        database="retail_sales_db"
    )

    engine = create_engine(url)


    # LOAD INTO POSTGRESQL
    df.columns = df.columns.str.lower()
    df["order_date"] = pd.to_datetime(
        df["order_date"]
    ).dt.date

    with engine.begin() as connection:
        connection.execute(text("DELETE FROM sales"))

        df.to_sql(
            "sales",
            con=connection,
            if_exists="append",
            index=False,
            chunksize=500
        )

        database_count = connection.execute(
            text("SELECT COUNT(*) FROM sales")
        ).scalar()

        if database_count != final_count:
            raise ValueError("Database record count mismatch")
        
    print("Database records:", database_count)
    print("ETL pipeline completed successfully!")

    logging.info(
        "Pipeline completed. Final records: %s",
        database_count
    )
    
    from datetime import datetime

    output_folder = project / "output"
    output_folder.mkdir(parents=True, exist_ok=True)

    summary_file = output_folder / "pipeline_summary.txt"

    rejected_count = original_count - final_count

    summary = f"""
    ===== ETL PIPELINE SUMMARY =====
    Execution Date: {datetime.now()}
    Original Records: {original_count}
    Accepted Records: {final_count}
    Rejected Records: {rejected_count}
    PostgreSQL Records: {database_count}
    Missing Values: {df.isnull().sum().sum()}
    Duplicate Order IDs: {df['order_id'].duplicated().sum()}
    Pipeline Status: SUCCESS
    """

    summary_file.write_text(summary, encoding="utf-8")

    print("Pipeline summary saved:", summary_file)


except Exception:
    logging.exception("ETL pipeline failed")
    print("ETL pipeline failed. Check logs/pipeline.log")

finally:
    if engine:
        engine.dispose()
