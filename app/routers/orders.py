from fastapi import APIRouter, HTTPException, Form
from app.database import get_connection 

router = APIRouter()

@router.post("/order")
def place_order(user_id:int=Form(...)):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO orders (user_id)
        VALUES (%s)
        RETURNING *
        """,
        (user_id,)
    )
    order=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"order placed successfully",
        "order_id":order[0],
        "user_id":order[1],
        "date":order[2],
        "statut":order[3]
    }

@router.get("/orders")
def show_orders():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM orders 
        """
    )
    orders=cursor.fetchall()
    cursor.close()
    connection.close()

    return orders

@router.get("/orders/{users_id}")
def show_orders(user_id,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM orders WHERE user_id=%s
        """,
        (user_id,)
    )
    orders=cursor.fetchall()
    cursor.close()
    connection.close()

    return orders
