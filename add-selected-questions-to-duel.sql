-- Add selected_question_ids column to duel_match table
ALTER TABLE duel_match ADD COLUMN IF NOT EXISTS selected_question_ids VARCHAR(1000);

