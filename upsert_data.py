import pandas as pd
import psycopg2

from config import load_config
from typing import List, Optional


def upsert_dataframe_batch(
    df: pd.DataFrame,
    table_name: str,
    conflict_column: str,
    batch_size: int = 1000,
    columns: Optional[List[str]] = None,
    config_func=load_config,
) -> int:
    """
    Upserts a DataFrame into a Postgres table in batches of 1k by default. Returns the number of rows upserted.
    """
    if df.empty:
        print("DataFrame is empty.")
        return 0

    total_rows = 0
    conn = None

    try:
        config = config_func()
        with psycopg2.connect(**config) as conn:
            print(f"Connected. Processing {len(df)} rows in batches of {batch_size}...")

            if columns is None:
                columns = [col for col in df.columns if col != "id"]

            temp_df = df[columns].copy().replace("", pd.NA)
            if "store_number" in columns:
                temp_df["store_number"] = pd.to_numeric(
                    temp_df["store_number"], errors="coerce"
                ).fillna(pd.NA)

            rows = [
                tuple(None if pd.isna(value) else value for value in row)
                for row in temp_df.to_numpy()
            ]

            # Process in batches
            for i in range(0, len(rows), batch_size):
                batch = rows[i : i + batch_size]

                placeholders = ", ".join(["%s"] * len(columns))
                set_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns])

                sql = f"""
                    INSERT INTO {table_name} ({', '.join(columns)})
                    VALUES ({placeholders})
                    ON CONFLICT ({conflict_column}) DO UPDATE SET
                        {set_clause}
                """

                with conn.cursor() as cur:
                    cur.executemany(sql, batch)
                    conn.commit()

                batch_rows = len(batch)
                total_rows += batch_rows
                print(f"  Batch {i//batch_size + 1}: {batch_rows} rows")

            print(f"✅ Completed: {total_rows} total rows upserted")
            return total_rows

    except Exception as error:
        print(f"❌ Error: {error}")
        return 0
    finally:
        if conn:
            conn.close()
