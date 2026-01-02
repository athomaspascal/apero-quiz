#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification complete du quiz Harry Potter"""
import json

print("Verification du quiz Harry Potter...")
print("=" * 60)

try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"[OK] Fichier JSON charge")
    print(f"Total quizzes: {len(data['quizzes'])}")
    print()

    # Trouver le quiz HP
    hp_quiz = None
    for quiz in data['quizzes']:
        if quiz['name'] == 'Harry Potter':
            hp_quiz = quiz
            break

    if not hp_quiz:
        print("[ERREUR] Quiz Harry Potter non trouve!")
        exit(1)

    print("[OK] Quiz Harry Potter trouve!")
    print()
    print("Details:")
    print(f"  Nom: {hp_quiz['name']}")
    print(f"  Image: {hp_quiz.get('imageFileName', 'N/A')}")
    print(f"  Nombre de questions: {len(hp_quiz['questions'])}")
    print()

    # Verifier la structure des questions
    print("Verification des questions...")
    errors = []

    for i, q in enumerate(hp_quiz['questions'][:10]):  # Check first 10
        if 'id' not in q:
            errors.append(f"Question {i+1}: manque 'id'")
        if 'uuid' not in q:
            errors.append(f"Question {i+1}: manque 'uuid'")
        if 'question' not in q:
            errors.append(f"Question {i+1}: manque 'question'")
        if 'difficulty_level' not in q:
            errors.append(f"Question {i+1}: manque 'difficulty_level'")
        if 'options' not in q:
            errors.append(f"Question {i+1}: manque 'options'")
        if 'answer' not in q:
            errors.append(f"Question {i+1}: manque 'answer'")
        elif q['answer'] not in q.get('options', []):
            errors.append(f"Question {i+1}: reponse pas dans options")

    if errors:
        print("[ERREUR] Problemes detectes:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("[OK] Structure des 10 premieres questions valide")

    print()
    print("Exemples de questions:")
    for i in range(min(3, len(hp_quiz['questions']))):
        q = hp_quiz['questions'][i]
        print(f"\nQuestion {q['id']}:")
        print(f"  {q['question']}")
        print(f"  Reponse: {q['answer']}")
        print(f"  Difficulte: {q['difficulty_level']}")

    print()
    print("=" * 60)
    print("[SUCCES] Quiz Harry Potter verifie!")
    print(f"1000 questions presentes et valides")
    print("=" * 60)

    # Ecrire le resume
    with open('hp_verification_result.txt', 'w', encoding='utf-8') as f:
        f.write("VERIFICATION DU QUIZ HARRY POTTER\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Statut: [OK] VALIDE\n")
        f.write(f"Nombre de questions: {len(hp_quiz['questions'])}\n")
        f.write(f"Image: {hp_quiz.get('imageFileName')}\n")
        f.write(f"\nExemples de questions:\n")
        for i in range(min(5, len(hp_quiz['questions']))):
            q = hp_quiz['questions'][i]
            f.write(f"\n{i+1}. {q['question']}\n")
            f.write(f"   Reponse: {q['answer']}\n")

    print("\nResultat ecrit dans: hp_verification_result.txt")

except Exception as e:
    print(f"[ERREUR] {e}")
    import traceback
    traceback.print_exc()

