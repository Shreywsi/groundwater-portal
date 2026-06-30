CREATE TABLE IF NOT EXISTS weather (

    time TIMESTAMPTZ NOT NULL,

    station_name VARCHAR(100),

    temperature_c DOUBLE PRECISION,

    humidity_pct DOUBLE PRECISION
);

SELECT create_hypertable(
    'weather',
    'time',
    if_not_exists => TRUE
);

CREATE TABLE IF NOT EXISTS pumping (

    time TIMESTAMPTZ NOT NULL,

    well_id INTEGER
        REFERENCES wells(id)
        ON DELETE CASCADE,

    pumping_hours DOUBLE PRECISION
);

SELECT create_hypertable(
    'pumping',
    'time',
    if_not_exists => TRUE
);