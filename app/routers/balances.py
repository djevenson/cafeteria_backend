from fastapi import APIRouter, HTTPException, Form
from app.database import get_connection

router = APIRouter()

@router.get("/balance/{user_id}")
def get_balance(user_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT balance
        FROM users
        WHERE id=%s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user_id,
        "balance": float(user[0])
    }