import random
from pathlib import Path

import numpy as np
import pandas as pd

from profiles import PROFILES

BASE_DIR = Path(__file__).resolve().parents[2]
WORKING_DIR = BASE_DIR / "data" / "working"
PUBLIC_INPUT_DIR = (
    BASE_DIR.parents[1]
    / "public"
    / "projects"
    / "smart-data-cleaning"
    / "demo"
    / "input"
)
PUBLIC_INPUT_DIR.mkdir(parents=True, exist_ok=True)


def _pick_idx(n: int, rate: float, rng: np.random.Generator):
    k = max(0, int(n * rate))
    if k == 0:
        return np.array([], dtype=int)
    return rng.choice(np.arange(n), size=k, replace=False)


def _inject_missing(df: pd.DataFrame, idx: np.ndarray, rng: np.random.Generator):
    if len(idx) == 0:
        return df

    cols = [
        "order_hour",
        "department",
        "aisle",
        "product_name",
        "unit_price",
        "order_date",
    ]
    cols = [c for c in cols if c in df.columns]

    for i in idx:
        c = rng.choice(cols)
        df.at[i, c] = np.nan

    return df


def _inject_dirty(df: pd.DataFrame, idx: np.ndarray, rng: np.random.Generator):
    if len(idx) == 0:
        return df

    for i in idx:
        choice = rng.integers(0, 5)

        # 0) unit_price as string with comma
        if (
            choice == 0
            and "unit_price" in df.columns
            and pd.notna(df.at[i, "unit_price"])
        ):
            df["unit_price"] = df["unit_price"].astype("object")
            v = df.at[i, "unit_price"]
            df.at[i, "unit_price"] = str(v).replace(".", ",")

        # 1) order_date wrong format
        elif (
            choice == 1
            and "order_date" in df.columns
            and pd.notna(df.at[i, "order_date"])
        ):
            d = str(df.at[i, "order_date"])
            if "-" in d[:10]:
                yyyy, mm, dd = d[:10].split("-")
                df.at[i, "order_date"] = f"{dd}/{mm}/{yyyy}"

        # 2) order_hour as string "08"
        elif (
            choice == 2
            and "order_hour" in df.columns
            and pd.notna(df.at[i, "order_hour"])
        ):
            df["order_hour"] = df["order_hour"].astype("object")
            h = int(df.at[i, "order_hour"])
            df.at[i, "order_hour"] = f"{h:02d}"

        # 3) quantity as string
        elif (
            choice == 3
            and "quantity" in df.columns
            and pd.notna(df.at[i, "quantity"])
        ):
            df["quantity"] = df["quantity"].astype("object")
            q = int(df.at[i, "quantity"])
            df.at[i, "quantity"] = str(q)

        # 4) stray whitespace
        elif choice == 4:
            for c in ["department", "product_name"]:
                if c in df.columns and pd.notna(df.at[i, c]):
                    df.at[i, c] = f"  {str(df.at[i, c]).strip()}  "

    return df


def _inject_outliers(df: pd.DataFrame, idx: np.ndarray, rng: np.random.Generator):
    if len(idx) == 0 or "unit_price" not in df.columns:
        return df

    for i in idx:
        if pd.isna(df.at[i, "unit_price"]):
            continue
        try:
            v = float(str(df.at[i, "unit_price"]).replace(",", "."))
            df.at[i, "unit_price"] = round(v * rng.uniform(6, 12), 2)
        except Exception:
            pass

    return df


def _duplicate_rows(df: pd.DataFrame, rate: float):
    n = len(df)
    k = max(0, int(n * rate))
    if k == 0:
        return df

    sample = df.sample(n=k, random_state=42)
    if "product_name" in sample.columns:
        sample["product_name"] = sample["product_name"].astype(str) + " "

    return pd.concat([df, sample], ignore_index=True)


def _schema_drift(df: pd.DataFrame):
    mapping = {
        "order_id": "Order ID",
        "user_id": "CustomerID",
        "order_date": "OrderDate",
        "unit_price": "Unit Price",
        "order_value": "Order Value",
    }
    cols = {k: v for k, v in mapping.items() if k in df.columns}
    return df.rename(columns=cols)


def generate_orders_raw(profile_name: str = "medium", seed: int = 42):
    if profile_name not in PROFILES:
        raise ValueError(
            f"Unknown profile: {profile_name}. Use one of {list(PROFILES.keys())}"
        )

    profile = PROFILES[profile_name]
    rng = np.random.default_rng(seed)
    random.seed(seed)

    src = WORKING_DIR / "orders_clean_base_sample.csv"
    df = pd.read_csv(src)

    # duplicates
    df = _duplicate_rows(df, profile.dup_rate)

    n = len(df)
    idx_missing = _pick_idx(n, profile.missing_rate, rng)
    idx_dirty = _pick_idx(n, profile.dirty_rate, rng)
    idx_outlier = _pick_idx(n, profile.outlier_rate, rng)

    df = _inject_missing(df, idx_missing, rng)
    df = _inject_dirty(df, idx_dirty, rng)
    df = _inject_outliers(df, idx_outlier, rng)

    if profile.rename_schema:
        df = _schema_drift(df)

    out = PUBLIC_INPUT_DIR / "orders_raw.csv"
    df.to_csv(out, index=False)

    print("✔ orders_raw.csv generated")
    print(f"Profile: {profile_name}")
    print(f"→ {out}")
    print(f"Rows: {len(df):,}")
    print(f"Missing injected: {len(idx_missing):,}")
    print(f"Dirty injected: {len(idx_dirty):,}")
    print(f"Outliers injected: {len(idx_outlier):,}")


if __name__ == "__main__":
    generate_orders_raw(profile_name="medium", seed=42)
