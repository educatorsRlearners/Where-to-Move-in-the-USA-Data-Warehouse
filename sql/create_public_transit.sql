CREATE TABLE IF NOT EXISTS raw.public_transit (
            id SERIAL PRIMARY Key
            , place TEXT NOT NULL
            , name TEXT NOT NULL
            , blkgrps DOUBLE PRECISION
            , population DOUBLE PRECISION
            , households DOUBLE PRECISION
            , alltransit_performance_score DOUBLE PRECISION
        )