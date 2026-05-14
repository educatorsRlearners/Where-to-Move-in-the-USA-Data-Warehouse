CREATE TABLE IF NOT EXISTS raw.internet_speeds (
    id BIGSERIAL PRIMARY KEY
    , zip VARCHAR(10) NOT NULL
    , avg_download_mbps DOUBLE PRECISION
    , avg_upload_mbps DOUBLE PRECISION
    , avg_latency_ms DOUBLE PRECISION
    , tests INTEGER
    , devices INTEGER
    , UNIQUE(zip)
);
