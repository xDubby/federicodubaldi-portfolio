---
title: Outputs & proof
order: 7
---

The pipeline produces a small set of **portable outputs**:

- `cleaned.csv` (or parquet)
- `kpi.json`
- `quality.json`
- `report.md` (human-readable narrative)

This separation is intentional:

- you can plug KPIs into a dashboard
- you can audit the quality independently
- you can share the report with non-technical stakeholders

The result is not just “data cleaned”:
it’s **proof that it’s safe to use**.
