from functools import partial

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
from config import load_config
from get_data.get_epa_smart_location import get_epa_sld_raw, get_zcta_tract_crosswalk
from get_data.get_internet_speeds import get_internet_speeds_df
from get_data.get_trader_joes import create_dataframe
from load_data import load_df

BRANCH_SECTIONS = {
    "production": "postgresql",
    "dev": "dev",
}


def run(pipes=None, branch="production"):
    if pipes is None or len(pipes) == 0:
        print("Please select the pipes you wish to run.")
        return

    section = BRANCH_SECTIONS.get(branch)
    if section is None:
        print(f"Unknown branch '{branch}'. Choose: {list(BRANCH_SECTIONS.keys())}")
        return

    config_func = partial(load_config, section=section)
    print(f"=== Targeting branch: {branch} ===")

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
            config_func=config_func,
        )

    if "internet_speeds" in pipes:
        print("\n=== Loading internet speeds ===")
        load_df(
            get_internet_speeds_df(),
            INTERNET_SPEED_TABLE,
            conflict_column="zip",
            sql_file=CREATE_INTERNET_SPEEDS_SQL,
            columns=INTERNET_SPEED_COLUMNS,
            config_func=config_func,
        )

    if "epa_smart_location" in pipes:
        print(
            "\n=== Loading EPA Smart Location data (downloads ~100MB on first run) ==="
        )
        load_df(
            get_epa_sld_raw(),
            EPA_SLD_TABLE,
            conflict_column="STATEFP, COUNTYFP, TRACTCE, BLKGRPCE",
            sql_file=CREATE_EPA_SLD_SQL,
            config_func=config_func,
        )
        load_df(
            get_zcta_tract_crosswalk(),
            ZCTA_TRACT_TABLE,
            conflict_column="ZCTA5, GEOID",
            sql_file=CREATE_ZCTA_TRACT_SQL,
            config_func=config_func,
        )


if __name__ == "__main__":
    run(pipes=["epa_smart_location"], branch="dev")
