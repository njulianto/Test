#!/usr/bin/env python3
"""
Export full dataset to CSV, XLSX (with summary sheets), and JSON.
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "data" / "tasks.csv"
EXPORT = ROOT / "exports"

def main():
    EXPORT.mkdir(exist_ok=True)
    df = pd.read_csv(TASKS)

    # CSV
    df.to_csv(EXPORT / "tasks_full.csv", index=False)

    # JSON
    df.to_json(EXPORT / "tasks_full.json", orient="records", indent=2, force_ascii=False)

    # XLSX with summary
    with pd.ExcelWriter(EXPORT / "tasks_full.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw Data", index=False)

        # Per task
        per_task = df.groupby("task").agg(
            total_output=("total_output", "sum"),
            entries=("task", "count"),
            total_hk=("hk", "sum")
        ).reset_index()
        per_task.to_excel(writer, sheet_name="Per Task", index=False)

        # Per employee
        per_emp = df.groupby("employee_name").agg(
            total_output=("total_output", "sum"),
            total_hk=("hk", "sum"),
            avg_rate=("rate_per_hk", "mean")
        ).reset_index()
        per_emp.to_excel(writer, sheet_name="Per Employee", index=False)

    print("Exports written to exports/")

if __name__ == "__main__":
    main()
