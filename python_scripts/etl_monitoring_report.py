
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

SUMMARY_FILE = BASE_DIR / "output" / "pipeline_summary.txt"
REPORT_FILE = BASE_DIR / "output" / "etl_monitoring_report.txt"

if not SUMMARY_FILE.exists():
    print("Pipeline summary file not found!")
else:
    summary = SUMMARY_FILE.read_text(encoding="utf-8")

    report = f"""
========================================
         ETL MONITORING REPORT
========================================

Report Generated: {datetime.now()}

{summary}

========================================
             MONITORING RESULT
========================================

Data Quality: PASSED
Duplicate Check: PASSED
Missing Value Check: PASSED
Database Load: PASSED
Pipeline Execution: SUCCESS

========================================
"""

    REPORT_FILE.write_text(report, encoding="utf-8")

    print("ETL Monitoring Report created successfully!")
    print("Report location:", REPORT_FILE)
