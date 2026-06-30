-- ============================================
-- Migration 004
-- GIS Views for Dashboard & QGIS
-- ============================================


--------------------------------------------------
-- Groundwater Map (Latest Reading per Well)
--------------------------------------------------

CREATE OR REPLACE VIEW groundwater_map AS

SELECT DISTINCT ON (g.well_id)

    w.id,
    w.well_name,
    w.village,
    w.latitude,
    w.longitude,
    w.depth_m,

    g.time,
    g.water_level_m,

    w.geom

FROM groundwater_levels g

JOIN wells w
ON g.well_id = w.id

ORDER BY
    g.well_id,
    g.time DESC;



--------------------------------------------------
-- Pumping Map (Latest Reading per Well)
--------------------------------------------------

CREATE OR REPLACE VIEW pumping_map AS

SELECT DISTINCT ON (p.well_id)

    w.id,
    w.well_name,
    w.village,

    p.time,
    p.pumping_hours,

    w.geom

FROM pumping p

JOIN wells w
ON p.well_id = w.id

ORDER BY
    p.well_id,
    p.time DESC;



--------------------------------------------------
-- Rainfall View
--------------------------------------------------

CREATE OR REPLACE VIEW rainfall_map AS

SELECT

    station_name,

    time,

    rainfall_mm

FROM rainfall;



--------------------------------------------------
-- Weather View
--------------------------------------------------

CREATE OR REPLACE VIEW weather_map AS

SELECT

    station_name,

    time,

    temperature_c,

    humidity_pct

FROM weather;