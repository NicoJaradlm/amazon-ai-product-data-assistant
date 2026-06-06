import pandas as pd
from fastapi import APIRouter
from app.database import engine

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/products/count")
def get_product_count():
    query = """
        SELECT COUNT(*) AS product_count
        FROM products;
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")[0]


@router.get("/reviews/count")
def get_review_count():
    query = """
        SELECT COUNT(*) AS review_count
        FROM reviews;
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")[0]


@router.get("/categories/products")
def get_products_by_category():
    query = """
        SELECT
            main_category,
            COUNT(*) AS product_count
        FROM products
        GROUP BY main_category
        ORDER BY product_count DESC;
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")


@router.get("/products/top-rated")
def get_top_rated_products():
    query = """
        SELECT
            product_id,
            product_name,
            main_category,
            rating,
            rating_count,
            discounted_price,
            actual_price
        FROM products
        WHERE rating >= 4.3
          AND rating_count >= 1000
        ORDER BY rating DESC, rating_count DESC
        LIMIT 20;
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")


@router.get("/categories/discounts")
def get_average_discount_by_category():
    query = """
        SELECT
            main_category,
            ROUND(AVG(discount_percentage), 2) AS avg_discount_percentage,
            COUNT(*) AS product_count
        FROM products
        GROUP BY main_category
        ORDER BY avg_discount_percentage DESC;
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")