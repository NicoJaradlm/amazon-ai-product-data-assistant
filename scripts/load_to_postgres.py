import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

CLEANED_DATA_PATH = Path("data/processed/amazon_cleaned.csv")

DATABASE_URL = "postgresql://admin:admin@localhost:5432/amazon_products_db"


def main():
    print("Loading cleaned Amazon data into PostgreSQL...")
    print("-" * 60)

    df = pd.read_csv(CLEANED_DATA_PATH)

    print(f"Rows loaded from CSV: {df.shape[0]}")
    print(f"Columns loaded from CSV: {df.shape[1]}")

    engine = create_engine(DATABASE_URL)

    # Create product-level table
    product_columns = [
        "product_id",
        "product_name",
        "category",
        "main_category",
        "sub_category",
        "discounted_price",
        "actual_price",
        "discount_percentage",
        "rating",
        "rating_count",
        "about_product",
        "img_link",
        "product_link",
    ]

    products_df = df[product_columns].drop_duplicates(subset=["product_id"])

    # Create review-level table
    review_columns = [
        "product_id",
        "user_id",
        "user_name",
        "review_id",
        "review_title",
        "review_content",
    ]

    reviews_df = df[review_columns].drop_duplicates(
        subset=["product_id", "review_title", "review_content"]
    )

    print(f"Unique products: {products_df.shape[0]}")
    print(f"Review records: {reviews_df.shape[0]}")

    # Load into PostgreSQL
    products_df.to_sql(
        "products",
        engine,
        if_exists="replace",
        index=False
    )

    reviews_df.to_sql(
        "reviews",
        engine,
        if_exists="replace",
        index=False
    )

    # Quick validation from PostgreSQL
    with engine.connect() as connection:
        product_count = connection.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar()

        review_count = connection.execute(
            text("SELECT COUNT(*) FROM reviews")
        ).scalar()

    print("\nPostgreSQL load complete")
    print("-" * 60)
    print(f"Products table rows: {product_count}")
    print(f"Reviews table rows: {review_count}")


if __name__ == "__main__":
    main()