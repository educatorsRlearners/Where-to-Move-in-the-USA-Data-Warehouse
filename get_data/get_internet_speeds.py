import pandas as pd


def get_internet_speeds_df() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/BroadbandNow/Open-Data/master/broadband_data_opendatachallenge.csv"
    df = pd.read_csv(url, encoding="latin-1", dtype={"Zip": str})

    df = df.rename(
        columns={
            "Zip": "zip",
            "Population": "population",
            "County": "county",
            "State": "state",
            "WiredCount_2020": "wiredcount_2020",
            "Fwcount_2020": "fwcount_2020",
            "AllProviderCount_2020": "allprovidercount_2020",
            "Wired25_3_2020": "wired25_3_2020",
            "Wired100_3_2020": "wired100_3_2020",
            "All25_3_2020": "all25_3_2020",
            "All100_3": "all100_3_2020",
            "TestCount": "testcount",
            "AverageMbps": "averagembps",
            "FastestAverageMbps": "fastestaveragembps",
            "%Access to Terrestrial Broadband": "access_terrestrial_broadband",
            "Lowest Priced Terrestrial Broadband Plan": "lowest_priced_terrestrial_broadband",
            "WiredCount_2015": "wiredcount_2015",
            "Fwcount_2015": "fwcount_2015",
            "AllProviderCount_2015": "allprovidercount_2015",
            "Wired25_3_2015": "wired25_3_2015",
            "Wired100_3_2015": "wired100_3_2015",
            "All25_3_2015": "all25_3_2015",
            "All100_3.1": "all100_3_1",
        }
    )

    integer_columns = [
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

    float_columns = [
        "averagembps",
        "fastestaveragembps",
        "lowest_priced_terrestrial_broadband",
    ]

    df[integer_columns] = (
        df[integer_columns].apply(pd.to_numeric, errors="coerce").astype("Int64")
    )
    df[float_columns] = df[float_columns].apply(pd.to_numeric, errors="coerce")
    df["zip"] = df["zip"].astype(str)

    return df


if __name__ == "__main__":
    df = get_internet_speeds_df()
