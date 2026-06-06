from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin@localhost:5432/amazon_products_db"

engine = create_engine(DATABASE_URL)