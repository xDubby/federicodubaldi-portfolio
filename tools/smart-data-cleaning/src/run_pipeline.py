from pathlib import Path
import json

import pandas as pd

from cleaning import normalize_schema_and_types, clean_rows
from quality_checks import build_quality_report
from kpi import compute_kpis
from report import build_report_md


def main():
    repo_root = Path(__file__).resolve().parents[2]

    input_csv = (
        repo_root.parent
        / "public"
        / "projects"
        / "smart-data-cleaning"
        / "demo"
        / "input"
        / "orders_raw.csv"
    )
    out_dir = (
        repo_root.parent
        / "public"
        / "projects"
        / "smart-data-cleaning"
        / "demo"
        / "output"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== Smart Data Cleaning + Reporting ===")
    print(f"Input:  {input_csv}")
    print(f"Output: {out_dir}")
    print("--------------------------------------")

    df_raw = pd.read_csv(input_csv)

    df_norm, schema_notes = normalize_schema_and_types(df_raw)
    df_clean, cleaning_notes = clean_rows(df_norm)

    quality = build_quality_report(df_raw=df_raw, df_norm=df_norm, df_clean=df_clean, notes=(schema_notes + cleaning_notes))
    kpis = compute_kpis(df_clean)
    report_md = build_report_md(quality=quality, kpis=kpis)

    # write outputs
    cleaned_path = out_dir / "cleaned.csv"
    kpi_path = out_dir / "kpi.json"
    quality_path = out_dir / "quality.json"
    report_path = out_dir / "report.md"

    df_clean.to_csv(cleaned_path, index=False)
    kpi_path.write_text(json.dumps(kpis, indent=2, ensure_ascii=False), encoding="utf-8")
    quality_path.write_text(json.dumps(quality, indent=2, ensure_ascii=False), encoding="utf-8")
    report_path.write_text(report_md, encoding="utf-8")

    print("✔ Done")
    print(f"cleaned.csv  → {cleaned_path}")
    print(f"kpi.json     → {kpi_path}")
    print(f"quality.json → {quality_path}")
    print(f"report.md    → {report_path}")
    print("--------------------------------------")
    print("Summary")
    print(f"- Rows in:   {quality['rows']['raw']:,}")
    print(f"- Rows out:  {quality['rows']['clean']:,}")
    print(f"- Dropped:   {quality['rows']['dropped']:,}")
    print(f"- Duplicates removed: {quality['duplicates_removed']:,}")
    print(f"- Missing cells (clean): {quality['missing_cells_clean']:,}")


if __name__ == "__main__":
    main()
