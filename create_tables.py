import psycopg2
from config import load_config


def create_tables():
    """create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS stores (
            id SERIAL PRIMARY Key
            , store_number INTEGER
            , store_name TEXT NOT NULL
            , street TEXT NOT NULL
            , city TEXT NOT NULL
            , state VARCHAR(2) NOT NULL
            , zip_code VARCHAR(10) NOT NULL
            , phone_number VARCHAR(20) NOT NULL
            , url TEXT NOT NULL
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
                print("Table created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    create_tables()
