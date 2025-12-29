import json
import sys

# Vérifier la structure JSON et les duplications
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("✓ Le fichier JSON est valide et bien formé\n")
except json.JSONDecodeError as e:
    print(f"✗ Erreur de parsing JSON: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Erreur lors de la lecture: {e}")
    sys.exit(1)

# Obtenir la liste des quiz
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

print("="*80)
print("ANALYSE DE TOUS LES QUIZ")
print("="*80)

total_duplicates = 0
quiz_with_duplicates = []

for quiz in quizzes:
    if not isinstance(quiz, dict):
        continue

    name = quiz.get('name', 'Sans nom')
    questions = quiz.get('questions', [])

    # Vérifier les duplications
    question_texts = {}
    duplicates = []
    for i, q in enumerate(questions):
        text = q.get('question', '').lower().strip()
        if text in question_texts:
            duplicates.append((i+1, text, question_texts[text], q.get('id')))
        else:
            question_texts[text] = i + 1

    # Vérifier les IDs en double
    ids = [q.get('id') for q in questions]
    duplicate_ids = len(ids) - len(set(ids))

    status = "✓" if len(duplicates) == 0 and duplicate_ids == 0 else "✗"

    print(f"\n{status} {name}")
    print(f"   Questions: {len(questions)}")

    if duplicates:
        print(f"   ⚠ Questions en double: {len(duplicates)}")
        total_duplicates += len(duplicates)
        quiz_with_duplicates.append(name)
        # Afficher quelques exemples
        for idx, text, original_idx, qid in duplicates[:3]:
            print(f"      - Question {idx} (ID: {qid}) = Question {original_idx}")
    else:
        print(f"   ✓ Pas de duplication de questions")

    if duplicate_ids > 0:
        print(f"   ⚠ IDs en double: {duplicate_ids}")
    else:
        print(f"   ✓ IDs uniques")

print("\n" + "="*80)
print("RÉSUMÉ GLOBAL")
print("="*80)
print(f"Nombre total de quiz: {len(quizzes)}")
print(f"Quiz avec duplications: {len(quiz_with_duplicates)}")
if quiz_with_duplicates:
    print(f"Liste: {', '.join(quiz_with_duplicates)}")
print(f"Total de duplications trouvées: {total_duplicates}")
print("="*80)

