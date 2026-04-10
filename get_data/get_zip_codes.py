import pandas as pd
import zipcodes


def import_us_zip_codes() -> pd.DataFrame:
    # Get all ZIP records
    all_zips = zipcodes.list_all()

    # Create Dataframe
    df = pd.DataFrame(all_zips)

    # Filter for just US ZipCodes
    df_US = df[df["country"] == "US"]

    return df_US


if __name__ == "main":
    df = import_us_zip_codes()
