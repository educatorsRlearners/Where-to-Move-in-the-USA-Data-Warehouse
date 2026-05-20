from io import StringIO

import pandas as pd
import psycopg2

from config import load_config
from typing import List, Optional


def insert_df(df: pd.DataFrame, table_name: str, columns: Optional[List[str]] = None, config_func=load_config):
    """
    Inserts a dataframe into a Postgresql table using the copy command for extremely fast insertion.

    Args:
        df (pd.DataFrame): Dataframe to be inserted into the table
        table_name (str): Name of the table where the data is to be inserted (can include schema: "schema.table")
        columns (Optional[List[str]], optional): Column names. Defaults to None.
    """
    config = config_func()
    csv_buffer = StringIO()
    df[columns].to_csv(csv_buffer, index=False, na_rep="\\N", header=False)
    csv_buffer.seek(0)

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            columns_str = ", ".join(columns) if columns else ""
            copy_sql = f"COPY {table_name} ({columns_str}) FROM STDIN WITH (FORMAT csv, NULL '\\N')"
            cur.copy_expert(copy_sql, csv_buffer)
            conn.commit()

    print(f"✅ {len(df)} rows inserted in <1 second!")
