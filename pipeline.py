from constants import (
    CREATE_STORES_SQL,
    CREATE_INTERNET_SPEEDS_SQL,
    CREATE_EPA_SMART_LOCATION_SQL,
    STORES_TABLE,
    INTERNET_SPEED_TABLE,
    EPA_SMART_LOCATION_TABLE,
    STORE_COLUMNS,
    INTERNET_SPEED_COLUMNS,
    EPA_SMART_LOCATION_COLUMNS,
)
from create_tables import create_tables
from get_data.get_epa_smart_location import get_epa_smart_location
from get_data.get_internet_speeds import get_internet_speeds_df
from get_data.get_trader_joes import create_dataframe
from upsert_data import upsert_dataframe_batch


def run():
    print("=== Creating tables ===")
    for sql_file in [CREATE_STORES_SQL, CREATE_INTERNET_SPEEDS_SQL, CREATE_EPA_SMART_LOCATION_SQL]:
        create_tables(command=open(sql_file).read())

    print("\n=== Loading Trader Joe's stores (scrapes ~500 pages, takes a few minutes) ===")
    stores_df = create_dataframe()
    upsert_dataframe_batch(stores_df, STORES_TABLE, conflict_column="store_number", columns=STORE_COLUMNS)

    print("\n=== Loading internet speeds ===")
    speeds_df = get_internet_speeds_df()
    upsert_dataframe_batch(speeds_df, INTERNET_SPEED_TABLE, conflict_column="zip", columns=INTERNET_SPEED_COLUMNS)

    print("\n=== Loading EPA Smart Location data (downloads ~100MB on first run) ===")
    epa_df = get_epa_smart_location()
    upsert_dataframe_batch(epa_df, EPA_SMART_LOCATION_TABLE, conflict_column="zip", columns=EPA_SMART_LOCATION_COLUMNS)


if __name__ == "__main__":
    run()
