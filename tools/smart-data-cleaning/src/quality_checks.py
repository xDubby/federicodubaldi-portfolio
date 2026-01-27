from __future__ import annotations
from typing import Any, Dict, List, Tuple
import pandas as pd


def build_quality_report(
    df_raw: pd.DataFrame,
    df_norm: pd.DataFrame,
    df_clean: pd.DataFrame,
    notes: List[str],
) -> Dict[str, Any]:
    report: Dict[str, Any] = {}

    report["rows"] = {
        "raw": int(len(df_raw)),
        "normalized": int(len(df_norm)),
        "clean": int(len(df_clean)),
        "dropped": int(len(df_raw) - len(df_clean)),
    }

    # duplicates removed estimate (raw duplicates on keys)
    dup_removed = 0
    if "Order ID" in df_raw.columns and "product_id" in df_raw.columns:
        dup_removed = int(df_raw.duplicated(subset=["Order ID", "product_id"], keep="first").sum())
    elif "order_id" in df_raw.columns and "product_id" in df_raw.columns:
        dup_removed = int(df_raw.duplicated(subset=["order_id", "product_id"], keep="first").sum())
    report["duplicates_removed"] = dup_removed

    report["missing_cells_raw"] = int(df_raw.isna().sum().sum())
    report["missing_cells_clean"] = int(df_clean.isna().sum().sum())

    # missing by column (top)
    miss = df_clean.isna().sum().sort_values(ascending=False).head(10)
    report["top_missing_columns_clean"] = [
        {"column": str(k), "missing": int(v)} for k, v in miss.items() if int(v) > 0
    ]

    report["notes"] = notes

    return report
