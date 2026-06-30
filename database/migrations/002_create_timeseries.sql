-- ============================================
-- Migration 002
-- Rainfall & Groundwater Levels
-- ============================================

CREATE TABLE rainfall (

    time TIMESTAMPTZ NOT NULL,

    station_name VARCHAR(100) NOT NULL,

    rainfall_mm DOUBLE PRECISION NOT NULL
);


CREATE TABLE groundwater_levels (

    time TIMESTAMPTZ NOT NULL,

    well_id INTEGER NOT NULL
        REFERENCES wells(id)
        ON DELETE CASCADE,

    water_level_m DOUBLE PRECISION NOT NULL
);


-- Convert to hypertables

SELECT create_hypertable(
    'rainfall',
    'time',
    if_not_exists => TRUE
);

SELECT create_hypertable(
    'groundwater_levels',
    'time',
    if_not_exists => TRUE
);