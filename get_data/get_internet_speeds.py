import pandas as pd


def get_internet_speeds_df() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/BroadbandNow/Open-Data/master/broadband_data_opendatachallenge.csv"
    df = pd.read_csv(url, encoding="latin-1", dtype={"Zip": str})

    return df


if __name__ == "__main__":
    df = get_internet_speeds_df()
