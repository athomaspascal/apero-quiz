#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify that the generated images exist and show their properties
"""
import os
from PIL import Image

print("=" * 70)
print("VERIFICATION DES IMAGES GENEREES")
print("=" * 70)

images_dir = "src/main/resources/static/images"

images_to_check = [
    ("french-history-quiz.png", "French History 1000"),
    ("world-cities-quiz.png", "World Cities - Latitude & Longitude")
]

for filename, quiz_name in images_to_check:
    filepath = os.path.join(images_dir, filename)

    print(f"\n📷 {quiz_name}")
    print(f"   Fichier: {filename}")

    if os.path.exists(filepath):
        print(f"   ✓ Fichier existe")

        # Get file size
        file_size = os.path.getsize(filepath)
        print(f"   Taille: {file_size:,} bytes ({file_size/1024:.1f} KB)")

        # Get image dimensions
        try:
            with Image.open(filepath) as img:
                print(f"   Dimensions: {img.width}x{img.height} pixels")
                print(f"   Format: {img.format}")
                print(f"   Mode: {img.mode}")
        except Exception as e:
            print(f"   ✗ Erreur lors de la lecture: {e}")
    else:
        print(f"   ✗ Fichier non trouvé!")

print("\n" + "=" * 70)
print("✓ Vérification terminée")
print("=" * 70)

