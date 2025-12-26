#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

print("=== VÉRIFICATION FINALE DES IMAGES SVG ===\n")

# 1. Vérifier le fichier JSON
json_file = "src/main/resources/quiz-questions.json"
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

quizzes = data.get("quizzes", [])
print(f"✓ Nombre de quiz dans le JSON: {len(quizzes)}\n")

# 2. Vérifier les images pour chaque quiz
images_dir = "src/main/resources/META-INF/resources/images"
missing_files = []
svg_files = []
png_files = []

for i, quiz in enumerate(quizzes):
    name = quiz.get("name", "N/A")
    image_file = quiz.get("imageFileName", "N/A")

    if image_file != "N/A":
        if image_file.endswith(".svg"):
            svg_files.append((i, name, image_file))
        elif image_file.endswith(".png"):
            png_files.append((i, name, image_file))

        full_path = os.path.join(images_dir, image_file)
        if not os.path.exists(full_path):
            missing_files.append((i, name, image_file))

# 3. Afficher les résultats
print(f"✓ Fichiers SVG: {len(svg_files)}")
print(f"✗ Fichiers PNG: {len(png_files)}")
print(f"✗ Fichiers manquants: {len(missing_files)}\n")

if png_files:
    print("⚠ ATTENTION: Fichiers PNG trouvés:")
    for i, name, img in png_files[:5]:
        print(f"  - Quiz #{i}: {name} -> {img}")
    if len(png_files) > 5:
        print(f"  ... et {len(png_files) - 5} autres")
    print()

if missing_files:
    print("⚠ ATTENTION: Fichiers d'images manquants:")
    for i, name, img in missing_files[:5]:
        print(f"  - Quiz #{i}: {name} -> {img}")
    if len(missing_files) > 5:
        print(f"  ... et {len(missing_files) - 5} autres")
    print()

# 4. Vérifier spécifiquement les quiz French History et World Cities
target_quizzes = [
    ("French History", "quiz-french-history.svg"),
    ("World Cities", "quiz-world-cities.svg")
]

print("=== VÉRIFICATION DES QUIZ SPÉCIFIQUES ===\n")
for quiz_name_part, expected_image in target_quizzes:
    found = False
    for i, quiz in enumerate(quizzes):
        if quiz_name_part.lower() in quiz.get("name", "").lower():
            actual_image = quiz.get("imageFileName", "N/A")
            image_path = os.path.join(images_dir, actual_image)
            exists = os.path.exists(image_path)

            status = "✓" if exists and actual_image == expected_image else "✗"
            print(f"{status} Quiz #{i}: {quiz['name']}")
            print(f"  Image: {actual_image}")
            print(f"  Fichier existe: {'Oui' if exists else 'Non'}")
            if exists:
                size = os.path.getsize(image_path)
                print(f"  Taille: {size} octets")
            print()
            found = True
            break

    if not found:
        print(f"✗ Quiz contenant '{quiz_name_part}' non trouvé\n")

print("=== RÉSUMÉ ===")
if not png_files and not missing_files:
    print("✓ Tout est en ordre! Tous les quiz utilisent des fichiers SVG et tous les fichiers existent.")
else:
    if png_files:
        print(f"⚠ {len(png_files)} quiz utilisent encore des fichiers PNG")
    if missing_files:
        print(f"⚠ {len(missing_files)} fichiers d'images sont manquants")

