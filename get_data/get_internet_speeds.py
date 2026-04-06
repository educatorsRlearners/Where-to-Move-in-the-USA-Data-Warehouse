import pandas as pd
from constants import (
    INTERNET_SPEED_COLUMNS,
    INTERNET_SPEED_FLOAT_COLUMNS,
    INTERNET_SPEED_INT_COLUMNS,
)


def get_internet_speeds_df() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/BroadbandNow/Open-Data/master/broadband_data_opendatachallenge.csv"

    df = pd.read_csv(url, encoding="latin-1", dtype={"Zip": str})

    df.columns = INTERNET_SPEED_COLUMNS

    df[INTERNET_SPEED_INT_COLUMNS] = (
        df[INTERNET_SPEED_INT_COLUMNS]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Int64")
    )

    df[INTERNET_SPEED_FLOAT_COLUMNS] = df[INTERNET_SPEED_FLOAT_COLUMNS].apply(
        pd.to_numeric, errors="coerce"
    )

    return df


if __name__ == "__main__":
    df = get_internet_speeds_df()
