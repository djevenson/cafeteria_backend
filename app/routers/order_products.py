from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection
from datetime import date

router = APIRouter()

@router.post("/order_products")
def order_products(
    order_id:int=Form(...),
    product_id:int=Form(...),
    quantity:int=Form(...),
    price:int=Form(...),
    delay:date=Form(...)

):
    connection = get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO order_products (order_id, product_id, quantity, price, delay) VALUES (%s, %s, %s, %s, %s) RETURNING *
        """, 
        (order_id, product_id, quantity, price, delay)
    )

    order_products = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return{
        "message":"Tout bg sou control",
        "order_id": order_products[0],
        "product_id":order_products[1],
        "quantity":order_products[2],
        "price":order_products[3],
        "delay":order_products[4]
    }