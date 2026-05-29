import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/amazon.csv")


def main():
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully")
    print("-" * 50)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nSample values per column:")
    for col in df.columns:
        print(f"\n{col}:")
        print(df[col].head(3).tolist())


if __name__ == "__main__":
    main()