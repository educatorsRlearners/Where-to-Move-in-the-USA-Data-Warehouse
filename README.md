# Where to Move in the USA — Data Warehouse

ETL pipeline that builds a PostgreSQL data warehouse of location quality metrics across the continental US. Serves as the raw layer for a downstream [dbt transformation and visualization project](https://github.com/educatorsRlearners/dbt_where_to_live).

## Architecture

```
[Trader Joe's website] ──scrape──┐
[Ookla Speedtest Open Data] ─────┤──► pipeline.py ──► PostgreSQL (raw schema)
[EPA Smart Location Database] ───┘                         │
[US Census ZCTA/Tract crosswalk] ────────────────────────►─┤
                                                           ▼
                                              dbt_where_to_live (transforms + viz)
```

The four raw tables will use US zip code as a join key, making them composable in the downstream analytics layer via dbt transformations. 

## Data Sources

| Table | Source | Granularity | What it measures |
|---|---|---|---|
| `raw.stores` | Trader Joe's website (scraped) | Store | Presence of a Trader Joe's |
| `raw.internet_speeds` | [Ookla Speedtest Open Data](https://github.com/teamookla/ookla-open-data) (Q1 2026, fixed broadband) | ZIP code | Weighted-average download/upload speeds and latency |
| `raw.epa_sld` | [EPA Smart Location Database v3](https://www.epa.gov/smartgrowth/smart-location-mapping) (Jan 2021) | Census block group | National Walkability Index and transit access scores |
| `raw.zcta_tract_crosswalk` | US Census Bureau 2010 ZCTA-to-Tract crosswalk | ZCTA / tract | Population-weighted mapping from census tracts to ZIP codes |

### Engineering notes

**Internet speeds** — Ookla publishes speed test results as quadkey tiles. Each tile is assigned to the nearest ZIP centroid using a KD-tree spatial join, then speeds are aggregated to ZIP level using test-count-weighted averages.

**EPA walkability** — The SLD is published at census block group level and loaded as-is into `raw.epa_sld`. A 2010 Census ZCTA-to-Tract crosswalk is loaded into `raw.zcta_tract_crosswalk` and used by the downstream dbt layer to roll block group scores up to ZIP level via population-weighted averages.

**Idempotent loading** — `load_data.py` detects whether a table already exists. On the first run it uses PostgreSQL `COPY` for fast bulk insertion. On subsequent runs it uses `INSERT ... ON CONFLICT DO UPDATE` (upsert), so the pipeline is safe to re-run.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A running PostgreSQL instance ([Neon](https://neon.tech) works well as a free hosted option)

## Setup

**1. Install dependencies**
```bash
uv sync
```

**2. Configure your database connection**

Create a `database.ini` file in the project root:
```ini
[postgresql]
host=<your_host>
database=<your_database>
user=<your_user>
password=<your_password>
```

`database.ini` is gitignored to avoid committing sensitive credentials. 

## Running the pipeline

To run the full pipeline, simply execute `pipeline.py` and speifiy which pipes to run and in which database branch like this:  

### Running individual/multiples pipes to a specified branch
```python
from pipeline import run

run(pipes=["internet_speeds"], branch="production")
run(pipes=["epa_smart_location"], branch="dev")
run(pipes=["stores", "internet_speeds"], branch="staging")
```

Note: if the branch or pipe doesn't exist, you will receive a notification. 

## Project Structure

```
pipeline.py          # Entrypoint — orchestrates which pipes run
load_data.py         # Smart load: COPY on first run, upsert on subsequent runs
create_tables.py     # Creates raw schema and tables in Postgres
insert_data.py       # Fast bulk insert via PostgreSQL COPY
upsert_data.py       # Batch upsert via INSERT ... ON CONFLICT
config.py            # Reads database.ini connection parameters
constants.py         # Table names, column lists, SQL file paths
get_data/
    get_trader_joes.py        # Scrapes store locations from Trader Joe's website
    get_internet_speeds.py    # Downloads Ookla tiles; KD-tree join to ZIP centroids
    get_epa_smart_location.py # Downloads EPA SLD and ZCTA-to-Tract crosswalk
sql/
    create_stores.sql
    create_internet_speeds.sql
    create_epa_sld.sql
    create_zcta_tract_crosswalk.sql
data/                # Local cache for downloaded files and CSVs (gitignored)
```
