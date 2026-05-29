from fastapi import APIRouter,HTTPException ,Form
from app.database import get_connection

router=APIRouter()

@router.post("/users")
def add_user(
    first_name:str=Form(...),
    last_name:str=Form(...),
    email:str=Form(...),
    balance:int=Form(...)
):
    connection=get_connection()
    cursor=connection.cursor()

    check_email=f"{email.strip()}"
    try:
        cursor.execute(
            """
            SELECT 1 FROM users WHERE email=%s LIMIT 1
            """,
            (check_email,)
            )
    
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="email already exist !!")
        
    finally:
        cursor.close()
        connection.close()

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (first_name, last_name, email, balance)
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """,
        (first_name, last_name, email, balance)
    )

    user=cursor.fetchone()
    user_id=user[0]
    
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "user_id":user_id,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "balance": balance
    }


@router.get("/users")
def  get_users():
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        """
    )
    users=cursor.fetchall()
    cursor.close()
    connection.close()

    return users


@router.get("/users/{user_id}")
def  get_users(user_id:int):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users WHERE id=%s
        """,
        (user_id,)
    )
    user=cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!!")
    cursor.close()
    connection.close()

    return user

@router.get("/users/search/q")
def search_produits(q:str):
    connection = get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT * FROM users WHERE first_name ILIKE %s
        """,
        (f"%{q}%",)
    )
    result=cursor.fetchall()
    if not result:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="user not found")
    cursor.close()
    connection.close()

    return result

@router.put("/users/profil/{user_id}")
def edit_role(
    user_id:int,
    first_name:str=Form(None),
    last_name:str=Form(None)          
):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT first_name, last_name FROM users WHERE id=%s
        """,
        (user_id,)
    )
    exist=cursor.fetchone()
    if not exist:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="user not found")
    
    new_f_name = first_name if first_name is not None else exist[0]
    new_l_name = last_name if last_name is not None else exist[1]
     
    cursor.execute(
        """
        UPDATE users SET first_name=%s, last_name=%s WHERE id=%s RETURNING *
        """,
        (new_f_name,new_l_name,user_id)
    )
    user=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"user modified successfully"}, user
    
@router.delete("/users/{user_id}")
def del_user(user_id:int):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT first_name, last_name FROM users WHERE id=%s
        """,
        (user_id,)
    )
    exist=cursor.fetchone()
    if not exist:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="user not found")
    cursor.execute(
        """
        DELETE FROM users WHERE id=%s
        """,
        (user_id,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {"message":"user deleted successfully"}
