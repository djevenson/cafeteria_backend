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
    price:int=Form(...),
    stock:int=Form(...),
    description:str=Form(...),
    photo:UploadFile=File(...),
    category_id:int=Form(...)
):
    ext=photo.filename.rsplit(".",1)[-1]
    photo_name=f"{uuid.uuid4()}.{ext}"
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
        INSERT INTO products (name, price, stock, description, photo_url, category_id)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING *
        """,
        (name, price, stock, description, photo_path_name, category_id)
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
        "photo_url":f"{photo_path_name}",
        "category_id":category_id
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
        connection.rollback()
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

@router.get("/search/products")
def search_produits(q:str):
    connection = get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM products WHERE name ILIKE %s
        """,
        (f"%{q}%",)
    )
    result=cursor.fetchall()
    cursor.close()
    connection.close()

    return result



@router.put("/products/{product_id}")
async def edit_product(
    product_id:int,
    name:str=Form(None),
    price:int=Form(None),
    stock:int=Form(None),
    description:str=Form(None),
    photo:UploadFile=File(None),
    category_id:int=Form(None)
):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM products WHERE product_id=%s
        """,
        (product_id,)
    )

    existing = cursor.fetchone()  # ← stocker ici

    if not existing:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Product not found!!")

    # Fusion ancienne/nouvelle valeur
    new_category_id = category_id if category_id is not None else existing[1]
    new_name        = name        if name        is not None else existing[2]
    new_price       = price       if price       is not None else existing[3]
    new_stock       = stock       if stock       is not None else existing[4]
    new_description = description if description is not None else existing[5]
    new_photo_url   = existing[6]

    # Nouvelle photo seulement si envoyée
    if photo and photo.filename != "":
        new_photo_url = f"uploads/{photo.filename}"
        with open(new_photo_url, "wb") as f:
            f.write(await photo.read())

    # Vérification nom unique seulement si changé
    if new_name != existing[2]:
        cursor.execute(
            "SELECT 1 FROM products WHERE name=%s AND product_id != %s",
            (new_name, product_id)
        )
        if cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=400, detail="Product name already exists!!")

    cursor.execute(
        """
        UPDATE products SET category_id=%s, name=%s, price=%s, stock=%s, description=%s, photo_url=%s
        WHERE product_id=%s RETURNING *
        """,
        (new_category_id, new_name, new_price, new_stock, new_description, new_photo_url, product_id,)
    )

    product=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {"Message":"Product modified successfully!!!"}, product




@router.delete("/products/{product_id}")
def del_product(
    product_id:int#=Form(...)
):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT photo_url FROM products WHERE product_id=%s 
        """,
        (product_id,)
    )
    product=cursor.fetchone()
    if not product :
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404,detail= "product not found !!")
    
    photo_path=product[0]

    cursor.execute(
        """
        DELETE FROM products WHERE product_id=%s
        """,
        (product_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    if photo_path and os.path.exists(photo_path):
        os.remove(photo_path)



    return {"message":"Product deleted successfully !!"}




   