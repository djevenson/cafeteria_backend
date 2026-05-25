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
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            role VARCHAR(25) DEFAULT 'user'
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories
            (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(50) UNIQUE
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
            price FLOAT DEFAULT 0,
            stock INT DEFAULT 0,
            description VARCHAR,
            photo_url TEXT,
            datetime DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites
            (
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
            create_date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cart_items 
            (
            cart_item_id PRIMARY KEY,
            cart_id,
            product_id,
            product_price FLOAT,
            FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
            FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """
        )


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS status
            (
            status_id SERIAL PRIMARY KEY,
            status_name VARCHAR(100) UNIQUE
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO status (status_name) VALUES
            ('Waiting')
            ('Pending')
            ('Done')
            ('Canceled')
            ON CONFLICT (status_name) DO NOTHING;
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders
            (
            order_id SERIAL PRIMARY KEY,
            user_id INT,
            tot_price FLOAT,
            date DATE DEFAULT CURRENT_DATE,
            status VARCHAR DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users(id)
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
            price FLOAT,
            delay DATE,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
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

