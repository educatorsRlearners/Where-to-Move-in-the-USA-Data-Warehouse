# Where to Move in the USA — Data Warehouse

ETL pipeline that builds a PostgreSQL data warehouse of location quality metrics across the continental US. Serves as the raw layer for a downstream [dbt transformation and visualization project](https://github.com/educatorsRlearners/dbt_where_to_live).

## Architecture

```
[Trader Joe's website] ──scrape──┐
[Ookla Speedtest Open Data] ─────┤──► pipeline.py ──► PostgreSQL (raw schema)
[EPA Smart Location Database] ───┘                         │
                                                           ▼
                                              dbt_where_to_live (transforms + viz)
```

Three source tables share ZIP code as a join key, making them composable in the downstream analytics layer.

## Data Sources

| Table | Source | Granularity | What it measures |
|---|---|---|---|
| `raw.stores` | Trader Joe's website (scraped) | Store | Presence of a Trader Joe's |
| `raw.internet_speeds` | [Ookla Speedtest Open Data](https://github.com/teamookla/ookla-open-data) (Q1 2026, fixed broadband) | ZIP code | Weighted-average download/upload speeds and latency |
| `raw.epa_smart_location` | [EPA Smart Location Database v3](https://www.epa.gov/smartgrowth/smart-location-mapping) (Jan 2021) | ZIP code | National Walkability Index and transit access scores |

### Engineering notes

**Internet speeds** — Ookla publishes speed test results as quadkey tiles. Each tile is assigned to the nearest ZIP centroid using a KD-tree spatial join, then speeds are aggregated to ZIP level using test-count-weighted averages.

**EPA walkability** — The SLD is published at census block group level. A 2010 Census ZCTA-to-Tract crosswalk is used to roll block group scores up to ZIP level via population-weighted averages.

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

`database.ini` is gitignored and should never be committed.

## Running the pipeline

```bash
uv run python pipeline.py
```

This loads internet speeds and EPA walkability data (~100MB download on first run for each source; both are cached locally after that). On subsequent runs only changed rows are upserted.

### Loading Trader Joe's store data (separate step)

The stores pipeline is split into two phases, both implemented in `get_data/get_trader_joes.py`. First, scrape the URL list:

```python
from get_data.get_trader_joes import write_store_urls_to_csv

write_store_urls_to_csv()  # scrapes ~500 pages, writes data/store_urls.csv
```

Then run the stores pipe, which reads that URL list, visits each store page to extract details, and loads the results into Postgres:

```python
from pipeline import run
run(pipes=["stores"])
```

### Running all pipes
`pipeline.py` runs all pipes by default.
```python
from pipeline import run
run() 
```

### Running individual/multiples pipes
To run individual pipes, pass a list of pipe names like so: 
```python
from pipeline import run

run(pipes=["internet_speeds"])
run(pipes=["epa_smart_location"])
run(pipes=["stores", "internet_speeds"])
```



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
    get_epa_smart_location.py # Downloads EPA SLD; crosswalks block groups to ZIP
sql/
    create_stores.sql
    create_internet_speeds.sql
    create_epa_smart_location.sql
data/                # Local cache for downloaded files and CSVs (gitignored)
```
