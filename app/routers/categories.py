from app.database import get_connection
from fastapi import HTTPException, APIRouter, Form


router=APIRouter()

@router.post("/categories")
def add_category(
    category_name:str=Form(...)
):
    check=category_name.strip().upper()
    connection=get_connection()
    cursor=connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 1 FROM categories WHERE category_name=%s LIMIT 1
            """,
            (check,)
        )
        
        if cursor.fetchone():
            connection.rollback()
            raise HTTPException(status_code=409, detail="category name already exist !!")
    finally:
        cursor.close()
        connection.close()

    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        INSERT INTO categories (category_name)
        VALUES (%s) RETURNING *
        """,
        (check,)
    )
    category = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"category added successfully !!"}, category


@router.delete("/categories/{category_id}")
def del_category(
    category_id:int#=Form(...)
):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM categories WHERE category_id=%s 
        """,
        (category_id,)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "category not found !!")
    
    cursor.execute(
        """
        DELETE FROM categories WHERE category_id=%s
        """,
        (category_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"Category deleted successfully !!"}



@router.get("/categories")
def show_categories():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM categories 
        """
    )
    categories=cursor.fetchall()
    cursor.close()
    connection.close()

    return {
        "Category":categories
    }

   