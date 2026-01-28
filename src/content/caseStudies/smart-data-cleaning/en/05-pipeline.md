---
title: Pipeline
order: 5
---

The pipeline is structured in clear steps:

1. **Ingest**
   - load file(s)
   - basic sanity checks

2. **Normalize**
   - column names normalization
   - type parsing (dates, numbers)
   - standardize missing values

3. **Deduplicate**
   - define dedupe keys
   - keep rules explicit and traceable

4. **Validate**
   - schema checks
   - range checks (where meaningful)
   - critical-field completeness

5. **Export**
   - cleaned dataset
   - KPIs
   - quality report
   - narrative report

Each step writes logs and produces measurable signals.
