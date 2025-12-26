#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add difficulty_level attribute to all questions in quiz-questions.json
"""

import json
import shutil
import os
import sys
from datetime import datetime

def add_difficulty_level():
    """Add difficulty_level attribute to all qudi estions with default value 1"""

    print("Starting script...")
    print(f"Current directory: {os.getcwd()}")

    input_file = "src/main/resources/quiz-questions.json"

    # Check if file exists
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        print("Files in src/main/resources:")
        if os.path.exists("src/main/resources"):
            for f in os.listdir("src/main/resources"):
                if f.endswith('.json'):
                    print(f"  - {f}")
        return False

    print(f"File found: {input_file}")

    # Create backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"src/main/resources/quiz-questions_backup_{timestamp}.json"

    print(f"Creating backup: {backup_file}")
    try:
        shutil.copy2(input_file, backup_file)
        print("Backup created successfully")
    except Exception as e:
        print(f"ERROR creating backup: {e}")
        return False

    # Read the JSON file
    print(f"Reading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if it's a dict with "quizzes" key or a direct list
        if isinstance(data, dict) and 'quizzes' in data:
            quizzes = data['quizzes']
            has_wrapper = True
        elif isinstance(data, list):
            quizzes = data
            has_wrapper = False
        else:
            print(f"ERROR: Unexpected JSON structure. Type: {type(data)}")
            return False

        print(f"JSON loaded successfully. Number of quizzes: {len(quizzes)}")
    except Exception as e:
        print(f"ERROR reading JSON: {e}")
        return False

    # Add difficulty_level to each question
    total_questions = 0
    modified_questions = 0

    for quiz in quizzes:
        quiz_name = quiz.get('name', 'Unknown')
        print(f"\nProcessing quiz: {quiz_name}")

        if 'questions' in quiz:
            for question in quiz['questions']:
                total_questions += 1

                # Add difficulty_level with value 1 if not present
                if 'difficulty_level' not in question:
                    # Create a new ordered dictionary to insert difficulty_level after question
                    new_question = {}
                    for key, value in question.items():
                        new_question[key] = value
                        # Insert difficulty_level right after 'question' attribute
                        if key == 'question':
                            new_question['difficulty_level'] = 1
                            modified_questions += 1

                    # Update the question with the new ordered dict
                    question.clear()
                    question.update(new_question)

    print(f"\nTotal questions: {total_questions}, Modified: {modified_questions}")

    # Write back to the file with proper formatting
    print(f"\nWriting modified JSON to {input_file}...")
    try:
        # Restore the wrapper if it was present
        if has_wrapper:
            output_data = {'quizzes': quizzes}
        else:
            output_data = quizzes

        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print("File written successfully")
    except Exception as e:
        print(f"ERROR writing JSON: {e}")
        return False

    print("\n" + "="*60)
    print("✅ COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"Total questions processed: {total_questions}")
    print(f"Questions modified: {modified_questions}")
    print(f"Backup created: {backup_file}")
    print(f"Output file: {input_file}")
    print("="*60)
    return True

if __name__ == "__main__":
    try:
        success = add_difficulty_level()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

