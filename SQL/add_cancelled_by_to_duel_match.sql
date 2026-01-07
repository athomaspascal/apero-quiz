-- Migration script to add cancelled_by column to duel_match table
-- This allows tracking which user cancelled a duel

ALTER TABLE duel_match ADD COLUMN IF NOT EXISTS cancelled_by_user_id BIGINT;

-- Add foreign key constraint
ALTER TABLE duel_match
ADD CONSTRAINT IF NOT EXISTS fk_duel_match_cancelled_by
FOREIGN KEY (cancelled_by_user_id) REFERENCES users(user_id);

-- Add index for better query performance
CREATE INDEX IF NOT EXISTS idx_duel_match_cancelled_by ON duel_match(cancelled_by_user_id);

