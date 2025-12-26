#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil
from datetime import datetime
import sys

print("Script démarré...", flush=True)

# Backup du fichier original
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f"src/main/resources/quiz-questions-backup-{timestamp}.json"
shutil.copy("src/main/resources/quiz-questions.json", backup_file)
print(f"✓ Backup créé: {backup_file}", flush=True)

# Lecture du fichier JSON
print("Lecture du fichier JSON...", flush=True)
try:
    with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"✓ Fichier chargé", flush=True)
except Exception as e:
    print(f"✗ Erreur lors de la lecture: {e}", flush=True)
    sys.exit(1)

# Compteurs
updates = 0

# Parcourir tous les quiz dans la clé "quizzes"
if "quizzes" in data:
    quizzes = data["quizzes"]
    print(f"Nombre de quiz à traiter: {len(quizzes)}", flush=True)

    for i, quiz in enumerate(quizzes):
        if "imageFileName" in quiz:
            # Remplacer french-history-quiz.png par quiz-french-history.svg
            if quiz["imageFileName"] == "french-history-quiz.png":
                quiz["imageFileName"] = "quiz-french-history.svg"
                updates += 1
                print(f"✓ Quiz #{i} '{quiz.get('name', 'N/A')}': french-history-quiz.png → quiz-french-history.svg", flush=True)

            # Remplacer world-cities-quiz.png par quiz-world-cities.svg
            elif quiz["imageFileName"] == "world-cities-quiz.png":
                quiz["imageFileName"] = "quiz-world-cities.svg"
                updates += 1
                print(f"✓ Quiz #{i} '{quiz.get('name', 'N/A')}': world-cities-quiz.png → quiz-world-cities.svg", flush=True)
else:
    print("✗ Clé 'quizzes' non trouvée dans le JSON", flush=True)

# Sauvegarder les modifications
with open("src/main/resources/quiz-questions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ {updates} image(s) mise(s) à jour", flush=True)
print("✓ Fichier quiz-questions.json mis à jour avec succès", flush=True)

