import psycopg2
from config import load_config


def create_tables(command: str):
    """create tables in the PostgreSQL database"""
    conn = None
    try:
        # read the connection parameters
        config = load_config()

        # connect to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
            with conn.cursor() as cur:
                # create the table
                cur.execute(command)
                print("Table created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    create_tables(command=open("sql/create_stores.sql").read())
