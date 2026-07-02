-- ============================================
-- Migration 004
-- Water Quality (TDS + Salinity)
-- ============================================

CREATE TABLE IF NOT EXISTS water_quality (

    time TIMESTAMPTZ NOT NULL,

    well_id INTEGER NOT NULL
        REFERENCES wells(id)
        ON DELETE CASCADE,

    tds_ppm DOUBLE PRECISION,

    salinity_ppt DOUBLE PRECISION
);

SELECT create_hypertable(
    'water_quality',
    'time',
    if_not_exists => TRUE
);


--------------------------------------------------
-- Water Quality Map (Latest Reading per Well)
--------------------------------------------------

CREATE OR REPLACE VIEW water_quality_map AS

SELECT DISTINCT ON (q.well_id)

    w.id,
    w.well_name,
    w.village,

    q.time,
    q.tds_ppm,
    q.salinity_ppt,

    w.geom

FROM water_quality q

JOIN wells w
ON q.well_id = w.id

ORDER BY
    q.well_id,
    q.time DESC;