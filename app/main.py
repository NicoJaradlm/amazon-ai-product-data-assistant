from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Amazon AI Product Data Engineering Assistant",
    description="API for querying cleaned Amazon product and review data from PostgreSQL.",
    version="0.1.0"
)

app.include_router(router)