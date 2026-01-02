#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correction du format dateUpdate dans le JSON"""
import json
from datetime import datetime
import shutil

print("Correction du format dateUpdate...")
print("=" * 60)

# 1. Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'src/main/resources/quiz-questions-backup-datefix-{timestamp}.json'
shutil.copy2('src/main/resources/quiz-questions.json', backup_file)
print(f"[OK] Backup cree: {backup_file}")

# 2. Charger le fichier
print("Chargement du fichier JSON...")
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"[OK] {len(data['quizzes'])} quizzes charges")

# 3. Corriger tous les dateUpdate
total_corrections = 0
for quiz in data['quizzes']:
    quiz_name = quiz['name']
    corrections_in_quiz = 0

    for question in quiz['questions']:
        if 'dateUpdate' in question:
            date_str = question['dateUpdate']
            # Si c'est juste une date (YYYY-MM-DD), ajouter l'heure
            if len(date_str) == 10 and date_str.count('-') == 2:
                question['dateUpdate'] = f"{date_str}T00:00:00"
                corrections_in_quiz += 1

    if corrections_in_quiz > 0:
        print(f"  {quiz_name}: {corrections_in_quiz} corrections")
        total_corrections += corrections_in_quiz

print(f"\n[OK] Total corrections: {total_corrections}")

# 4. Sauvegarder
print("Sauvegarde du fichier corrige...")
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("[SUCCES] Fichier corrige!")
print(f"Backup: {backup_file}")
print(f"Corrections effectuees: {total_corrections}")
print("=" * 60)

# Ecrire un resume
with open('dateUpdate_fix_summary.txt', 'w', encoding='utf-8') as f:
    f.write("CORRECTION DU FORMAT dateUpdate\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Date: {timestamp}\n")
    f.write(f"Corrections: {total_corrections}\n")
    f.write(f"Backup: {backup_file}\n")
    f.write(f"\nFormat corrige: YYYY-MM-DD -> YYYY-MM-DDTHH:MM:SS\n")
    f.write(f"Exemple: 2025-12-31 -> 2025-12-31T00:00:00\n")
    f.write(f"\nStatut: [OK] SUCCES\n")

print("\nResume ecrit dans: dateUpdate_fix_summary.txt")

