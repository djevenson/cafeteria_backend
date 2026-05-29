from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/favorites")
def add_to_favorites(
    user_id:int=Form(...),
    product_id:int=Form(...)
):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT last_name FROM users WHERE id=%s
        """,
        (user_id,)
    )
    last_name = cursor.fetchone()[0]
    if not last_name:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="User not found!!")

    cursor.execute(
        """
        SELECT name FROM products WHERE product_id=%s
        """,
        (product_id,)
    )
    product_name = cursor.fetchone()[0]
    if not product_name:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Product not found!!")
    
    cursor.execute(
        """
        SELECT * FROM favorites WHERE user_id=%s AND product_id=%s 
        """,
        (user_id,product_id)
    )
    if cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=409,detail= "product already in favorites !!")
    
    cursor.execute(
        """
        INSERT INTO favorites (user_id, product_id)
        VALUES (%s, %s)
        """,
        (user_id, product_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":f"user '{last_name}' added product '{product_name}' to favorites successfully!!!"
    }
    

@router.get("/favorites/{user_id}")
def get_favorites(user_id:int,):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT product_id FROM favorites WHERE user_id=%s   
        """,
        (user_id,)
    )
    favoris_id=cursor.fetchall()
    if not favoris_id:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Any products in favorites")
    favoris = []
    for favorite in favoris_id:
        cursor.execute(
            """
            SELECT * FROM products WHERE product_id=%s
            """,
            (favorite[0],)
        )
        product = cursor.fetchone()
        favoris.append(product)

    cursor.close()
    connection.close()
    return {
        "message":"here are your favorites",
        "favoris": [
            {
                "product_id": product[0],
                "category_id": product[1],
                "name": product[2],
                "price": product[3],
                "stock": product[4],
                "description": product[5],
                "photo_url": product[6]
            } for product in favoris
        ]
    }


@router.delete("/favorites")
def delete_favorites(user_id:int, product_id:int): 
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM favorites WHERE user_id=%s AND product_id=%s 
        """,
        (user_id,product_id)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "product not found !!")
    
    cursor.execute(
        """
        DELETE FROM favorites WHERE user_id=%s AND product_id=%s 
        """,
        (user_id,product_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"product out of your favorites"
    }
    
