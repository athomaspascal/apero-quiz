import json
import sys
from datetime import datetime

# Lire le fichier existant
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Obtenir les quiz
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

print(f"Nombre de quiz trouvés: {len(quizzes)}")

# Date par défaut pour toutes les questions existantes
default_date = datetime.now().isoformat()

total_questions = 0
questions_updated = 0

for quiz in quizzes:
    if isinstance(quiz, dict):
        quiz_name = quiz.get('name', 'Sans nom')
        questions = quiz.get('questions', [])

        for question in questions:
            total_questions += 1
            # Ajouter dateUpdate si elle n'existe pas
            if 'dateUpdate' not in question or question.get('dateUpdate') is None:
                question['dateUpdate'] = default_date
                questions_updated += 1

print(f"\nQuestions totales: {total_questions}")
print(f"Questions mises à jour avec dateUpdate: {questions_updated}")

# Créer un backup avec timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_file = f"quiz-questions-backup-{timestamp}.json"

try:
    # Backup
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nBackup créé: {backup_file}")

    # Sauvegarder la version mise à jour
    with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Fichier quiz-questions.json mis à jour avec succès!")

except Exception as e:
    print(f"Erreur lors de la sauvegarde: {e}")
    sys.exit(1)

print("\n✓ Terminé! Toutes les questions ont maintenant un champ dateUpdate.")

