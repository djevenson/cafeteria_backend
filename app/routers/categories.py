from fastapi import APIRouter, HTTPException, Form
from app.database import get_connection 

router = APIRouter()

@router.post("/categories")
def category(
    category_name:str=Form(...)
):
    
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
            INSERT INTO categories (category_name)
            VALUES(%s) RETURNING *
        """, (category_name,)
    )

    category=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()

    return{
          "message":"Category created !!!",
          "category": category
    }

