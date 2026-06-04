import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/amazon.csv")
PROCESSED_DATA_PATH = Path("data/processed/amazon_cleaned.csv")


def clean_numeric(value):
    """
    Cleans messy numeric strings like:
    '₹1,099' or 'â‚¹1,099' -> 1099.0
    '64%' -> 64.0
    '24,269' -> 24269.0
    """
    if pd.isna(value):
        return None

    cleaned = (
        str(value)
        .replace(",", "")
        .replace("%", "")
        .strip()
    )

    # Keep only digits, decimal points, and minus signs
    cleaned = "".join(
        char for char in cleaned
        if char.isdigit() or char in [".", "-"]
    )

    if cleaned == "":
        return None

    return float(cleaned)


def main():
    df = pd.read_csv(RAW_DATA_PATH)

    numeric_columns = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]

    for col in numeric_columns:
        df[col] = df[col].apply(clean_numeric)

    # Split category into main category and subcategory
    df["main_category"] = df["category"].str.split("|").str[0]
    df["sub_category"] = df["category"].str.split("|").str[-1]

    # Save cleaned data
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Cleaned dataset saved successfully")
    print("-" * 50)
    print(f"Output path: {PROCESSED_DATA_PATH}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nUpdated data types:")
    print(df[numeric_columns + ["main_category", "sub_category"]].dtypes)

    print("\nMissing values in key numeric fields:")
    print(df[numeric_columns].isna().sum())

    print("\nSample cleaned values:")
    print(df[numeric_columns + ["main_category", "sub_category"]].head())


if __name__ == "__main__":
    main()