import os
import requests
import pandas as pd

# EPA Smart Location Database v3 (Jan 2021) — block group level, all US
# Direct CSV; no geospatial libraries required.
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

# Columns needed from the SLD CSV.
# NOTE: GEOID10 has float precision loss in the CSV, so we reconstruct
# the tract FIPS from STATEFP + COUNTYFP + TRACTCE instead.
SLD_USECOLS = ["STATEFP", "COUNTYFP", "TRACTCE", "TotPop", "NatWalkInd", "D4A", "D4C", "D4D"]


def _download(url: str, dest: str) -> None:
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65_536):
                f.write(chunk)


def _load_sld(cache_dir: str) -> pd.DataFrame:
    path = os.path.join(cache_dir, "epa_sld_v3.csv")
    if not os.path.exists(path):
        os.makedirs(cache_dir, exist_ok=True)
        _download(EPA_SLD_URL, path)

    df = pd.read_csv(
        path,
        usecols=SLD_USECOLS,
        dtype={"STATEFP": str, "COUNTYFP": str, "TRACTCE": str},
        low_memory=False,
    )
    return df


def _load_crosswalk(cache_dir: str) -> pd.DataFrame:
    path = os.path.join(cache_dir, "zcta_tract_rel_10.txt")
    if not os.path.exists(path):
        os.makedirs(cache_dir, exist_ok=True)
        _download(ZCTA_TRACT_URL, path)

    df = pd.read_csv(
        path,
        usecols=["ZCTA5", "GEOID"],
        dtype={"ZCTA5": str, "GEOID": str},
    )
    df["ZCTA5"] = df["ZCTA5"].str.zfill(5)
    df["GEOID"] = df["GEOID"].str.zfill(11)
    return df.rename(columns={"ZCTA5": "zip", "GEOID": "tract_fips"})


def _weighted_mean(group: pd.DataFrame, col: str) -> float:
    weights = group["TotPop"].fillna(0)
    total = weights.sum()
    if total == 0:
        return group[col].mean()
    return (group[col].fillna(0) * weights).sum() / total


def get_epa_smart_location(cache_dir: str = "data/00.raw/epa_sld") -> pd.DataFrame:
    """
    Returns a ZIP-level DataFrame with EPA walkability and transit scores.

    Block group scores are aggregated to ZCTA (≈ ZIP code) using
    population-weighted averages via the 2010 Census ZCTA-to-Tract crosswalk.

    Columns returned:
      zip                    — 5-digit ZIP / ZCTA code
      nat_walkability_index  — National Walkability Index (1–20, higher = better)
      transit_route_density  — D4A: transit routes per sq mile within 0.25 mi
      transit_stop_distance  — D4C: distance to nearest transit stop (meters, lower = better)
      transit_freq_index     — D4D: aggregate transit frequency index
      population             — total population (sum of block group populations)
    """
    sld = _load_sld(cache_dir)
    crosswalk = _load_crosswalk(cache_dir)

    # Reconstruct 11-digit tract FIPS from individual components.
    # zero-pad: state=2, county=3, tract=6
    sld["tract_fips"] = (
        sld["STATEFP"].str.zfill(2)
        + sld["COUNTYFP"].str.zfill(3)
        + sld["TRACTCE"].str.zfill(6)
    )

    merged = sld.merge(crosswalk, on="tract_fips", how="inner")

    score_cols = [c for c in ["NatWalkInd", "D4A", "D4C", "D4D"] if c in merged.columns]

    result = (
        merged.groupby("zip")
        .apply(
            lambda g: pd.Series(
                {
                    **{col: _weighted_mean(g, col) for col in score_cols},
                    "population": g["TotPop"].sum(),
                }
            )
        )
        .reset_index()
        .rename(
            columns={
                "NatWalkInd": "nat_walkability_index",
                "D4A": "transit_route_density",
                "D4C": "transit_stop_distance",
                "D4D": "transit_freq_index",
            }
        )
    )

    return result


if __name__ == "__main__":
    df = get_epa_smart_location()
