from fastapi import APIRouter,HTTPException ,Form
from app.database import get_connection

router=APIRouter()

@router.post("/users")
def add_user(
    name:str=Form(...),
    email:str=Form(...)
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
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        RETURNING *
        """,
        (name, email)
    )

    user=cursor.fetchone()
    user_id=user[0]
    account=user[3]
    
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "user_id":user_id,
        "name":name,
        "email":email,
        "account":account
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


@router.put("/users/{user_id}")
def topup_user(
    user_id:int,
    amount:int=Form(0)     
):
    connection=get_connection()
    cursor=connection.cursor()
    
    cursor.execute(
        """
        SELECT * FROM users WHERE id=%s
        """,
        (user_id,)
    )
    exist=cursor.fetchone()
    if not exist:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="User not found!!")
        
    cursor.execute(
        """
        UPDATE users SET account=account+%s WHERE id=%s RETURNING *
        """,
        (amount,user_id,)
    )
    user=cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    return {"Message":"Account topup successfully!!!"}, user
