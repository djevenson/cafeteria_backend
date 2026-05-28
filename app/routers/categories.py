from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection

router=APIRouter()

@router.post("/categories")
def set_categories(cat_name:str):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO categories(category_name) VALUES (%s) RETURNING *
        """,
        (cat_name,)
    )
    categorie=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return {"message":"categorie added successfully!!", "categorie":f"{categorie}"}


@router.get("/categories")
def set_categories(cat_id:str):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM categories WHERE category_id=%s 
        """,
        (cat_id,)
    )
    categorie=cursor.fetchone()
    cursor.close()
    connection.close()

    return categorie
