#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic script to understand JSON structure
"""
import json

try:
    with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 60)
    print("JSON STRUCTURE DIAGNOSTIC")
    print("=" * 60)
    print(f"Root type: {type(data)}")
    print(f"Root type name: {type(data).__name__}")

    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())}")
        if "quizzes" in data:
            print(f"'quizzes' type: {type(data['quizzes'])}")
            if isinstance(data['quizzes'], list) and len(data['quizzes']) > 0:
                print(f"First quiz type: {type(data['quizzes'][0])}")
                if isinstance(data['quizzes'][0], dict):
                    print(f"First quiz keys: {list(data['quizzes'][0].keys())}")
                    print(f"First quiz name: {data['quizzes'][0].get('name', 'N/A')}")
    elif isinstance(data, list):
        print(f"Array length: {len(data)}")
        if len(data) > 0:
            print(f"First element type: {type(data[0])}")
            if isinstance(data[0], dict):
                print(f"First element keys: {list(data[0].keys())}")
                print(f"First element name: {data[0].get('name', 'N/A')}")
            else:
                print(f"First element value (first 100 chars): {str(data[0])[:100]}")

    print("=" * 60)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

