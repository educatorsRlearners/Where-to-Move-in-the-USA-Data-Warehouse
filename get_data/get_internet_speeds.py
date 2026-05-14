import os

import numpy as np
import pandas as pd
import requests
from scipy.spatial import cKDTree

from constants import STATES_TO_OMIT

# Ookla Speedtest Open Data — fixed broadband, Q1 2026
# Full dataset listing: https://github.com/teamookla/ookla-open-data
OOKLA_URL = (
    "https://ookla-open-data.s3.amazonaws.com/parquet/performance/"
    "type=fixed/year=2026/quarter=1/2026-01-01_performance_fixed_tiles.parquet"
)

# Continental US bounding box
_LAT_MIN, _LAT_MAX = 24.0, 50.0
_LON_MIN, _LON_MAX = -125.0, -66.0

_PARQUET_COLS = ["tile_x", "tile_y", "avg_d_kbps", "avg_u_kbps", "avg_lat_ms", "tests", "devices"]


def _download(url: str, dest: str) -> None:
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65_536):
                f.write(chunk)


def _load_zip_centroids() -> pd.DataFrame:
    import zipcodes
    df = pd.DataFrame(zipcodes.list_all())
    df = df[(df["country"] == "US") & (~df["state"].isin(STATES_TO_OMIT))]
    df = df[["zip_code", "lat", "long"]].dropna().reset_index(drop=True)
    df[["lat", "long"]] = df[["lat", "long"]].astype(float)
    return df


def get_internet_speeds_df(cache_dir: str = "data/00.raw/ookla") -> pd.DataFrame:
    """
    Returns ZIP-level broadband speeds from Ookla Speedtest Open Data (Q1 2026).

    tile_x/tile_y are pre-computed tile centroids (lon/lat). Each tile is assigned
    to the nearest ZIP centroid via KD-tree. Speeds are aggregated using test-count
    weights and converted from kbps to Mbps.

    Columns returned:
      zip               — 5-digit ZIP code
      avg_download_mbps — test-weighted average download speed (Mbps)
      avg_upload_mbps   — test-weighted average upload speed (Mbps)
      avg_latency_ms    — test-weighted average latency (ms)
      tests             — total speed tests in the ZIP
      devices           — total unique devices in the ZIP
    """
    path = os.path.join(cache_dir, "ookla_fixed_q1_2026.parquet")
    if not os.path.exists(path):
        os.makedirs(cache_dir, exist_ok=True)
        _download(OOKLA_URL, path)

    tiles = pd.read_parquet(path, columns=_PARQUET_COLS)

    # tile_x = longitude, tile_y = latitude
    tiles = tiles[
        tiles["tile_y"].between(_LAT_MIN, _LAT_MAX)
        & tiles["tile_x"].between(_LON_MIN, _LON_MAX)
    ].copy()

    zip_df = _load_zip_centroids()

    tree = cKDTree(zip_df[["lat", "long"]].values)
    _, idx = tree.query(tiles[["tile_y", "tile_x"]].values)
    tiles["zip"] = zip_df.loc[idx, "zip_code"].values

    def wavg(g: pd.DataFrame, col: str) -> float:
        w = g["tests"]
        total = w.sum()
        return (g[col] * w).sum() / total if total > 0 else g[col].mean()

    result = (
        tiles.groupby("zip")
        .apply(
            lambda g: pd.Series({
                "avg_download_mbps": wavg(g, "avg_d_kbps") / 1000,
                "avg_upload_mbps": wavg(g, "avg_u_kbps") / 1000,
                "avg_latency_ms": wavg(g, "avg_lat_ms"),
                "tests": int(g["tests"].sum()),
                "devices": int(g["devices"].sum()),
            })
        )
        .reset_index()
    )

    return result


if __name__ == "__main__":
    df = get_internet_speeds_df()
