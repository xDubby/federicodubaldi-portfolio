from __future__ import annotations
from typing import Any, Dict, List


def build_report_md(quality: Dict[str, Any], kpis: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# Smart Data Cleaning + Reporting")
    lines.append("")
    lines.append("## Execution summary")
    lines.append(f"- Rows (raw): {quality['rows']['raw']:,}")
    lines.append(f"- Rows (clean): {quality['rows']['clean']:,}")
    lines.append(f"- Dropped: {quality['rows']['dropped']:,}")
    lines.append(f"- Duplicates removed (estimate): {quality['duplicates_removed']:,}")
    lines.append(f"- Missing cells (raw): {quality['missing_cells_raw']:,}")
    lines.append(f"- Missing cells (clean): {quality['missing_cells_clean']:,}")
    lines.append("")

    lines.append("## KPI snapshot")
    for key in ["orders", "customers", "products", "total_value", "aov", "repeat_rate"]:
        if key in kpis and kpis[key] is not None:
            lines.append(f"- **{key}**: {kpis[key]}")
    lines.append("")

    if kpis.get("top_departments"):
        lines.append("## Top departments (by items)")
        for x in kpis["top_departments"]:
            lines.append(f"- {x['department']}: {x['items']}")
        lines.append("")

    if quality.get("top_missing_columns_clean"):
        lines.append("## Data quality notes (top missing columns)")
        for x in quality["top_missing_columns_clean"]:
            lines.append(f"- {x['column']}: {x['missing']}")
        lines.append("")

    if quality.get("notes"):
        lines.append("## Rules applied / notes")
        for n in quality["notes"]:
            lines.append(f"- {n}")
        lines.append("")

    return "\n".join(lines)
