from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import re

import pandas as pd


CANONICAL_COLS = {
    "order_id": ["order_id", "Order ID", "orderId", "ORDER_ID"],
    "user_id": ["user_id", "CustomerID", "customer_id", "USER_ID"],
    "order_number": ["order_number", "orderNumber"],
    "order_dow": ["order_dow", "orderDayOfWeek"],
    "order_hour": ["order_hour", "order_hour_of_day", "OrderHour", "hour"],
    "order_date": ["order_date", "OrderDate", "date"],
    "product_id": ["product_id", "ProductID"],
    "product_name": ["product_name", "ProductName", "product"],
    "department": ["department", "Department"],
    "aisle": ["aisle", "Aisle"],
    "quantity": ["quantity", "qty", "Quantity"],
    "unit_price": ["unit_price", "Unit Price", "price"],
    "order_value": ["order_value", "Order Value", "value"],
}


def _rename_to_canonical(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    notes = []
    col_map = {}
    lower_map = {c.lower(): c for c in df.columns}

    for canon, variants in CANONICAL_COLS.items():
        found = None
        for v in variants:
            key = v.lower()
            if key in lower_map:
                found = lower_map[key]
                break
        if found and found != canon:
            col_map[found] = canon
            notes.append(f"Renamed column '{found}' -> '{canon}'")

    if col_map:
        df = df.rename(columns=col_map)

    return df, notes


def _to_float_series(s: pd.Series) -> pd.Series:
    # accept "1,47" and "  2.50 "
    def parse(x):
        if pd.isna(x):
            return pd.NA
        txt = str(x).strip()
        txt = txt.replace("€", "").replace("$", "").strip()
        txt = txt.replace(",", ".")
        try:
            return float(txt)
        except Exception:
            return pd.NA

    return s.apply(parse).astype("Float64")


def _to_int_series(s: pd.Series) -> pd.Series:
    def parse(x):
        if pd.isna(x):
            return pd.NA
        txt = str(x).strip()
        # keep only digits (e.g. "08")
        m = re.match(r"^\d+$", txt)
        if not m:
            return pd.NA
        try:
            return int(txt)
        except Exception:
            return pd.NA

    return s.apply(parse).astype("Int64")


def _to_date_series(s: pd.Series) -> pd.Series:
    # Parse ISO dates (YYYY-MM-DD) and EU dates (DD/MM/YYYY) without warnings
    s_str = s.astype("string")

    iso_mask = s_str.str.match(r"^\d{4}-\d{2}-\d{2}", na=False)
    eu_mask = s_str.str.match(r"^\d{2}/\d{2}/\d{4}", na=False)

    out = pd.Series(pd.NaT, index=s.index)

    # ISO first (no dayfirst)
    if iso_mask.any():
        out.loc[iso_mask] = pd.to_datetime(
            s_str.loc[iso_mask],
            errors="coerce",
            format="%Y-%m-%d",
        )

    # EU format only where it matches (dayfirst implied by format)
    if eu_mask.any():
        out.loc[eu_mask] = pd.to_datetime(
            s_str.loc[eu_mask],
            errors="coerce",
            format="%d/%m/%Y",
        )

    # fallback (anything else)
    other_mask = ~(iso_mask | eu_mask)
    if other_mask.any():
        out.loc[other_mask] = pd.to_datetime(
            s_str.loc[other_mask],
            errors="coerce",
            dayfirst=True,
        )

    return out.dt.date



def normalize_schema_and_types(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    df = df_raw.copy()
    notes = []

    # trim column names
    df.columns = [c.strip() for c in df.columns]

    df, rn = _rename_to_canonical(df)
    notes.extend(rn)

    # strip whitespace on common string cols
    for c in ["product_name", "department", "aisle"]:
        if c in df.columns:
            df[c] = df[c].astype("string").str.strip()

    # coerce types
    if "unit_price" in df.columns:
        df["unit_price"] = _to_float_series(df["unit_price"])
    if "order_value" in df.columns:
        df["order_value"] = _to_float_series(df["order_value"])
    if "quantity" in df.columns:
        df["quantity"] = _to_int_series(df["quantity"])
    if "order_hour" in df.columns:
        df["order_hour"] = _to_int_series(df["order_hour"])
    if "order_date" in df.columns:
        df["order_date"] = _to_date_series(df["order_date"])

    # recompute order_value if missing or invalid
    if "unit_price" in df.columns and "quantity" in df.columns:
        if "order_value" not in df.columns:
            df["order_value"] = (df["unit_price"] * df["quantity"]).astype("Float64")
            notes.append("Created 'order_value' as unit_price * quantity")
        else:
            mask_bad = df["order_value"].isna()
            df.loc[mask_bad, "order_value"] = (df["unit_price"] * df["quantity"]).astype("Float64")
            if mask_bad.any():
                notes.append(f"Recomputed 'order_value' for {int(mask_bad.sum())} rows")

    return df, notes


def clean_rows(df_norm: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    df = df_norm.copy()
    notes = []

    before = len(df)

    # drop duplicates (same order_id + product_id)
    if "order_id" in df.columns and "product_id" in df.columns:
        dups = df.duplicated(subset=["order_id", "product_id"], keep="first")
        n_dups = int(dups.sum())
        if n_dups:
            df = df.loc[~dups].copy()
            notes.append(f"Removed duplicates on (order_id, product_id): {n_dups}")

    # drop rows missing critical fields
    critical = [c for c in ["order_id", "user_id", "product_id", "order_date"] if c in df.columns]
    if critical:
        mask = df[critical].isna().any(axis=1)
        n_drop = int(mask.sum())
        if n_drop:
            df = df.loc[~mask].copy()
            notes.append(f"Dropped rows missing critical fields {critical}: {n_drop}")

    # basic sanity filters
    if "quantity" in df.columns:
        mask = df["quantity"].isna() | (df["quantity"] <= 0)
        n_drop = int(mask.sum())
        if n_drop:
            df = df.loc[~mask].copy()
            notes.append(f"Dropped rows with invalid quantity: {n_drop}")

    if "unit_price" in df.columns:
        # keep price > 0 and cap crazy outliers (we also report them later)
        mask = df["unit_price"].isna() | (df["unit_price"] <= 0)
        n_drop = int(mask.sum())
        if n_drop:
            df = df.loc[~mask].copy()
            notes.append(f"Dropped rows with invalid unit_price: {n_drop}")

    after = len(df)
    notes.append(f"Rows: {before} -> {after} (delta {after-before})")

    return df, notes
