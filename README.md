CREATE TABLE IF NOT EXISTS public.citybik_log (
    id TEXT not NULL,
    updated_at TIMESTAMPTZ,
    station_name TEXT NOT NULL,
    free_bikes INT NOT NULL,
    empty_slots INT NOT NULL,
    address TEXT null,
    distance_to_supersim FLOAT NULL,
    renting INT NOT NULL,
    "returning" INT NOT NULL,
    has_ebikes BOOLEAN NOT NULL,
    ebikes INT NOT NULL,
    normal_bikes INT NOT NULL,
    payment_terminal TEXT null,
    PRIMARY KEY (id, updated_at)
);
