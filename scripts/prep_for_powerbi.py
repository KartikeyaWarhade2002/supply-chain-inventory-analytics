from pathlib import Path

import pandas as pd

print("=" * 60)
print("PREPARING DATA FOR POWER BI")
print("=" * 60)

# =====================================================
# Paths
# =====================================================

INPUT_FILE = Path("data/processed/supply_chain_clean.csv")
OUTPUT_FILE = Path("data/processed/supply_chain_powerbi.csv")

# =====================================================
# Load Clean Dataset
# =====================================================

df = pd.read_csv(INPUT_FILE)

# =====================================================
# Prepare Dataset for Power BI
# =====================================================

# No additional transformations are required.
# The dataset has already been cleaned and feature engineered
# in prepare_data.py.

powerbi_df = df.copy()

# =====================================================
# Save CSV
# =====================================================

powerbi_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# =====================================================
# Summary
# =====================================================

print("\nDataset Summary")
print("-" * 40)

print(f"Rows                 : {len(powerbi_df):,}")
print(f"Columns              : {len(powerbi_df.columns)}")

print("\nOutput File")
print("-" * 40)

print(OUTPUT_FILE)

print("\nPower BI Dataset Created Successfully.")