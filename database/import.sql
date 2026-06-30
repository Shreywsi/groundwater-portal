\copy wells (
    id,
    well_name,
    village,
    latitude,
    longitude,
    depth_m,
    aquifer,
    status
)
FROM '/tmp/wells.csv'
DELIMITER ','
CSV HEADER;

\copy rainfall (
    time,
    station_name,
    rainfall_mm
)
FROM '/tmp/rainfall.csv'
DELIMITER ','
CSV HEADER;

\copy weather (
    time,
    station_name,
    temperature_c,
    humidity_pct
)
FROM '/tmp/weather.csv'
DELIMITER ','
CSV HEADER;

\copy groundwater_levels (
    time,
    well_id,
    water_level_m
)
FROM '/tmp/groundwater.csv'
DELIMITER ','
CSV HEADER;

\copy pumping (
    time,
    well_id,
    pumping_hours
)
FROM '/tmp/pumping.csv'
DELIMITER ','
CSV HEADER;