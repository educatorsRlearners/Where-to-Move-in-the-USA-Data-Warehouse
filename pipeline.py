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
from get_data.get_epa_smart_location import get_epa_smart_location
from get_data.get_internet_speeds import get_internet_speeds_df
from get_data.get_trader_joes import create_dataframe
from load_data import load_df

ALL_PIPES = {"stores", "internet_speeds", "epa_smart_location"}


def run(pipes=None):
    if pipes is None:
        pipes = ALL_PIPES

    if "stores" in pipes:
        print(
            "=== Loading Trader Joe's stores (scrapes ~500 pages, takes a few minutes) ==="
        )
        load_df(
            create_dataframe(),
            STORES_TABLE,
            conflict_column="store_number",
            sql_file=CREATE_STORES_SQL,
            columns=STORE_COLUMNS,
        )

    if "internet_speeds" in pipes:
        print("\n=== Loading internet speeds ===")
        load_df(
            get_internet_speeds_df(),
            INTERNET_SPEED_TABLE,
            conflict_column="zip",
            sql_file=CREATE_INTERNET_SPEEDS_SQL,
            columns=INTERNET_SPEED_COLUMNS,
        )

    if "epa_smart_location" in pipes:
        print(
            "\n=== Loading EPA Smart Location data (downloads ~100MB on first run) ==="
        )
        load_df(
            get_epa_smart_location(),
            EPA_SMART_LOCATION_TABLE,
            conflict_column="zip",
            sql_file=CREATE_EPA_SMART_LOCATION_SQL,
            columns=EPA_SMART_LOCATION_COLUMNS,
        )


if __name__ == "__main__":
    run(pipes=["internet_speeds", "epa_smart_location"])
