---
title: Data quality checks
order: 6
---

Quality checks are the “seatbelt” of the system.

Instead of trusting the output blindly, we compute:

- rows in / rows out
- dropped rows (and why)
- duplicate rate
- missingness on critical fields
- parsing errors (dates/numbers)

The point is to answer:

> “Can I trust these KPIs?”

If the quality is below threshold, the pipeline should **warn clearly**.
