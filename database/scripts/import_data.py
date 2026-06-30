import pandas as pd
from sqlalchemy import create_engine, text

# =====================================================
# PostgreSQL Connection
# =====================================================

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/water_db"

engine = create_engine(DATABASE_URL)

# =====================================================
# CSV Files
# =====================================================

FILES = [
    ("wells", "database/seed/wells.csv"),
    ("rainfall", "database/seed/rainfall.csv"),
    ("weather", "database/seed/weather.csv"),
    ("pumping", "database/seed/pumping.csv"),
    ("groundwater_levels", "database/seed/groundwater.csv"),
]

# =====================================================
# Clear Existing Data
# =====================================================

print("\nCleaning existing data...\n")

with engine.begin() as conn:

    conn.execute(text("TRUNCATE groundwater_levels RESTART IDENTITY CASCADE;"))
    conn.execute(text("TRUNCATE pumping RESTART IDENTITY CASCADE;"))
    conn.execute(text("TRUNCATE rainfall RESTART IDENTITY CASCADE;"))
    conn.execute(text("TRUNCATE weather RESTART IDENTITY CASCADE;"))
    conn.execute(text("TRUNCATE wells RESTART IDENTITY CASCADE;"))

print("Database cleaned.\n")

# =====================================================
# Import Data
# =====================================================

total_rows = 0

for table, file in FILES:

    print(f"Importing {table}...")

    df = pd.read_csv(file)

    df.to_sql(
        table,
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )

    print(f"✓ {len(df)} rows")

    total_rows += len(df)

print("\n==============================")
print("Import Complete")
print("==============================")

for table, file in FILES:
    rows = len(pd.read_csv(file))
    print(f"{table:<22} {rows}")

print("------------------------------")
print(f"TOTAL ROWS IMPORTED : {total_rows}")
print("==============================")