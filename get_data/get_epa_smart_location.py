import os
import requests
import pandas as pd

# EPA Smart Location Database v3 (Jan 2021) — block group level, all US
# If this URL breaks, check: https://www.epa.gov/smartgrowth/smart-location-mapping
EPA_SLD_URL = (
    "https://edg.epa.gov/EPADataCommons/public/OA/"
    "EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv"
)

# Census 2010 ZCTA-to-Tract relationship file
# Maps 5-digit ZCTAs (≈ ZIP codes) to 11-digit census tract FIPS codes
ZCTA_TRACT_URL = (
    "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_tract_rel_10.txt"
)


def _download(url: str, dest: str) -> None:
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65_536):
                f.write(chunk)


def get_epa_sld_raw(cache_dir: str = "data/00.raw/epa_sld") -> pd.DataFrame:
    path = os.path.join(cache_dir, "epa_sld_v3.csv")
    if not os.path.exists(path):
        os.makedirs(cache_dir, exist_ok=True)
        _download(EPA_SLD_URL, path)
    return pd.read_csv(path, low_memory=False)


def get_zcta_tract_crosswalk(cache_dir: str = "data/00.raw/epa_sld") -> pd.DataFrame:
    path = os.path.join(cache_dir, "zcta_tract_rel_10.txt")
    if not os.path.exists(path):
        os.makedirs(cache_dir, exist_ok=True)
        _download(ZCTA_TRACT_URL, path)
    df = pd.read_csv(path, dtype=str)
    df.columns = df.columns.str.strip()
    return df
