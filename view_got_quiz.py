import json
import sys

# Lire le fichier existant
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Trouver le quiz Game of Thrones
got_quiz = None
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

for quiz in quizzes:
    if isinstance(quiz, dict) and 'Game of Thrones' in quiz.get('name', ''):
        got_quiz = quiz
        break

if not got_quiz:
    print("Quiz Game of Thrones non trouvé!")
    sys.exit(1)

# Obtenir les questions existantes
existing_questions = set()
current_max_id = 0
for q in got_quiz.get('questions', []):
    existing_questions.add(q.get('question', '').lower().strip())
    current_max_id = max(current_max_id, q.get('id', 0))

print(f"Quiz trouvé: {got_quiz['name']}")
print(f"Questions existantes: {len(existing_questions)}")
print(f"ID maximum actuel: {current_max_id}")

# Afficher quelques questions existantes pour référence
print("\nExemples de questions existantes:")
for i, q in enumerate(got_quiz.get('questions', [])[:5]):
    print(f"{i+1}. {q.get('question', '')}")

