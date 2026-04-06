from io import StringIO

import pandas as pd
import psycopg2

from config import load_config
from typing import List, Optional


def insert_df(df: pd.DataFrame, table_name: str, columns: Optional[List[str]] = None):
    """_summary_

    Args:
        df (pd.DataFrame): Dataframe to be inserted into the table
        table_name (str): Name of the table where the data is to be inserted
        columns (Optional[List[str]], optional): Column names. Defaults to None.
    """
    config = load_config()
    csv_buffer = StringIO()
    df[columns].to_csv(csv_buffer, index=False, na_rep="\\N", header=False)
    csv_buffer.seek(0)

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.copy_from(csv_buffer, table_name, columns=columns, sep=",", null="\\N")
            conn.commit()

    print(f"✅ {len(df)} rows inserted in <1 second!")
