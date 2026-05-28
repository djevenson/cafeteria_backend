from fastapi import APIRouter, HTTPException, Form
from app.database import get_connection

router = APIRouter()

@router.post("/transactions/deposit")
def deposit(
    user_id: int = Form(...),
    amount: float = Form(...)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE id=%s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    cursor.execute(
        """
        INSERT INTO transactions
        (user_id, type, amount, status)

        VALUES (%s, %s, %s, %s)

        RETURNING *
        """,
        (user_id, "deposit", amount, "Validé")
    )

    transaction = cursor.fetchone()

    cursor.execute(
        """
        UPDATE users
        SET balance = balance + %s
        WHERE id = %s
        """,
        (amount, user_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Deposit successful",
        "transaction_id": transaction[0],
        "user_id": transaction[1],
        "type": transaction[2],
        "amount": float(transaction[3]),
        "status": transaction[4]
    }

@router.post("/transactions/withdraw")
def withdraw(
    user_id: int = Form(...),
    amount: float = Form(...)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT balance FROM users
        WHERE id=%s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    balance = float(user[0])

    if balance < amount:

        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    cursor.execute(
        """
        INSERT INTO transactions
        (user_id, type, amount, status)

        VALUES (%s, %s, %s, %s)

        RETURNING *
        """,
        (user_id, "withdrawal", amount, "Validé")
    )

    transaction = cursor.fetchone()

    cursor.execute(
        """
        UPDATE users
        SET balance = balance - %s
        WHERE id=%s
        """,
        (amount, user_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Withdraw successful",
        "transaction_id": transaction[0],
        "user_id": transaction[1],
        "type": transaction[2],
        "amount": float(transaction[3]),
        "status": transaction[4]
    }

@router.get("/transactions/{user_id}")
def get_transactions(user_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM transactions
        WHERE user_id=%s
        ORDER BY date DESC
        """,
        (user_id,)
    )

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions