import pandas as pd
import zipcodes
from constants import STATES_TO_OMIT


def import_us_zip_codes() -> pd.DataFrame:
    # Get all ZIP records
    all_zips = zipcodes.list_all()

    # Create Dataframe
    df = pd.DataFrame(all_zips)

    # Filter for just US Zip Codes
    df_US = df[df["country"] == "US"]

    # Keep only continental US Zip Codes
    continental_us = df_US[~df_US["state"].isin(STATES_TO_OMIT)]

    return continental_us


if __name__ == "main":
    df = import_us_zip_codes()
