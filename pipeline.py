from constants import (
    CREATE_STORES_SQL,
    CREATE_INTERNET_SPEEDS_SQL,
    CREATE_EPA_SLD_SQL,
    CREATE_ZCTA_TRACT_SQL,
    STORES_TABLE,
    INTERNET_SPEED_TABLE,
    EPA_SLD_TABLE,
    ZCTA_TRACT_TABLE,
    STORE_COLUMNS,
    INTERNET_SPEED_COLUMNS,
)
from get_data.get_epa_smart_location import get_epa_sld_raw, get_zcta_tract_crosswalk
from get_data.get_internet_speeds import get_internet_speeds_df
from get_data.get_trader_joes import create_dataframe
from load_data import load_df


def run(pipes=None):
    if pipes is None or len(pipes) == 0:
        print("Please select the pipes you wish to run.")
        return

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
            get_epa_sld_raw(),
            EPA_SLD_TABLE,
            conflict_column="GEOID10",
            sql_file=CREATE_EPA_SLD_SQL,
        )
        load_df(
            get_zcta_tract_crosswalk(),
            ZCTA_TRACT_TABLE,
            conflict_column="ZCTA5, GEOID",
            sql_file=CREATE_ZCTA_TRACT_SQL,
        )


if __name__ == "__main__":
    run()
