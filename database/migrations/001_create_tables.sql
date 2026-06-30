-- ============================================
-- Water Management Portal
-- Migration 001
-- Users and Wells
-- ============================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ------------------------
-- Users
-- ------------------------

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL
        CHECK (role IN ('admin','crp','researcher')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------
-- Wells
-- ------------------------

CREATE TABLE IF NOT EXISTS wells (
    id SERIAL PRIMARY KEY,

    well_name VARCHAR(100) NOT NULL,

    village VARCHAR(100),

    latitude DOUBLE PRECISION NOT NULL,

    longitude DOUBLE PRECISION NOT NULL,

    depth_m DOUBLE PRECISION,

    status VARCHAR(20)
        DEFAULT 'active'
        CHECK (status IN ('active','inactive')),

    geom geometry(Point,4326)
);

-- Fill geometry from latitude/longitude
UPDATE wells
SET geom = ST_SetSRID(
    ST_MakePoint(longitude, latitude),
    4326
)
WHERE geom IS NULL;

CREATE INDEX IF NOT EXISTS idx_wells_geom
ON wells
USING GIST (geom);