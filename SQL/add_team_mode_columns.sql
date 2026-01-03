-- Script SQL pour ajouter les colonnes du mode équipe
-- À exécuter sur la base de données

-- Ajouter la colonne team_mode à la table quiz_session
ALTER TABLE quiz_session ADD COLUMN IF NOT EXISTS team_mode BOOLEAN NOT NULL DEFAULT FALSE;

-- Ajouter la colonne selected_teams à la table quiz_session
ALTER TABLE quiz_session ADD COLUMN IF NOT EXISTS selected_teams VARCHAR(500);

-- Ajouter la colonne team_name à la table quiz_participant
ALTER TABLE quiz_participant ADD COLUMN IF NOT EXISTS team_name VARCHAR(100);

-- Commenter les colonnes pour la documentation
COMMENT ON COLUMN quiz_session.team_mode IS 'Indique si le mode équipe est activé pour cette session';
COMMENT ON COLUMN quiz_session.selected_teams IS 'Liste des équipes sélectionnées séparées par des virgules';
COMMENT ON COLUMN quiz_participant.team_name IS 'Nom de l''équipe du participant (stark, lannister, etc.)';

