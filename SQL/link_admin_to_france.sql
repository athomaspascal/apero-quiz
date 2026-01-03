-- Link admin user to France
UPDATE user
SET country_id = (SELECT id FROM country WHERE sigle = 'FRA')
WHERE email = 'administrateur@quiz.admin';

