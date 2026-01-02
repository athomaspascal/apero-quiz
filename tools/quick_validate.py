#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation rapide du fichier JSON"""
import json

try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('validation_result.txt', 'w', encoding='utf-8') as out:
        out.write("VALIDATION RESULTS\n")
        out.write("=" * 50 + "\n\n")

        out.write(f"Total quizzes: {len(data['quizzes'])}\n\n")

        for quiz in data['quizzes']:
            out.write(f"Quiz: {quiz['name']}\n")
            out.write(f"  Questions: {len(quiz['questions'])}\n")
            out.write(f"  Image: {quiz.get('imageFileName', 'N/A')}\n")

            # Vérifier la première question
            if quiz['questions']:
                q = quiz['questions'][0]
                out.write(f"  First question has: uuid={('uuid' in q)}, "
                         f"difficulty_level={('difficulty_level' in q)}, "
                         f"answer={('answer' in q)}, "
                         f"options={len(q.get('options', []))} options\n")
            out.write("\n")

        out.write("\n" + "=" * 50 + "\n")
        out.write("Validation complete!\n")

    print("Results written to validation_result.txt")

except Exception as e:
    with open('validation_result.txt', 'w', encoding='utf-8') as out:
        out.write(f"ERROR: {str(e)}\n")
    print(f"Error: {e}")

