---
title: Controlled input
order: 3
---

The starting point is a real-world export (e-commerce / CRM style).

Before doing any cleaning, we define a **controlled input contract**:

- expected columns (even if some may be missing)
- data types and parsing rules
- minimal fields required for KPIs
- how to treat nulls and placeholders

This makes the pipeline *idiot-proof*:
when the input changes, we detect it and react consistently.
