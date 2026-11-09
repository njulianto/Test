#!/usr/bin/env python3
"""
Generate a simple static HTML dashboard from data/tasks.csv
Output: reports/index.html
"""
import pandas as pd
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "data" / "tasks.csv"
OUT = ROOT / "reports" / "index.html"

def main():
    df = pd.read_csv(TASKS)
    df["date"] = pd.to_datetime(df["date"])
    df["total_output"] = pd.to_numeric(df["total_output"], errors="coerce").fillna(0)
    df["hk"] = pd.to_numeric(df["hk"], errors="coerce").fillna(0)
    df["rate_per_hk"] = pd.to_numeric(df["rate_per_hk"], errors="coerce").fillna(0)

    today = date.today().isoformat()
    # Use latest date in data if today is after data
    latest = df["date"].max().strftime("%Y-%m-%d")
    default_date = latest

    # Today summary
    today_df = df[df["date"] == default_date]
    today_rows = today_df[["date", "employee_name", "task", "total_output", "unit", "hk", "rate_per_hk"]].to_dict("records")

    # Per task
    per_task = df.groupby("task").agg(
        total_output=("total_output", "sum"),
        entries=("task", "count"),
        total_hk=("hk", "sum"),
        avg_output=("total_output", "mean")
    ).reset_index().sort_values("total_output", ascending=False)

    # Per employee
    per_emp = df.groupby("employee_name").agg(
        total_output=("total_output", "sum"),
        total_hk=("hk", "sum"),
        days=("date", "nunique"),
        avg_rate=("rate_per_hk", "mean")
    ).reset_index()
    per_emp["output_per_hk"] = (per_emp["total_output"] / per_emp["total_hk"].replace(0, 1)).round(2)
    per_emp = per_emp.sort_values("total_output", ascending=False)

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Laporan Kegiatan Harian</title>
<style>
body {{ font-family: system-ui, Arial, sans-serif; margin: 20px; background: #f7f7f7; }}
h1 {{ color: #1a5f2a; }}
table {{ border-collapse: collapse; width: 100%; background: white; margin: 10px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #1a5f2a; color: white; }}
tr:nth-child(even) {{ background: #f2f2f2; }}
.card {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
input, select {{ padding: 6px; margin: 5px; }}
</style>
</head>
<body>
<h1>Laporan Kegiatan Harian</h1>
<p>Data terakhir: {latest} &nbsp;|&nbsp; Total baris: {len(df):,}</p>

<div class="card">
<h2>Filter (sederhana)</h2>
<label>Tanggal: <input type="date" id="dateFilter" value="{default_date}"></label>
<button onclick="filterToday()">Tampilkan Hari Ini</button>
</div>

<div class="card">
<h2>Kegiatan Hari Terpilih</h2>
<div id="todayTable"></div>
</div>

<div class="card">
<h2>Ringkasan per Task (semua data)</h2>
{per_task.head(30).to_html(index=False, classes="summary")}
</div>

<div class="card">
<h2>Ringkasan per Karyawan</h2>
{per_emp.head(30).to_html(index=False, classes="summary")}
</div>

<script>
const allData = {df[["date","employee_name","task","total_output","unit","hk","rate_per_hk"]].to_json(orient="records", date_format="iso")};

function filterToday() {{
  const d = document.getElementById("dateFilter").value;
  const rows = allData.filter(r => r.date.startsWith(d));
  let html = "<table><tr><th>Nama</th><th>Task</th><th>Output</th><th>Unit</th><th>HK</th><th>Rp/HK</th></tr>";
  rows.forEach(r => {{
    html += `<tr><td>${{r.employee_name}}</td><td>${{r.task}}</td><td>${{r.total_output}}</td><td>${{r.unit||""}}</td><td>${{r.hk}}</td><td>${{r.rate_per_hk}}</td></tr>`;
  }});
  html += "</table>";
  document.getElementById("todayTable").innerHTML = rows.length ? html : "<p>Tidak ada data pada tanggal ini.</p>";
}}
filterToday();
</script>
</body>
</html>"""

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Report written to {OUT}")

if __name__ == "__main__":
    main()
