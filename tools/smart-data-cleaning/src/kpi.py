from __future__ import annotations
from typing import Any, Dict
import pandas as pd


def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    k: Dict[str, Any] = {}

    # basic counts
    k["rows"] = int(len(df))
    k["orders"] = int(df["order_id"].nunique()) if "order_id" in df.columns else None
    k["customers"] = int(df["user_id"].nunique()) if "user_id" in df.columns else None
    k["products"] = int(df["product_id"].nunique()) if "product_id" in df.columns else None

    # revenue-ish
    if "order_value" in df.columns:
        k["total_value"] = float(df["order_value"].sum())
        k["avg_item_value"] = float(df["order_value"].mean())

    if "order_id" in df.columns and "order_value" in df.columns:
        order_totals = df.groupby("order_id")["order_value"].sum()
        k["aov"] = float(order_totals.mean())  # average order value
        k["median_order_value"] = float(order_totals.median())

    # repeat rate
    if "user_id" in df.columns and "order_id" in df.columns:
        orders_per_user = df.groupby("user_id")["order_id"].nunique()
        k["repeat_rate"] = float((orders_per_user > 1).mean())

    # top departments
    if "department" in df.columns:
        top_dept = df["department"].value_counts().head(5)
        k["top_departments"] = [{"department": d, "items": int(n)} for d, n in top_dept.items()]

    return k
