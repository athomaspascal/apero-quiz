#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Lecture du fichier JSON
with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Type de données: {type(data)}")
print(f"Longueur: {len(data) if isinstance(data, list) else 'N/A'}")

if isinstance(data, list):
    print(f"\nPremier élément - Type: {type(data[0])}")
    if isinstance(data[0], dict):
        print(f"Clés: {list(data[0].keys())[:5]}")
        if "imageFileName" in data[0]:
            print(f"imageFileName dans premier élément: {data[0]['imageFileName']}")
else:
    print(f"\nClés principales: {list(data.keys())}")
    for key in data.keys():
        print(f"  {key}: type={type(data[key])}, len={len(data[key]) if isinstance(data[key], (list, dict)) else 'N/A'}")
        if isinstance(data[key], list) and len(data[key]) > 0:
            print(f"    Premier élément: {type(data[key][0])}")
            if isinstance(data[key][0], dict):
                print(f"    Clés: {list(data[key][0].keys())[:10]}")

