from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import users, products, favoris, categories, orders

app=FastAPI(
    title="API"
    )

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")
app.include_router(users.router,tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(favoris.router,tags=["favoris"])
app.include_router(categories.router,tags=["categories"])
app.include_router(orders.router,tags=["orders"])