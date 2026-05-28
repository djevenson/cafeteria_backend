from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/carts")
def create_cart(user_id:int, ):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO carts(user_id)
        VALUES (%s) RETURNING *
        """,
        (user_id)
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
    connection.close()

    return {
        "cart_id":cart[0],
        "user_id":cart[1],
        "create_date":cart[2] 
    }


@router.delete("/carts/{cart_id}")
def delete_cart(cart_id:int,):
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
        raise HTTPException(status_code=404,detail= "Cart not found !!")
    
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        DELETE FROM carts WHERE cart_id=%s
        """,
        (cart_id,)
    )
    cursor.close()
    connection.close()

    return {"message":"carts ready for your products"}

