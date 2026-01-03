-- Script to add country_id column to users table

-- Add country_id column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS country_id BIGINT;

-- Add foreign key constraint
ALTER TABLE users ADD CONSTRAINT fk_users_country
    FOREIGN KEY (country_id) REFERENCES countries(country_id);

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_users_country_id ON users(country_id);

