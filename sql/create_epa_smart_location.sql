CREATE TABLE IF NOT EXISTS raw.epa_smart_location (
    id SERIAL PRIMARY KEY
    , zip VARCHAR(10) NOT NULL
    , nat_walkability_index DOUBLE PRECISION
    , transit_route_density DOUBLE PRECISION
    , transit_stop_distance DOUBLE PRECISION
    , transit_freq_index DOUBLE PRECISION
    , population INTEGER
    , UNIQUE(zip)
);
