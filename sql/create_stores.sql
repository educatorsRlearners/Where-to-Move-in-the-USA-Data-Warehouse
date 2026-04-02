CREATE TABLE IF NOT EXISTS stores (
            id SERIAL PRIMARY Key
            , store_number INTEGER
            , store_name TEXT NOT NULL
            , street TEXT NOT NULL
            , city TEXT NOT NULL
            , state VARCHAR(2) NOT NULL
            , zip_code VARCHAR(10) NOT NULL
            , phone_number VARCHAR(20) NOT NULL
            , url TEXT NOT NULL
        )