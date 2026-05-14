BASE_URL = "https://locations.traderjoes.com"

# Default Values
BLANK = "Blank"
COMING_SOON = "Coming Soon"


# SQL
CREATE_STORES_SQL = "sql/create_stores.sql"
CREATE_INTERNET_SPEEDS_SQL = "sql/create_internet_speeds.sql"
CREATE_EPA_SMART_LOCATION_SQL = "sql/create_epa_smart_location.sql"

# Table Names
STORES_TABLE = "raw.stores"
INTERNET_SPEED_TABLE = "raw.internet_speeds"
EPA_SMART_LOCATION_TABLE = "raw.epa_smart_location"

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

EPA_SMART_LOCATION_COLUMNS = [
    "zip",
    "nat_walkability_index",
    "transit_route_density",
    "transit_stop_distance",
    "transit_freq_index",
    "population",
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
