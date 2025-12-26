#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

images_dir = "src/main/resources/META-INF/resources/images"

svg_files = [
    "quiz-french-history.svg",
    "quiz-world-cities.svg",
    "france.svg",
    "japan.svg",
    "europe.svg",
    "knowledge.svg"
]

print("=== DIMENSIONS DES FICHIERS SVG ===\n")

for svg_file in svg_files:
    file_path = os.path.join(images_dir, svg_file)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(500)  # Lire les premiers 500 caractères

            # Rechercher width et height
            width_match = re.search(r'width="(\d+)"', content)
            height_match = re.search(r'height="(\d+)"', content)
            viewbox_match = re.search(r'viewBox="([^"]+)"', content)

            width = width_match.group(1) if width_match else "N/A"
            height = height_match.group(1) if height_match else "N/A"
            viewbox = viewbox_match.group(1) if viewbox_match else "N/A"

            size = os.path.getsize(file_path)

            print(f"{svg_file}")
            print(f"  Dimensions: {width} x {height} px")
            print(f"  ViewBox: {viewbox}")
            print(f"  Taille fichier: {size} octets")
            print()
    else:
        print(f"{svg_file} - FICHIER NON TROUVÉ\n")

