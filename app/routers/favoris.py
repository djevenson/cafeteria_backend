from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/favoris")
def add_to_favoris(
    user_id:int=Form(...),
    product_id:int=Form(...)
):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM favoris WHERE user_id=%s AND product_id=%s 
        """,
        (user_id,product_id)
    )
    if cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=409,detail= "product already in favoris !!")
    
    cursor.execute(
        """
        INSERT INTO favoris (user_id, product_id)
        VALUES (%s, %s)
        """,
        (user_id, product_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":f"user {user_id} added product {product_id} to favoris successfully!!!"
    }
    

@router.get("/favoris/{user_id}")
def get_favoris(user_id:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT product_id FROM favoris WHERE user_id=%s   
        """,
        (user_id)
    )
    favoris=cursor.fetchall()
    if not favoris:
        raise HTTPException(status_code=404, detail="Any products in favoris")
    cursor.close()
    connection.close()
    return {
        "message":"here are your favoris",
        "favoris":favoris
    }


@router.delete("/favoris")
def delete_favoris(user_id:int, product_id:int): 
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM favoris WHERE user_id=%s AND product_id=%s 
        """,
        (user_id,product_id)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "product not found !!")
    
    cursor.execute(
        """
        DELETE FROM favoris WHERE user_id=%s AND product_id=%s 
        """,
        (user_id,product_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message":"product out of your favoris"
    }
    