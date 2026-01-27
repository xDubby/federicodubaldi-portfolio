import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
WORKING_DIR = BASE_DIR / "data" / "working"
WORKING_DIR.mkdir(parents=True, exist_ok=True)

def main(n_rows: int = 120_000, seed: int = 42):
    src = WORKING_DIR / "orders_clean_base.csv"
    out = WORKING_DIR / "orders_clean_base_sample.csv"

    # Legge tutto ma campiona (ok per una volta; poi lavoriamo sul sample)
    df = pd.read_csv(src)
    df_sample = df.sample(n=n_rows, random_state=seed).sort_values(["user_id", "order_id"])

    df_sample.to_csv(out, index=False)

    print("✔ Sample dataset generated")
    print(f"→ {out}")
    print(f"Rows: {len(df_sample):,}")

if __name__ == "__main__":
    main()
