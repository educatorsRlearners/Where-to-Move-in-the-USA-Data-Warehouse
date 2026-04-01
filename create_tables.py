import psycopg2
from config import load_config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS stores (
            store_id SERIAL PRIMARY KEY,
            store_name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            state VARCHAR(255) NOT NULL,
            zip_code VARCHAR(20) NOT NULL,
            phone_number VARCHAR(20) NOT NULL
        )
        """,
    )
    conn = None
    try:
        # read the connection parameters
        config = load_config()

        # connect to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
            with conn.cursor() as cur:
                # create table one by one
                for command in commands:
                    cur.execute(command)
                print("Tables created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")