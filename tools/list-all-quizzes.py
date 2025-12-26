#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List all quiz names
"""
import json

with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

quizzes = data["quizzes"]

print("=" * 60)
print(f"TOTAL QUIZZES: {len(quizzes)}")
print("=" * 60)

for i, quiz in enumerate(quizzes, 1):
    name = quiz.get("name", "N/A")
    image = quiz.get("imageFileName", "N/A")
    print(f"{i}. {name}")
    print(f"   Image: {image}")
    print()

