from fastapi import APIRouter, Form, HTTPException
from app.database import get_connection
from datetime import date

router = APIRouter()


@router.get("/order_products/{order_id}")
def show_order_products(order_id:int):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
        SELECT * FROM order_products WHERE order_id=%s
        """,
        (order_id,)
    )

    order_products=cursor.fetchall()
    if not order_products:
        connection.rollback()
        raise HTTPException(status_code=404, detail="No product have been added yet!!")
    cursor.close()
    connection.close()

    return {"message":"orders products details",
            "details":[
                {       
                "order_id": order_product[0],
                "product_id":order_product[1],
                "quantity":order_product[2],
                "price":order_product[3],
                "delay":order_product[4]      
                }for order_product in order_products
            ]
    }