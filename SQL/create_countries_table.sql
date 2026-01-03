-- Script to add countries table

CREATE TABLE IF NOT EXISTS countries (
    country_id BIGSERIAL PRIMARY KEY,
    sigle VARCHAR(3) NOT NULL UNIQUE,
    country_name VARCHAR(100) NOT NULL,
    country_flag TEXT
);

CREATE INDEX IF NOT EXISTS idx_countries_sigle ON countries(sigle);
CREATE INDEX IF NOT EXISTS idx_countries_name ON countries(country_name);

