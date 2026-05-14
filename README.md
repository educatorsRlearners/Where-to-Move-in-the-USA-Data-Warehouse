# Where to Move in the USA — Data Warehouse

ETL pipeline that builds a PostgreSQL database of location quality metrics across the continental US. Used as the data warehouse for a "where should I live?" dashboard.

## Data Sources

| Table | Source | Granularity | What it measures |
|---|---|---|---|
| `raw.stores` | Trader Joe's website (scraped) | Store | Presence of a Trader Joe's |
| `raw.internet_speeds` | [BroadbandNow Open Data](https://github.com/BroadbandNow/Open-Data) | ZIP code | Average download speeds |
| `raw.epa_smart_location` | [EPA Smart Location Database v3](https://www.epa.gov/smartgrowth/smart-location-mapping) | ZIP code | Walkability and transit access |

All three tables share ZIP code as a join key, making them joinable in a downstream analytics layer.

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

This will:
1. Create the `raw` schema and all tables if they don't exist
2. Scrape all Trader Joe's store locations (~500 pages, takes a few minutes)
3. Download and load internet speed data
4. Download and load EPA walkability/transit data (~100MB download on first run; cached after that)

## Project Structure

```
pipeline.py          # Entrypoint — runs the full ETL in order
create_tables.py     # Creates tables in Postgres
upsert_data.py       # Generic batch upsert for any table
insert_data.py       # Fast bulk insert using COPY
config.py            # Loads database.ini
constants.py         # Table names, column lists, SQL file paths
get_data/
    get_trader_joes.py        # Scrapes store locations
    get_internet_speeds.py    # Downloads broadband data
    get_epa_smart_location.py # Downloads EPA SLD, crosswalks to ZIP level
sql/
    create_stores.sql
    create_internet_speeds.sql
    create_epa_smart_location.sql
```
