import json
import sys

# Vérifier la structure JSON
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
    print("✗ Quiz Game of Thrones non trouvé!")
    sys.exit(1)

print(f"✓ Quiz trouvé: {got_quiz['name']}")

# Vérifier les questions
questions = got_quiz.get('questions', [])
print(f"✓ Nombre total de questions: {len(questions)}")

# Vérifier les duplications
question_texts = {}
duplicates = []
for i, q in enumerate(questions):
    text = q.get('question', '').lower().strip()
    if text in question_texts:
        duplicates.append((i+1, text, question_texts[text]))
    else:
        question_texts[text] = i + 1

if duplicates:
    print(f"\n✗ {len(duplicates)} questions en double trouvées:")
    for idx, text, original_idx in duplicates[:5]:
        print(f"  Question {idx} est identique à la question {original_idx}")
else:
    print("✓ Aucune duplication trouvée!")

# Vérifier les IDs
ids = [q.get('id') for q in questions]
if len(ids) != len(set(ids)):
    print("✗ Des IDs en double ont été trouvés!")
else:
    print(f"✓ Tous les IDs sont uniques (1 à {max(ids)})")

# Vérifier les UUIDs
uuids = [q.get('uuid') for q in questions]
if len(uuids) != len(set(uuids)):
    print("✗ Des UUIDs en double ont été trouvés!")
else:
    print("✓ Tous les UUIDs sont uniques")

# Vérifier la structure de chaque question
missing_fields = []
for i, q in enumerate(questions):
    required_fields = ['question', 'options', 'answer', 'id', 'uuid', 'difficulty_level']
    for field in required_fields:
        if field not in q:
            missing_fields.append((i+1, field))

if missing_fields:
    print(f"\n✗ {len(missing_fields)} champs manquants trouvés:")
    for idx, field in missing_fields[:10]:
        print(f"  Question {idx}: manque '{field}'")
else:
    print("✓ Toutes les questions ont tous les champs requis")

# Vérifier le nombre d'options
wrong_options = []
for i, q in enumerate(questions):
    options = q.get('options', [])
    if len(options) != 4:
        wrong_options.append((i+1, len(options)))

if wrong_options:
    print(f"\n✗ {len(wrong_options)} questions n'ont pas exactement 4 options:")
    for idx, count in wrong_options[:5]:
        print(f"  Question {idx}: {count} options")
else:
    print("✓ Toutes les questions ont exactement 4 options")

# Vérifier que la réponse est dans les options
wrong_answers = []
for i, q in enumerate(questions):
    answer = q.get('answer', '')
    options = q.get('options', [])
    if answer not in options:
        wrong_answers.append((i+1, answer))

if wrong_answers:
    print(f"\n✗ {len(wrong_answers)} questions ont une réponse qui n'est pas dans les options:")
    for idx, answer in wrong_answers[:5]:
        print(f"  Question {idx}: réponse '{answer}'")
else:
    print("✓ Toutes les réponses sont dans les options")

print("\n" + "="*60)
print("RÉSUMÉ FINAL - GAME OF THRONES QUIZ:")
print("="*60)
print(f"Quiz: {got_quiz['name']}")
print(f"Nombre de questions: {len(questions)}")
print(f"Pas de duplications: {'✓ OUI' if not duplicates else '✗ NON'}")
print(f"Structure valide: {'✓ OUI' if not (missing_fields or wrong_options or wrong_answers) else '✗ NON'}")
print(f"De 35 à {len(questions)} questions: +{len(questions) - 35} nouvelles questions")
print("="*60)

