from fastapi import APIRouter, HTTPException, Form
from app.database import get_connection 

router = APIRouter()

@router.post("/orders")
def place_order(user_id:int,cart_id:int=Form(...)):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT total_amount FROM carts WHERE cart_id=%s
        """,
        (cart_id,)
    )
    cart=cursor.fetchone()
    if not cart:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="cart not found!!")
    total_amount=cart[0]
    cursor.execute(
        """
        INSERT INTO orders (user_id, total_amount)
        VALUES (%s, %s) RETURNING *
        """,
        (user_id, total_amount,)
    )
    order=cursor.fetchone()
    order_id=order[0]
    order_date=order[2]
    connection.commit()
    cursor.execute(
        """
        SELECT * FROM cart_products WHERE cart_id=%s
        """,
        (cart_id,)
    )
    cart_items=cursor.fetchall()

    for item in cart_items:
        cursor.execute(
            """
            INSERT INTO order_products (order_id, product_id, quantity, price, total)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order_id, item[1], item[2], item[3], item[4])  
        )
        connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"order placed successfully",
        "order_id":order_id ,
        "user_id":user_id,
        "date":order_date,
        "total_amount":total_amount,
        "status":order[3],
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

    return {"message":"orders retrieved successfully",
            "orders":[
                {
                    "order_id":order[0],
                    "user_id":order[1],
                    "total_amount":order[2],
                    "creation":order[3],
                    "expiration":order[4],
                }
                for order in orders
            ]
        }



@router.get("/orders/{user_id}")
def order_by_user(user_id,):
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

    return {"message":"orders retrieved successfully",
            "orders":[
                {
                    "order_id":order[0],
                    "user_id":order[1],
                    "total_amount":order[2],
                    "creation":order[3],
                    "expiration":order[4],
                }
                for order in orders
            ]
        }



@router.put("/orders/{order_id}")
def update_order(order_id:int,status:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        UPDATE orders
        SET status = %s
        WHERE order_id = %s
        """,
       (status,order_id) 
    )
    connection.commit()
    cursor.close()
    connection.close()
    message={
        1: "en cours",
        2: "valider", 
        3: "livrer", 
        4: "payer"
        }.get(status, "status updated")
    return {"message":f"{message}avec succes"}





