from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import users, products, favoris, categories, orders, order_products, carts, cart_items

app=FastAPI(
    title="API"
    )

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")
app.include_router(users.router,tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(favoris.router,tags=["favoris"])
app.include_router(categories.router,tags=["categories"])
app.include_router(orders.router,tags=["orders"])
app.include_router(order_products.router, tags=["order_products"])
app.include_router(carts.router,tags=["carts"])
app.include_router(cart_items.router,tags=["cart_items"])