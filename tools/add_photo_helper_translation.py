# -*- coding: utf-8 -*-
"""Add photoUploadHelper translation to messages files"""

import os

# File paths
files = {
    'fr': r'c:\Users\athom\IdeaProjects\quizz1\src\main\resources\messages_fr.properties',
    'it': r'c:\Users\athom\IdeaProjects\quizz1\src\main\resources\messages_it.properties',
}

translations = {
    'fr': 'register.photoUploadHelper=Sélectionnez une image JPEG, PNG ou GIF (max 10 MB). La photo sera redimensionnée automatiquement.\n',
    'it': 'register.photoUploadHelper=Seleziona un\'immagine JPEG, PNG o GIF (max 10 MB). La foto verrà ridimensionata automaticamente.\n',
}

def add_translation(filepath, translation_line):
    """Add translation after register.photoUpload if not already present"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    added_count = 0

    while i < len(lines):
        new_lines.append(lines[i])

        # Check if this line contains photoUpload and next line doesn't have photoUploadHelper
        if 'register.photoUpload=' in lines[i]:
            if i+1 < len(lines) and 'register.photoUploadHelper=' not in lines[i+1]:
                new_lines.append(translation_line)
                added_count += 1

        i += 1

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    return added_count

# Process each file
for lang, filepath in files.items():
    if os.path.exists(filepath):
        count = add_translation(filepath, translations[lang])
        print(f"Added {count} photoUploadHelper translation(s) to messages_{lang}.properties")
    else:
        print(f"File not found: {filepath}")

print("\nDone!")

