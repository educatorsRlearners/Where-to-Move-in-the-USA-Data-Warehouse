import psycopg2
from config import load_config
from constants import CREATE_INTERNET_SPEEDS_SQL, CREATE_STORES_SQL, CREATE_EPA_SLD_SQL, CREATE_ZCTA_TRACT_SQL


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
                # create the raw schema if it doesn't exist
                cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
                print("Schema 'raw' created or already exists.")
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
    create_tables(command=open(CREATE_STORES_SQL).read())
    create_tables(command=open(CREATE_INTERNET_SPEEDS_SQL).read())
    create_tables(command=open(CREATE_EPA_SLD_SQL).read())
    create_tables(command=open(CREATE_ZCTA_TRACT_SQL).read())
