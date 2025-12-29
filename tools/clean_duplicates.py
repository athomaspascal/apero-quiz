import json
import os
import sys
from datetime import datetime
from collections import OrderedDict

print("Demarrage du script de nettoyage des doublons...")

file_path = r'src\main\resources\quiz-questions.json'

if not os.path.exists(file_path):
    print(f"ERREUR: Fichier non trouve: {file_path}")
    sys.exit(1)

# Faire une sauvegarde
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_path = f'quiz-questions-backup-{timestamp}.json'

print(f"\n1. Creation de la sauvegarde: {backup_path}")
sys.stdout.flush()

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"   Taille fichier: {len(content)} octets")
sys.stdout.flush()

with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"   OK: Sauvegarde creee")
sys.stdout.flush()

# Charger le fichier JSON
print("\n2. Chargement du fichier JSON...")
sys.stdout.flush()

root = json.loads(content)

# Gerer la structure
if isinstance(root, dict) and 'quizzes' in root:
    data = root['quizzes']
elif isinstance(root, list):
    data = root
else:
    print("ERREUR: Structure JSON inconnue!")
    sys.exit(1)

print(f"   OK: {len(data)} quiz charges")
sys.stdout.flush()

total_before = 0
total_after = 0
total_removed = 0

print("\n3. Nettoyage des doublons...")
sys.stdout.flush()

for idx, quiz in enumerate(data, 1):
    quiz_name = quiz.get('name', 'Sans nom')
    questions = quiz.get('questions', [])

    original_count = len(questions)
    total_before += original_count

    print(f"\n   [{idx}/{len(data)}] {quiz_name}")
    print(f"       Questions originales: {original_count}")
    sys.stdout.flush()

    # Nettoyer les doublons
    seen = OrderedDict()
    unique_questions = []

    for q in questions:
        question_text = q.get('question', '').strip().lower()
        if question_text not in seen:
            seen[question_text] = True
            unique_questions.append(q)

    new_count = len(unique_questions)
    removed = original_count - new_count

    if removed > 0:
        print(f"       NETTOYAGE: {removed} doublons supprimes")
        quiz['questions'] = unique_questions
        total_removed += removed

        # Reassigner les IDs
        for i, q in enumerate(unique_questions, 1):
            q['id'] = i

        print(f"       Questions restantes: {new_count}")
    else:
        print(f"       OK: Aucun doublon")

    sys.stdout.flush()
    total_after += new_count

print(f"\n{'='*60}")
print(f"RESUME")
print(f"{'='*60}")
print(f"Questions avant: {total_before}")
print(f"Questions apres: {total_after}")
print(f"Doublons supprimes: {total_removed}")
print(f"{'='*60}")
sys.stdout.flush()

if total_removed > 0:
    print(f"\n4. Enregistrement du fichier nettoye...")
    sys.stdout.flush()

    if isinstance(root, dict) and 'quizzes' in root:
        root['quizzes'] = data
        output = root
    else:
        output = data

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"   OK: Fichier nettoye enregistre!")
    print(f"\nSauvegarde: {backup_path}")
    print("TERMINÉ!")
else:
    print("\nAucun nettoyage necessaire.")

sys.stdout.flush()

