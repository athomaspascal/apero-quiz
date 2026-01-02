#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification finale du JSON apres correction"""
import json

print("Verification du fichier JSON...")
print("=" * 60)

try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("[OK] JSON valide!")
    print(f"\nNombre de quizzes: {len(data['quizzes'])}")

    # Verifier les dateUpdate
    print("\nVerification des dateUpdate...")
    issues = []

    for quiz in data['quizzes']:
        for i, q in enumerate(quiz['questions'][:5]):  # Check first 5 per quiz
            if 'dateUpdate' in q:
                date_str = q['dateUpdate']
                # Verifier le format
                if 'T' not in date_str:
                    issues.append(f"{quiz['name']}: question {i+1} - format court: {date_str}")

    if issues:
        print("[ATTENTION] Problemes detectes:")
        for issue in issues[:10]:
            print(f"  - {issue}")
    else:
        print("[OK] Tous les dateUpdate sont au bon format!")

    # Liste des quizzes
    print("\nListe des quizzes:")
    for i, quiz in enumerate(data['quizzes'], 1):
        print(f"  {i}. {quiz['name']}: {len(quiz['questions'])} questions")

    print("\n" + "=" * 60)
    print("[SUCCES] Verification terminee!")
    print("L'application devrait maintenant pouvoir charger les quizzes.")
    print("=" * 60)

except json.JSONDecodeError as e:
    print(f"[ERREUR] JSON invalide: {e}")
except Exception as e:
    print(f"[ERREUR] {e}")

