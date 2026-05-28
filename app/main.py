from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cart_products, users, products, orders, order_products, carts, categories, favorites

app=FastAPI(
    title="API"
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")
app.include_router(users.router,tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(favorites.router,tags=["favorites"])
app.include_router(categories.router,tags=["categories"])
app.include_router(orders.router,tags=["orders"])
app.include_router(order_products.router, tags=["order_products"])
app.include_router(carts.router,tags=["carts"])
app.include_router(cart_products.router,tags=["cart_products"])