
from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/carts_products")
def add_product_in_carts(cart_id:int, product_id:int, quantity:int):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM products WHERE product_id = %s
        """
        (product_id,)
    )
    product = cursor.fetchone()
    product_price = product[3]
    total_price = product_price * quantity
    product_stock = product[4]
    if product_stock ==0:
        raise HTTPException(status_code=404, detail={"error" : "This product is done"})
    
    if quantity > product_stock:
        raise HTTPException(status_code=400, detail={"error" : "This product is unsufficient, there are only {product_stock} left"})
    
    stock_info = None
    if product_stock <= 5:
        stock_info = f"There are only {product_stock} available"  

    cursor.execute(
        """
        INSERT INTO carts_products(cart_id, product_id, quantity, price, total)
        VALUES (%s, %s, %s, %s, %s) RETURNING *
        """,
        (cart_id, product_id, quantity, product_price, total_price)
    )
    cart=cursor.fetchone()
    connection.commit()

    cursor.execute(
        """
        UPDATE products
        SET stock = stock - %s
        WHERE product_id = %s
        """,
        (quantity, product_id,)
    )
    connection.commit()

    cursor.execute(
        """
        UPDATE carts
        SET total_amount = total_amount + %s
        WHERE cart_id = %s
        """,
        (total_price, cart_id,)
    )
    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message":"Product added successfully",
        "cart_id":cart[0],
        "product_id":cart[1],
        "quantity":cart[2],
        "price":cart[3],
        "total":cart[4],
        "stock_warning" : stock_info,
    }




@router.get("/carts_products/{cart_id}")
def show_products_in_cart(cart_id:int,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM cart_products WHERE cart_id=%s
        """,
        (cart_id,)
    )
    products=cursor.fetchall()
    cursor.close()
    connection.close()

    return {
        "cart_id":cart_id,
        "products":[
            {
                "product_id":product[1],
                "quantity":product[2],
                "price":product[3],
                "total":product[4]
            }
            for product in products
        ]
    }




@router.put("/carts_products")
def modify_quantity_in_cart(cart_id:int, product_id:int, quantity:int,):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT price, stock FROM products WHERE product_id = %s
        """,
        (product_id,)
    )
    product = cursor.fetchone()

    if product[1] ==0:
        raise HTTPException(status_code=404, detail={"error" : "This product is done"})
    
    if quantity > product[1]:
        raise HTTPException(status_code=400, detail={"error" : "This product is unsufficient, there are only {product[1]} left"})
    
    stock_info = ""
    if product[1] <= 5:
        stock_info = f"There are only {product[1]} available"  

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
        "cart_id":cart_id,
        "product_id":product_id,
        "quantity":quantity,
        "price":product[0],
        "total":product[0] * quantity,
        "stock_warning":stock_info
    }





@router.delete("/carts_products/{product_id}")
def delete_product_in_cart(product_id:int,cart_id:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT quantity FROM carts_products WHERE product_id=%s AND cart_id=%s
        """,
        (product_id, cart_id,)
    )
    result = cursor.fetchone()
    if not result:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "product not found !!")
    quantity = result[0]

    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        DELETE FROM carts_products WHERE product_id=%s AND cart_id=%s
        """,
        (product_id, cart_id,)
    )
    connection.commit()
    cursor.execute(
        """
        UPDATE products
        SET stock = stock + %s
        WHERE product_id = %s
        """,
        (quantity, product_id,)
    )
    connection.commit()

    cursor.execute(
        """
        UPDATE carts
        SET total_amount = total_amount - (quantity * (SELECT price FROM products WHERE product_id = %s))
        WHERE cart_id = %s""",
        (product_id, cart_id,)
    )
    connection.commit()
  
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"product deleted"}

