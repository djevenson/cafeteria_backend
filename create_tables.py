from app.database import get_connection                                                                            
                                                                            
def create_table():
    connection=get_connection()
    cursor=connection.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clients
            (                                                                              
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            role VARCHAR(25)
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories
            (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(50)
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products
            (
            product_id SERIAL PRIMARY KEY,
            category_id INT,
            name VARCHAR(100) UNIQUE,
            price INT DEFAULT 0,
            stock INT DEFAULT 0,
            description VARCHAR,
            photo_url TEXT,
            datetime DATE,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites
            (
            client_id INT,
            product_id INT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (product_id) REFERENCES products(product_id) 
            ) 
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders
            (
            order_id SERIAL PRIMARY KEY,
            client_id INT,
            date DATE,
            status VARCHAR,
            FOREIGN KEY (client_id) REFERENCES clients(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_products
            (
            order_id INT,
            product_id INT,
            quantity INT,
            price INT,
            delay DATE,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """
        )
        connection.commit()
        print('Tables created successfully!!')
    except Exception :
        connection.rollback()
        print("error occured during creating table !!")

    finally:
        cursor.close()
        connection.close()
        

create_table()

