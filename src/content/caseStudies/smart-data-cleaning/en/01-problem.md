---
title: The real problem
order: 1
---

In real projects, messy data rarely “breaks” a pipeline.

Most of the time it **silently corrupts the numbers**:
the pipeline runs, the dashboard updates, and the business trusts KPIs that are wrong.

Typical symptoms:

- schema drift (renamed / missing columns)
- mixed formats for dates and numbers
- duplicates inflating totals
- inconsistent missing values (especially in critical fields)

The goal is not “clean for beauty”.
The goal is **reliable decisions**.
