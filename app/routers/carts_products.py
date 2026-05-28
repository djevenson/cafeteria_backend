from fastapi import APIRouter, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/carts_products")
def add_product_in_carts(cart_id:int, product_id:int, quantity:int):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT stock FROM products WHERE product_id = %s
        """,
        (product_id,)
    )
    product = cursor.fetchone()

    if product[0] ==0:
        return {"error" : "This product is done"}
    
    if quantity > product[0]:
        return {"error" : "This product is unsufficient, there are only {product[0]} left"}
    
    stock_info = None
    if product[0] <= 5:
        stock_info = f"There are only {product[0]} available"  

    cursor.execute(
        """
        INSERT INTO carts_products(cart_id, product_id, quantity)
        VALUES (%s, %s, %s) RETURNING *
        """,
        (cart_id, product_id, quantity)
    )
    cart=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"Product added successfully",
        "stock_warning" : stock_info
    }

@router.put("/carts_products")
def modify_quantity_in_cart(cart_id:int, product_id:int, quantity:int):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT stock FROM products WHERE product_id = %s
        """,
        (product_id)
    )

    product = cursor.fetchone()

    if product[0] ==0:
        return {"error" : "This product is done"}
    
    if quantity > product[0]:
        return {"error" : "This product is unsufficient, there are only {product[0]} left"}
    
    stock_info = None
    if product[0] <= 5:
        stock_info = f"There are only {product[0]} available"  

    cursor.execute(
        """
        UPDATE carts_products
        SET quantity = %s
        WHERE cart_id = %s AND product_id = %s
        """,
        (quantity, cart_id, product_id)
    ) 
    
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"quantity has been modified",
        "quantity":quantity,
        "stock_warning":stock_info

    }

@router.put("/carts_products/change product")
def modify_product_in_cart(cart_id:int, old_product_id:int, new_product_id:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        UPDATE carts_products
        SET product_id = %s
        WHERE cart_id = %s AND product_id =%s
        """,
        (new_product_id, cart_id, old_product_id)
    ) 
    
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"product has been modified",
        }

@router.delete("/carts_products/{product_id}")
def delete_product_in_cart(product_id:int,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM carts_products WHERE product_id=%s 
        """,
        (product_id,)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "product not found !!")
    
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        DELETE FROM carts_products WHERE product_id=%s
        """,
        (product_id,)
    )
    cursor.close()
    connection.close()

    return {"message":"product deleted"}

