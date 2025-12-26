#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil
from datetime import datetime

print("=== AJOUT DU QUIZ TABLEAU PÉRIODIQUE ===\n")

# 1. Backup du fichier original
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f"src/main/resources/quiz-questions-backup-{timestamp}.json"
shutil.copy("src/main/resources/quiz-questions.json", backup_file)
print(f"✓ Backup créé: {backup_file}")

# 2. Charger le fichier JSON principal
with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    main_data = json.load(f)

print(f"✓ Fichier principal chargé: {len(main_data['quizzes'])} quiz existants")

# 3. Charger le nouveau quiz
with open("periodic-table-quiz-temp.json", "r", encoding="utf-8") as f:
    new_quiz = json.load(f)

print(f"✓ Nouveau quiz chargé: {new_quiz['name']}")
print(f"  - Nombre de questions: {len(new_quiz['questions'])}")

# 4. Ajouter le nouveau quiz
main_data['quizzes'].append(new_quiz)

print(f"✓ Quiz ajouté au fichier principal")
print(f"  - Total de quiz: {len(main_data['quizzes'])}")

# 5. Sauvegarder le fichier mis à jour
with open("src/main/resources/quiz-questions.json", "w", encoding="utf-8") as f:
    json.dump(main_data, f, ensure_ascii=False, indent=2)

print(f"✓ Fichier quiz-questions.json mis à jour avec succès")

# 6. Vérification
with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    verify_data = json.load(f)

print(f"\n=== VÉRIFICATION ===")
print(f"✓ Nombre total de quiz: {len(verify_data['quizzes'])}")

# Trouver le quiz du tableau périodique
for i, quiz in enumerate(verify_data['quizzes']):
    if 'Periodic Table' in quiz['name']:
        print(f"✓ Quiz trouvé à l'index #{i}: {quiz['name']}")
        print(f"  - Nombre de questions: {len(quiz['questions'])}")
        print(f"  - Image: {quiz['imageFileName']}")

        # Vérifier quelques questions
        if len(quiz['questions']) > 0:
            print(f"\n  Exemple de questions:")
            for j in range(min(3, len(quiz['questions']))):
                q = quiz['questions'][j]
                print(f"    Q{q['id']}: {q['question'][:60]}...")
        break

print("\n✓ Ajout terminé avec succès!")

