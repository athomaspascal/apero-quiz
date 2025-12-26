#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update image filenames in quiz-questions.json
"""
import json
import shutil
from datetime import datetime

# Backup the file first
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f"src/main/resources/quiz-questions_backup_{timestamp}.json"
shutil.copy("src/main/resources/quiz-questions.json", backup_file)
print(f"✓ Backup created: {backup_file}")

# Read the JSON file
with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Get the quizzes array
if isinstance(data, dict) and "quizzes" in data:
    quizzes = data["quizzes"]
    print(f"Found {len(quizzes)} quizzes in the file")
else:
    print("Error: Expected structure with 'quizzes' key not found")
    exit(1)

# Update image filenames
updated = 0
for i, quiz in enumerate(quizzes):
    if not isinstance(quiz, dict):
        print(f"Warning: Quiz at index {i} is not a dictionary, skipping...")
        continue

    quiz_name = quiz.get("name", "")

    if quiz_name == "French History 1000":
        old_image = quiz.get("imageFileName", "N/A")
        quiz["imageFileName"] = "french-history-quiz.png"
        print(f"✓ Updated 'French History 1000': {old_image} -> french-history-quiz.png")
        updated += 1
    elif quiz_name == "World Cities - Latitude & Longitude":
        old_image = quiz.get("imageFileName", "N/A")
        quiz["imageFileName"] = "world-cities-quiz.png"
        print(f"✓ Updated 'World Cities - Latitude & Longitude': {old_image} -> world-cities-quiz.png")
        updated += 1

# Write the updated JSON file
with open("src/main/resources/quiz-questions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Updated {updated} quiz image(s)")
print("✓ quiz-questions.json has been updated successfully!")

