from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/carts_items")
def add_to_carts(
    cart_id:int,
    product_id:int,
    quantity:int
):  
    
    connection=get_connection()
    cursor=connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 1 FROM products WHERE prduct_id=%s LIMIT 1
            """,
            (product_id,)
        )
        product_price=cursor.fetchone()
        if not product_price:
            raise HTTPException(status_code=404, detail="Product not found !!")
    finally:
        cursor.close()
        connection.close()
    total_price= product_price*quantity
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO cart_item(cart_id,product_id, product_price, quantity, total_price)
        VALUES (%s, %s, %s, %s, %s) RETURNING *
        """,
        (cart_id, product_id,product_price,quantity,total_price)
    )
    
    cart_item=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"carts ready for your products",
        "cart_item_id":cart_item[0],
        "cart_id":cart_item[1],
        " product_id":cart_item[2],
        "product_price":cart_item[3],
        "quantity":cart_item[4],
        "total_price":cart_item[5]
    }


@router.get("/cart_items/{cart_id}")
def show_carts_item(cart_id:int):
    connection=get_connection()
    cursor = connection.cursor()
    cursor.execute(
            """
            SELECT * FROM cart_items WHERE cart_id=%s 
            """,
            (cart_id,)
    )
    carts_items=cursor.fetchall()
    cursor.close()
    connection.close()
    return carts_items
    

@router.put("/cart_items/{cart_item_id}")
def edit_item_on_cart(
    cart_item_id:int,
    quantity:int
):
    connection=get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 1 FROM cart_items WHERE cart_item_id=%s LIMIT 1
            """,
            (cart_item_id,)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found !!")
    finally:
        cursor.close()
        connection.close()

    connection=get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE cart_items SET quantity=%s WHERE cart_item_id=%s
        """,
        (quantity,cart_item_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {f"new quantity quantity update successfully!!"} 


@router.delete("/cart_items/{cart_item_id}")
def move_from_cart(cart_item_id:int):
    connection=get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 1 FROM cart_items WHERE cart_item_id=%s LIMIT 1
            """,
            (cart_item_id,)
        )
        if cursor.fetchone():
            cursor.execute(
                """
                DELETE * FROM cart_item WHERE cart_item_id=%s
                """,
                (cart_item_id,)
            )
            return {"product deleted to cart successfully!!"}
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found !!")
    finally:
        cursor.close()
        connection.close()