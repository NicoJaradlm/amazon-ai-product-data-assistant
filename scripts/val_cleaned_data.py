import pandas as pd
from pathlib import Path

CLEANED_DATA_PATH = Path("data/processed/amazon_cleaned.csv")
DUPLICATE_OUTPUT_PATH = Path("data/processed/duplicate_product_review_records.csv")
PRODUCT_ID_DUPES_OUTPUT_PATH = Path("data/processed/duplicate_product_ids.csv")


def main():
    df = pd.read_csv(CLEANED_DATA_PATH)

    print("Cleaned dataset validation")
    print("-" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    # --------------------------------------------------
    # Numeric validation
    # --------------------------------------------------
    numeric_columns = [
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]

    print("\nNumeric column summary:")
    print(df[numeric_columns].describe())

    print("\nMissing values in numeric columns:")
    print(df[numeric_columns].isna().sum())

    # --------------------------------------------------
    # Duplicate validation
    # --------------------------------------------------
    print("\nExact full-row duplicates:")
    print(df.duplicated().sum())

    print("\nDuplicate product_id count:")
    duplicate_product_id_count = df["product_id"].duplicated().sum()
    print(duplicate_product_id_count)

    print("\nDuplicate product review records based on:")
    print("product_id + review_title + review_content")

    duplicate_review_count = df.duplicated(
        subset=["product_id", "review_title", "review_content"]
    ).sum()

    print(f"Duplicate product review records: {duplicate_review_count}")

    # Export duplicate product review records if any remain
    duplicate_review_records = df[
        df.duplicated(
            subset=["product_id", "review_title", "review_content"],
            keep=False
        )
    ].copy()

    if not duplicate_review_records.empty:
        duplicate_review_records = duplicate_review_records.sort_values(
            by=["product_id", "review_title", "review_content"]
        )

        columns_to_export = [
            "product_id",
            "product_name",
            "main_category",
            "sub_category",
            "discounted_price",
            "actual_price",
            "discount_percentage",
            "rating",
            "rating_count",
            "user_id",
            "user_name",
            "review_id",
            "review_title",
            "review_content",
        ]

        duplicate_review_records[columns_to_export].to_csv(
            DUPLICATE_OUTPUT_PATH,
            index=False
        )

        print(f"\nDuplicate review records exported to: {DUPLICATE_OUTPUT_PATH}")
    else:
        print("\nNo duplicate product review records found.")

    # --------------------------------------------------
    # Product ID duplicate inspection
    # --------------------------------------------------
    duplicated_product_ids = df[df["product_id"].duplicated(keep=False)].copy()

    if not duplicated_product_ids.empty:
        duplicated_product_ids = duplicated_product_ids.sort_values(
            by=["product_id", "review_id", "user_id"]
        )

        columns_to_export = [
            "product_id",
            "product_name",
            "main_category",
            "sub_category",
            "discounted_price",
            "actual_price",
            "discount_percentage",
            "rating",
            "rating_count",
            "user_id",
            "user_name",
            "review_id",
            "review_title",
            "review_content",
        ]

        duplicated_product_ids[columns_to_export].to_csv(
            PRODUCT_ID_DUPES_OUTPUT_PATH,
            index=False
        )

        print(f"\nRows with duplicated product_id exported to: {PRODUCT_ID_DUPES_OUTPUT_PATH}")
        print(f"Rows exported: {duplicated_product_ids.shape[0]}")
    else:
        print("\nNo duplicated product_id rows found.")

    # --------------------------------------------------
    # Category validation
    # --------------------------------------------------
    print("\nTop main categories:")
    print(df["main_category"].value_counts().head(10))

    print("\nTop subcategories:")
    print(df["sub_category"].value_counts().head(10))

    # --------------------------------------------------
    # Sample cleaned rows
    # --------------------------------------------------
    print("\nSample cleaned rows:")
    sample_columns = [
        "product_id",
        "product_name",
        "main_category",
        "sub_category",
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
    ]

    print(df[sample_columns].head())


if __name__ == "__main__":
    main()