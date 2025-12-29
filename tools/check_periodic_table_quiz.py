import json
import sys

# Lire le fichier existant
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Trouver le quiz Periodic Table
periodic_quiz = None
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

for quiz in quizzes:
    if isinstance(quiz, dict):
        name = quiz.get('name', '')
        if 'periodic' in name.lower() or 'tableau' in name.lower() or 'périodique' in name.lower():
            periodic_quiz = quiz
            break

if not periodic_quiz:
    print("Quiz sur le tableau périodique non trouvé!")
    print("\nListe des quiz disponibles:")
    for quiz in quizzes:
        if isinstance(quiz, dict):
            print(f"  - {quiz.get('name', 'Sans nom')}")
    sys.exit(1)

# Obtenir les questions
questions = periodic_quiz.get('questions', [])

print("="*60)
print(f"Quiz: {periodic_quiz['name']}")
print("="*60)
print(f"Nombre de questions: {len(questions)}")
print(f"Image: {periodic_quiz.get('imageFileName', 'N/A')}")
print("="*60)

if len(questions) > 0:
    print("\nExemples de questions (5 premières):")
    for i, q in enumerate(questions[:5]):
        print(f"\n{i+1}. {q.get('question', '')}")
        print(f"   Réponse: {q.get('answer', '')}")

