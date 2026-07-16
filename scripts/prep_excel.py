from pathlib import Path

import pandas as pd

print("=" * 60)
print("PREPARING DATA FOR EXCEL")
print("=" * 60)

# =====================================================
# Paths
# =====================================================

INPUT_FILE = Path("data/processed/supply_chain_clean.csv")
OUTPUT_FILE = Path("excel/supply_chain_excel.xlsx")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv(INPUT_FILE)

# =====================================================
# Save for Excel
# =====================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Data",
        index=False
    )

print("\nDataset Summary")
print("-" * 40)

print(f"Rows      : {len(df):,}")
print(f"Columns   : {len(df.columns)}")

print("\nOutput File")
print("-" * 40)

print(OUTPUT_FILE)

print("\nExcel Dataset Created Successfully.")