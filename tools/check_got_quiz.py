import json
import sys

# Vérifier la structure JSON et les duplications
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("✓ Le fichier JSON est valide et bien formé")
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
        duplicates.append((i+1, text, question_texts[text], q.get('id')))
    else:
        question_texts[text] = i + 1

if duplicates:
    print(f"\n✗ {len(duplicates)} questions en double trouvées:")
    for idx, text, original_idx, qid in duplicates[:20]:
        print(f"  Question {idx} (ID: {qid}) est identique à la question {original_idx}")
        print(f"    -> {text[:80]}...")
else:
    print("✓ Aucune duplication trouvée!")

# Vérifier les IDs
ids = [q.get('id') for q in questions]
if len(ids) != len(set(ids)):
    print("\n✗ Des IDs en double ont été trouvés!")
    id_counts = {}
    for qid in ids:
        id_counts[qid] = id_counts.get(qid, 0) + 1
    duplicate_ids = [qid for qid, count in id_counts.items() if count > 1]
    print(f"  IDs en double: {duplicate_ids[:10]}")
else:
    print(f"✓ Tous les IDs sont uniques")

# Vérifier les UUIDs
uuids = [q.get('uuid') for q in questions]
if len(uuids) != len(set(uuids)):
    print("✗ Des UUIDs en double ont été trouvés!")
else:
    print("✓ Tous les UUIDs sont uniques")

print("\n" + "="*60)
print("RÉSUMÉ:")
print("="*60)
print(f"Quiz: {got_quiz['name']}")
print(f"Nombre de questions: {len(questions)}")
print(f"Duplications: {len(duplicates)} trouvées")
print("="*60)

