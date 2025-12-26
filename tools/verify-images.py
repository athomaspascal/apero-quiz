#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify the image filenames were updated correctly
"""
import json

with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

quizzes = data["quizzes"]

print("=" * 60)
print("VERIFICATION OF IMAGE UPDATES")
print("=" * 60)

for quiz in quizzes:
    name = quiz.get("name", "")
    if "French History" in name or "World Cities" in name:
        image = quiz.get("imageFileName", "N/A")
        print(f"\nQuiz: {name}")
        print(f"Image: {image}")

print("\n" + "=" * 60)

