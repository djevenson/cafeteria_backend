import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
DATABASE=os.getenv("DATABASE")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")

def get_connection():
    connection=psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
    )
    return connection
