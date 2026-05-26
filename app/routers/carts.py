from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/carts")
def create_cart(order_id:int, quantity:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO carts(order_id, quantity)
        VALUES (%s) RETURNING *
        """,
        (order_id, quantity,)
    )
    cart=cursor.fetchone()
    cursor.close()
    connection.close()

    return {
        "message":"carts ready for your products",
        "cart_id":cart[0],
        "user_id":cart[1],
        "create_date":cart[2],
    }

@router.put("/carts")
def modify_carts(quantity:int,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO carts(quantity)
        VALUES (%s) RETURNING *
        """,
        (quantity,)
    ) 
    
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"quantity has been modified",
        "quantity=quantity"

    }


@router.get("/carts/{cart_id}")
def show_cart(cart_id:int,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM carts WHERE cart_id=%s
        """,
        (cart_id,)
    )
    cart=cursor.fetchone()
    cursor.close()
    connection.cose()

    return {
        "cart_id":cart[0],
        "user_id":cart[1],
        "create_date":cart[2] 
    }


@router.delete("/carts/{cart_id}")
def show_cart(cart_id:int,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM carts WHERE cart_id=%s 
        """,
        (cart_id,)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "category not found !!")
    
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        DELETE * FROM carts WHERE cart_id=%s
        """,
        (cart_id,)
    )
    cursor.close()
    connection.cose()

    return {"message":"carts ready for your products"}

