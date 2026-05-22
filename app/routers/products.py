import os
import uuid
from app.database import get_connection
from fastapi import APIRouter,HTTPException, UploadFile, File, Form

router=APIRouter()

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)


#====ENDPOINT TO ADD A PRODUCT======#
@router.post("/products")
async def add_products(
    name:str=Form(...),
    price:int=Form(0),
    stock:int=Form(0),
    description:str=Form(...),
    photo:UploadFile=File(...),
    category:str=Form(...)
):
    extention=photo.filename.split(".")[-1]
    photo_name=f"{uuid.uuid4()}.{extention}"
    photo_path=os.path.join(UPLOAD_DIR,photo_name)
    photo_path_name=photo_path.replace("\\","/")

    connection=get_connection()
    cursor=connection.cursor()

    check_name=name.strip()
    try:
        cursor.execute(
            """
            SELECT 1 FROM products WHERE name=%s LIMIT 1
            """,
            (check_name,)
        )
        
        if cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product name already exist !!")
    finally:
        cursor.close()
        connection.close()
        
    connection=get_connection()
    cursor=connection.cursor()
    
    cursor.execute(
        """
        INSERT INTO products (name, price, stock, description, photo_url, category)
        VALUES (%s, %s, %s, %s, %s,%s) RETURNING *
        """,
        (name, price, stock, description, photo_path_name, category)
    )

    products_id=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    with open (photo_path_name,"wb")as f:
        f.write(await photo.read())

    return {
        "message":"product added succesfully!!",
        "product_id":products_id,
        "name":name,
        "price":price,
        "stock":stock,
        "description":description,
        "photo_url":f"http://localhost:8000/{photo_path_name}",
        "category":category
    }



#====ENDPOINT SHOW ALL PRODUCTS======#
@router.get("/products")
def get_products():
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM products
        """
    )

    products=cursor.fetchall()
    if not products:
        raise HTTPException(status_code=404, detail="No product have been added yet!!")
    cursor.close()
    connection.close()

    return products


#====ENDPOINT TO GET ON PRODUCT WITHM ID======#
@router.get("/products/{product_id}")
def get_product(product_id:int):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM products WHERE id=%s
        """,
        (product_id,)
    )

    product=cursor.fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!!")
    cursor.close()
    connection.close()

    return product

