# Data Schema

All files use UTF-8 CSV. Dates are always `YYYY-MM-DD`. Numbers use `.` as decimal separator. Empty values are blank (not "null").

## data/tasks.csv (main historical data — never rewrite past rows)

| Column | Type | Required | Description | Validation |
|--------|------|----------|-------------|------------|
| date | date | Yes | Work date | YYYY-MM-DD, not blank |
| task | text | Yes | Task name | Must exist in task_master.csv |
| employee_name | text | Yes | Employee full name | Must exist in employees.csv |
| position | text | No | Job title at the time | Free text |
| hk | number | Yes | Jumlah Hari Kerja (work-days) | ≥ 0, usually 1 or 0.5 |
| overtime | number | No | Overtime hours/days | ≥ 0 |
| output | number | No | Raw prestasi | ≥ 0 |
| output_premium | number | No | Premium prestasi | ≥ 0 |
| total_output | number | Yes | Final output quantity | ≥ 0 |
| unit | text | No | Unit of output (BUAH, HA, MTR, etc.) | Free text |
| estate | text | No | Estate / location name | Free text |
| block | text | No | Block number | Free text |
| notes | text | No | Details / notes | Free text |
| rate_per_hk | number | Yes | Salary rate (Rp) per HK **at the time of this row** | ≥ 0. Historical snapshot — do not update old rows |
| premium_rate | number | No | Premium rate | ≥ 0 |
| hk_amount | number | No | Calculated HK cost | ≥ 0 |
| premium_amount | number | No | Calculated premium cost | ≥ 0 |
| overtime_amount | number | No | Calculated overtime cost | ≥ 0 |
| group | text | No | Task group / category | Free text |

**Important salary rule**: `rate_per_hk` is frozen when the row is created. Changing an employee’s current salary in `employees.csv` does **not** change past rows.

## data/employees.csv (master list — can be edited)

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| employee_name | text | Yes | Full name (must match exactly in tasks) |
| employee_id | text/number | No | Internal ID |
| position | text | No | Current job title |
| current_rate_per_hk | number | Yes | **Current** salary rate (Rp per HK). Used for new entries only |
| nik | text | No | National ID |

To change salary: edit `current_rate_per_hk`. New task rows will use the new rate. Old task rows keep their original `rate_per_hk`.

## data/task_master.csv (allowed tasks)

| Column | Type | Description |
|--------|------|-------------|
| task_id | text | Internal code |
| category_1 | text | High-level category |
| category_2 | text | Sub-category |
| task | text | Exact task name (must match tasks.csv) |
| unit | text | Default unit |

## Rate definition used in reports

- **Output rate** = total_output / hk (output per work-day)
- **Cost rate** = rate_per_hk (Rp per work-day, already stored per row)
- Daily / weekly totals are simple sums of total_output and hk

No separate target column is required for the first version. Add one later if needed.
