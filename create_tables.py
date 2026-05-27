from app.database import get_connection                                                                            
                                                                            
def create_table():
    connection=get_connection()
    cursor=connection.cursor()

    try:
        cursor.execute(
            """
            CREATE SCHEMA IF NOT EXISTS public
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (                                                                              
            id SERIAL PRIMARY KEY,
            last_name VARCHAR(100),
            first_name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            role VARCHAR(25) DEFAULT 'client'
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories
            (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR CHECK(type IN ('Food', 'Drink', 'Dessert')),
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
            price INT,
            stock INT DEFAULT 0,
            description VARCHAR,
            status INT,
            photo_url TEXT,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites
            (
            favorite_id SERIAL PRIMARY KEY,
            user_id INT,
            product_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(product_id) 
            ) 
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS carts
            (
            cart_id SERIAL PRIMARY KEY,
            user_id INT,
            creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expiration TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '24 hours',
            FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS carts_items
            (
            cart_id SERIAL PRIMARY KEY,
            product_id INT,
            quantity INT,
            price INT,
            total INT,
            FOREIGN KEY (cart_id) REFERENCES carts(cart_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id) 
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders
            (
            order_id SERIAL PRIMARY KEY,
            user_id INT,
            total_price INT DEFAULT 0,
            creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expiration TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '3 hours',
            status INT DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_products
            (
            product_id SERIAL PRIMARY KEY,
            order_id INT,
            quantity INT,
            total_price INT,
            unit_price INT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transaction
            (
            transaction_id SERIAL PRIMARY KEY,
            user_id INT,
            type VARCHAR CHECK(type IN ('deposit', 'withdrawal')),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quantity INT,
            status VARCHAR,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        connection.commit()
        print('Tables created successfully!!')
    except Exception as e :
        connection.rollback()
        print(f"error occured during creating table {e} !!")

    finally:
        cursor.close()
        connection.close()
        

create_table()

