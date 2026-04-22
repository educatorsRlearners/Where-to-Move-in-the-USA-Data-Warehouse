import glob
import pandas as pd
import os


def get_public_transit_data():
    folder_path = "data/00.raw/transit"

    files = glob.glob(os.path.join(folder_path, "*.csv"))

    data_frames = [pd.read_csv(file) for file in files]

    df = pd.concat(data_frames, ignore_index=True)

    # Select only object/string columns
    string_cols = df.select_dtypes(include=["object"]).columns

    # Vectorized strip only on those columns
    df[string_cols] = df[string_cols].apply(lambda col: col.str.strip('"'))

    return df


if __name__ == "__main__":
    df = get_public_transit_data()
