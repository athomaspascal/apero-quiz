import json
import sys

# Lire le fichier quiz-questions.json
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Trouver le quiz Greek Mythology
greek_quiz = None
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

for quiz in quizzes:
    if isinstance(quiz, dict) and 'Greek Mythology' in quiz.get('name', ''):
        greek_quiz = quiz
        break

if greek_quiz:
    print(f"Quiz trouvé: {greek_quiz['name']}")
    print(f"Nombre de questions: {len(greek_quiz.get('questions', []))}")

    # Vérifier les duplications
    questions_text = []
    duplicates = []

    for q in greek_quiz.get('questions', []):
        question_text = q.get('question', '')
        if question_text in questions_text:
            duplicates.append(question_text)
        else:
            questions_text.append(question_text)

    if duplicates:
        print(f"\n{len(duplicates)} questions en double trouvées:")
        for dup in duplicates[:10]:  # Afficher les 10 premières
            print(f"  - {dup}")
    else:
        print("\nAucune duplication trouvée!")

    # Afficher quelques questions pour voir la structure
    print("\nExemple de questions (5 premières):")
    for i, q in enumerate(greek_quiz.get('questions', [])[:5]):
        print(f"\n{i+1}. {q.get('question', '')}")
        print(f"   Réponse: {q.get('answer', '')}")
        print(f"   ID: {q.get('id', 'N/A')}")
else:
    print("Quiz Greek Mythology non trouvé!")

