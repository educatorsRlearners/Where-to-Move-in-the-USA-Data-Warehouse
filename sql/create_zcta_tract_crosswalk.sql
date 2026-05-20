CREATE TABLE IF NOT EXISTS raw.zcta_tract_crosswalk (
    id            SERIAL PRIMARY KEY
    -- Geographic identifiers
    , ZCTA5       TEXT NOT NULL
    , STATE       TEXT
    , COUNTY      TEXT
    , TRACT       TEXT
    , GEOID       TEXT NOT NULL
    -- Population & housing overlap (ZCTA ∩ Tract)
    , POPPT       INTEGER
    , HUPT        INTEGER
    , AREAPT      DOUBLE PRECISION
    , AREALANDPT  DOUBLE PRECISION
    -- ZCTA totals
    , ZPOP        INTEGER
    , ZHU         INTEGER
    , ZAREA       DOUBLE PRECISION
    , ZAREALAND   DOUBLE PRECISION
    -- Tract totals
    , TRPOP       INTEGER
    , TRHU        INTEGER
    , TRAREA      DOUBLE PRECISION
    , TRAREALAND  DOUBLE PRECISION
    -- ZCTA share percentages
    , ZPOPPCT     DOUBLE PRECISION
    , ZHUPCT      DOUBLE PRECISION
    , ZAREAPCT    DOUBLE PRECISION
    , ZAREALANDPCT DOUBLE PRECISION
    -- Tract share percentages
    , TRPOPPCT    DOUBLE PRECISION
    , TRHUPCT     DOUBLE PRECISION
    , TRAREAPCT   DOUBLE PRECISION
    , TRAREALANDPCT DOUBLE PRECISION
    , UNIQUE (ZCTA5, GEOID)
);
