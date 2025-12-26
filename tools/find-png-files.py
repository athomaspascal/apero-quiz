#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

# Lecture du fichier JSON
with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Type de données: {type(data)}", flush=True)

if isinstance(data, dict) and "quizzes" in data:
    quizzes = data["quizzes"]
    print(f"Nombre de quizzes: {len(quizzes)}", flush=True)

    # Chercher les fichiers PNG
    png_count = 0
    for i, quiz in enumerate(quizzes):
        if "imageFileName" in quiz and ".png" in quiz["imageFileName"]:
            png_count += 1
            print(f"Quiz #{i}: {quiz.get('name', 'N/A')} -> {quiz['imageFileName']}", flush=True)
            if png_count >= 5:  # Limiter à 5 pour ne pas surcharger
                break

    print(f"\nTotal de fichiers PNG trouvés: {png_count}", flush=True)

