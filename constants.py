BASE_URL = "https://locations.traderjoes.com"

# Default Values
BLANK = "Blank"
COMING_SOON = "Coming Soon"


# SQL
CREATE_STORES_SQL = "sql/create_stores.sql"
CREATE_INTERNET_SPEEDS_SQL = "sql/create_internet_speeds.sql"
CREATE_EPA_SLD_SQL = "sql/create_epa_sld.sql"
CREATE_ZCTA_TRACT_SQL = "sql/create_zcta_tract_crosswalk.sql"

# Table Names
STORES_TABLE = "raw.stores"
INTERNET_SPEED_TABLE = "raw.internet_speeds"
EPA_SLD_TABLE = "raw.epa_sld"
ZCTA_TRACT_TABLE = "raw.zcta_tract_crosswalk"

# Column names
STORE_COLUMNS = [
    "store_number",
    "store_name",
    "street",
    "city",
    "state",
    "zip_code",
    "phone_number",
    "url",
]


INTERNET_SPEED_COLUMNS = [
    "zip",
    "avg_download_mbps",
    "avg_upload_mbps",
    "avg_latency_ms",
    "tests",
    "devices",
]


STATES_TO_OMIT = [
    "AA",
    "AE",
    "AK",
    "AP",
    "AS",
    "FM",
    "GU",
    "HI",
    "MH",
    "MP",
    "PR",
    "PW",
    "VI",
]
