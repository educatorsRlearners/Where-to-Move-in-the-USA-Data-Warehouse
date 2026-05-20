CREATE TABLE IF NOT EXISTS raw.zcta_tract_crosswalk (
    id            SERIAL PRIMARY KEY
    -- Geographic identifiers
    , ZCTA5       TEXT
    , STATE       TEXT
    , COUNTY      TEXT
    , TRACT       TEXT
    , GEOID       TEXT
    -- Population & housing overlap (ZCTA ∩ Tract)
    , POPPT       DOUBLE PRECISION
    , HUPT        DOUBLE PRECISION
    , AREAPT      DOUBLE PRECISION
    , AREALANDPT  DOUBLE PRECISION
    -- ZCTA totals
    , ZPOP        DOUBLE PRECISION
    , ZHU         DOUBLE PRECISION
    , ZAREA       DOUBLE PRECISION
    , ZAREALAND   DOUBLE PRECISION
    -- Tract totals
    , TRPOP       DOUBLE PRECISION
    , TRHU        DOUBLE PRECISION
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
