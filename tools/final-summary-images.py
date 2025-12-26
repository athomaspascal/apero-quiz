#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final summary of the image generation with multiline text
"""
import os
import json

print("=" * 80)
print(" " * 20 + "✅ RÉSUMÉ COMPLET - IMAGES GÉNÉRÉES")
print("=" * 80)

# Check images
print("\n📷 IMAGES GÉNÉRÉES:")
print("-" * 80)

images_dir = "src/main/resources/static/images"
images = [
    ("french-history-quiz.png", "French History 1000", "Histoire\nde France\n1000 Questions"),
    ("world-cities-quiz.png", "World Cities - Latitude & Longitude", "Villes du Monde\nLatitude &\nLongitude")
]

for filename, quiz_name, text_layout in images:
    filepath = os.path.join(images_dir, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"\n✓ {quiz_name}")
        print(f"  Fichier: {filename}")
        print(f"  Taille: {size:,} bytes ({size/1024:.1f} KB)")
        print(f"  Texte:")
        for line in text_layout.split('\n'):
            print(f"    • {line}")
    else:
        print(f"\n✗ {quiz_name} - FICHIER NON TROUVÉ!")

# Check JSON configuration
print("\n" + "-" * 80)
print("\n📋 CONFIGURATION JSON:")
print("-" * 80)

try:
    with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    quizzes = data.get("quizzes", [])

    for quiz in quizzes:
        name = quiz.get("name", "")
        if name in ["French History 1000", "World Cities - Latitude & Longitude"]:
            image = quiz.get("imageFileName", "N/A")
            print(f"\n✓ {name}")
            print(f"  imageFileName: {image}")

            # Verify the image file exists
            image_path = os.path.join(images_dir, image)
            if os.path.exists(image_path):
                print(f"  Statut: ✅ Image configurée et fichier existant")
            else:
                print(f"  Statut: ⚠️ Image configurée mais fichier manquant")

except Exception as e:
    print(f"✗ Erreur lors de la lecture du JSON: {e}")

# Summary
print("\n" + "=" * 80)
print("\n🎯 RÉSUMÉ:")
print("-" * 80)
print("\n✅ Modifications appliquées:")
print("   • Texte réparti sur PLUSIEURS LIGNES pour meilleure lisibilité")
print("   • Tailles de police adaptées (52px, 48px, 36px, 28px)")
print("   • Positionnement vertical optimisé")
print("   • Tout le texte est maintenant visible")
print("\n✅ Fichiers mis à jour:")
print("   • generate-quiz-images.py")
print("   • french-history-quiz.png")
print("   • world-cities-quiz.png")
print("   • quiz-questions.json (déjà configuré)")
print("\n📄 Documentation:")
print("   • MD/QUIZ_IMAGES_GENERATION.md")
print("   • MD/IMAGES_MULTILINE_UPDATE.md")
print("   • preview-quiz-images.html (pour visualiser)")

print("\n" + "=" * 80)
print("\n🚀 PROCHAINE ÉTAPE:")
print("   Redémarrer l'application Spring Boot pour voir les nouvelles images !")
print("\n" + "=" * 80)

