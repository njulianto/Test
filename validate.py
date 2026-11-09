#!/usr/bin/env python3
"""
Validate data/tasks.csv against schema and master lists.
Run this on every pull request / commit.
Exit code 0 = OK, 1 = errors found.
"""
import sys
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "data" / "tasks.csv"
EMPLOYEES = ROOT / "data" / "employees.csv"
TASK_MASTER = ROOT / "data" / "task_master.csv"

REQUIRED = ["date", "task", "employee_name", "hk", "total_output", "rate_per_hk"]

def main():
    errors = []

    if not TASKS.exists():
        print("ERROR: data/tasks.csv not found")
        return 1

    tasks = pd.read_csv(TASKS, dtype=str)
    employees = pd.read_csv(EMPLOYEES, dtype=str) if EMPLOYEES.exists() else pd.DataFrame()
    task_master = pd.read_csv(TASK_MASTER, dtype=str) if TASK_MASTER.exists() else pd.DataFrame()

    # 1. Required columns
    missing_cols = [c for c in REQUIRED if c not in tasks.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")

    # 2. No blank dates / tasks / names
    for col in ["date", "task", "employee_name"]:
        if col in tasks.columns:
            blanks = tasks[col].isna() | (tasks[col].str.strip() == "")
            if blanks.any():
                errors.append(f"{blanks.sum()} blank values in column '{col}'")

    # 3. Date format YYYY-MM-DD
    if "date" in tasks.columns:
        bad_dates = tasks["date"].dropna().apply(lambda x: not (len(str(x)) == 10 and str(x)[4] == "-" and str(x)[7] == "-"))
        if bad_dates.any():
            errors.append(f"{bad_dates.sum()} dates not in YYYY-MM-DD format")

    # 4. Numeric columns
    for col in ["hk", "total_output", "rate_per_hk"]:
        if col in tasks.columns:
            numeric = pd.to_numeric(tasks[col], errors="coerce")
            if numeric.isna().any():
                errors.append(f"{numeric.isna().sum()} non-numeric values in '{col}'")
            if (numeric < 0).any():
                errors.append(f"Negative values found in '{col}'")

    # 5. Employee names must exist in employees.csv
    if not employees.empty and "employee_name" in tasks.columns:
        known = set(employees["employee_name"].str.strip())
        unknown = set(tasks["employee_name"].str.strip()) - known
        if unknown:
            errors.append(f"Unknown employee names: {sorted(unknown)[:10]}{'...' if len(unknown)>10 else ''}")

    # 6. Tasks must exist in task_master.csv
    if not task_master.empty and "task" in tasks.columns and "task" in task_master.columns:
        known_tasks = set(task_master["task"].str.strip().dropna())
        unknown_tasks = set(tasks["task"].str.strip()) - known_tasks
        if unknown_tasks:
            errors.append(f"Unknown task names: {sorted(unknown_tasks)[:10]}{'...' if len(unknown_tasks)>10 else ''}")

    # 7. Exact full-row duplicates only (group work on same task is allowed)
    if tasks.duplicated().any():
        errors.append(f"{tasks.duplicated().sum()} exact duplicate rows")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        return 1

    print("VALIDATION PASSED:", len(tasks), "rows")
    return 0

if __name__ == "__main__":
    sys.exit(main())
