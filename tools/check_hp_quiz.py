#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    hp_quiz = None
    for quiz in data['quizzes']:
        if quiz['name'] == 'Harry Potter':
            hp_quiz = quiz
            break

    with open('hp_check_result.txt', 'w', encoding='utf-8') as out:
        if hp_quiz:
            out.write(f"✓ Quiz Harry Potter trouvé!\n")
            out.write(f"Nombre de questions: {len(hp_quiz['questions'])}\n")
            out.write(f"Image: {hp_quiz.get('imageFileName', 'N/A')}\n")
        else:
            out.write("✗ Quiz Harry Potter NON trouvé\n")
            out.write(f"Quizzes disponibles: {[q['name'] for q in data['quizzes']]}\n")

    print("Résultat écrit dans hp_check_result.txt")
except Exception as e:
    with open('hp_check_result.txt', 'w', encoding='utf-8') as out:
        out.write(f"ERREUR: {e}\n")
    print(f"Erreur: {e}")

