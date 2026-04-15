BASE_URL = "https://locations.traderjoes.com"

# Default Values
BLANK = "Blank"
COMING_SOON = "Coming Soon"


# SQL
CREATE_STORES_SQL = "sql/create_stores.sql"
CREATE_INTERNET_SPEEDS_SQL = "sql/create_internet_speeds.sql"

# Table Names
STORES_TABLE = "stores"
INTERNET_SPEED_TABLE = "internet_speeds"

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
    "population",
    "county",
    "state",
    "wiredcount_2020",
    "fwcount_2020",
    "allprovidercount_2020",
    "wired25_3_2020",
    "wired100_3_2020",
    "all25_3_2020",
    "all100_3_2020",
    "testcount",
    "averagembps",
    "fastestaveragembps",
    "access_terrestrial_broadband",
    "lowest_priced_terrestrial_broadband",
    "wiredcount_2015",
    "fwcount_2015",
    "allprovidercount_2015",
    "wired25_3_2015",
    "wired100_3_2015",
    "all25_3_2015",
    "all100_3_1",
]

INTERNET_SPEED_FLOAT_COLUMNS = [
    "averagembps",
    "fastestaveragembps",
    "lowest_priced_terrestrial_broadband",
]

INTERNET_SPEED_INT_COLUMNS = [
    "population",
    "wiredcount_2020",
    "fwcount_2020",
    "allprovidercount_2020",
    "wired25_3_2020",
    "wired100_3_2020",
    "all25_3_2020",
    "all100_3_2020",
    "testcount",
    "wiredcount_2015",
    "fwcount_2015",
    "allprovidercount_2015",
    "wired25_3_2015",
    "wired100_3_2015",
    "all25_3_2015",
    "all100_3_1",
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
