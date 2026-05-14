import psycopg2

import pandas as pd
from typing import List, Optional

from config import load_config
from create_tables import create_tables
from insert_data import insert_df
from upsert_data import upsert_dataframe_batch


def _table_exists(table_name: str, config_func=load_config) -> bool:
    schema, table = table_name.split(".")
    config = config_func()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = %s
                )
                """,
                (schema, table),
            )
            return cur.fetchone()[0]


def load_df(
    df: pd.DataFrame,
    table_name: str,
    conflict_column: str,
    sql_file: str,
    columns: Optional[List[str]] = None,
    config_func=load_config,
) -> int:
    """
    Smart load: creates the table and uses fast bulk INSERT (COPY) on first run.
    On subsequent runs, upserts into the existing table using ON CONFLICT.
    """
    if columns is None:
        columns = [col for col in df.columns if col != "id"]

    if not _table_exists(table_name, config_func):
        create_tables(command=open(sql_file).read())
        insert_df(df, table_name, columns=columns)
        return len(df)

    return upsert_dataframe_batch(
        df, table_name, conflict_column, columns=columns, config_func=config_func
    )
