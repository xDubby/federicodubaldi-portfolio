---
title: Noise & common issues
order: 4
---

This project focuses on issues that usually generate **silent KPI errors**:

- duplicates (same order/customer repeated)
- inconsistent identifiers (spaces, casing, formatting)
- broken dates (DD/MM vs MM/DD, strings, invalid values)
- numeric fields with commas/dots and currency symbols
- empty values represented in different ways (null, "", "N/A", "-")

A good cleaning system must **surface the problem**,
not hide it.
