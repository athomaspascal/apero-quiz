-- Create duel_match table for Duel Quiz feature
-- Date: 2026-01-05

CREATE TABLE IF NOT EXISTS duel_match (
    duel_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    player1_id BIGINT NOT NULL,
    player2_id BIGINT,
    quiz_id BIGINT,
    status VARCHAR(20) NOT NULL DEFAULT 'SEARCHING',
    player1_score INT,
    player2_score INT,
    player1_ready BOOLEAN DEFAULT FALSE,
    player2_ready BOOLEAN DEFAULT FALSE,
    player1_rematch BOOLEAN DEFAULT FALSE,
    player2_rematch BOOLEAN DEFAULT FALSE,
    rematch_count INT DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    countdown_started_at TIMESTAMP,
    CONSTRAINT fk_duel_player1 FOREIGN KEY (player1_id) REFERENCES user(user_id),
    CONSTRAINT fk_duel_player2 FOREIGN KEY (player2_id) REFERENCES user(user_id),
    CONSTRAINT fk_duel_quiz FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_duel_status ON duel_match(status);
CREATE INDEX IF NOT EXISTS idx_duel_player1 ON duel_match(player1_id);
CREATE INDEX IF NOT EXISTS idx_duel_player2 ON duel_match(player2_id);
CREATE INDEX IF NOT EXISTS idx_duel_created_at ON duel_match(created_at);

