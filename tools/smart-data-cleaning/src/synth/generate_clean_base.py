import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
KAGGLE_DIR = BASE_DIR / "data" / "kaggle_raw"
WORKING_DIR = BASE_DIR / "data" / "working"

WORKING_DIR.mkdir(parents=True, exist_ok=True)

def main():
    # --- load raw data ---
    orders = pd.read_csv(KAGGLE_DIR / "orders.csv")
    order_products = pd.read_csv(KAGGLE_DIR / "order_products__prior.csv")
    products = pd.read_csv(KAGGLE_DIR / "products.csv")
    aisles = pd.read_csv(KAGGLE_DIR / "aisles.csv")
    departments = pd.read_csv(KAGGLE_DIR / "departments.csv")

    # --- joins ---
    df = (
        order_products
        .merge(orders, on="order_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(aisles, on="aisle_id", how="left")
        .merge(departments, on="department_id", how="left")
    )

    # --- canonical fields ---
    df["quantity"] = 1  # Instacart è one-row-per-product
    np.random.seed(42)

    # simulate prices by department
    price_map = {
        "produce": (0.5, 4.0),
        "dairy eggs": (1.0, 5.0),
        "snacks": (1.0, 6.0),
        "beverages": (1.0, 8.0),
    }

    def simulate_price(dept):
        low, high = price_map.get(dept, (1.0, 6.0))
        return round(np.random.uniform(low, high), 2)

    df["unit_price"] = df["department"].apply(simulate_price)
    df["order_value"] = df["unit_price"] * df["quantity"]

    # simulate order_date (relative to order_number)
    start_date = pd.Timestamp("2023-01-01")
    df["order_date"] = start_date + pd.to_timedelta(df["order_number"], unit="D")

    # --- final selection ---
    final = df[
        [
            "order_id",
            "user_id",
            "order_number",
            "order_dow",
            "order_hour_of_day",
            "order_date",
            "product_id",
            "product_name",
            "department",
            "aisle",
            "quantity",
            "unit_price",
            "order_value",
        ]
    ].rename(columns={"order_hour_of_day": "order_hour"})

    # --- save ---
    out_path = WORKING_DIR / "orders_clean_base.csv"
    final.to_csv(out_path, index=False)

    print("✔ Clean base dataset generated")
    print(f"→ {out_path}")
    print(f"Rows: {len(final):,}")

if __name__ == "__main__":
    main()
