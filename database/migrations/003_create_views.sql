-- ============================================
-- Migration 003
-- GIS Views
-- ============================================


------------------------------------------------
-- Latest groundwater level for each well
------------------------------------------------

CREATE OR REPLACE VIEW groundwater_latest AS

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



------------------------------------------------
-- Latest pumping for each well
------------------------------------------------

CREATE OR REPLACE VIEW pumping_latest AS

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