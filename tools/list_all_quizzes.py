#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("TOUS LES QUIZZES:")
print("="*60)
for i, quiz in enumerate(data['quizzes'], 1):
    print(f"{i}. {quiz['name']}: {len(quiz['questions'])} questions")

hp = [q for q in data['quizzes'] if q['name'] == 'Harry Potter']
if hp:
    print(f"\n[OK] Harry Potter trouve avec {len(hp[0]['questions'])} questions")
    print(f"Image: {hp[0].get('imageFileName')}")
else:
    print("\n[ERREUR] Harry Potter non trouve")

