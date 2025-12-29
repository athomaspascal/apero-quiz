#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier que toutes les clés de traduction du Quiz Editor
sont présentes dans tous les fichiers de traduction.
"""

import re
from pathlib import Path

def load_properties(file_path):
    """Charge un fichier .properties et retourne un dictionnaire."""
    props = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorer les commentaires et lignes vides
                if not line or line.startswith('#'):
                    continue
                # Trouver la clé=valeur
                if '=' in line:
                    key, value = line.split('=', 1)
                    props[key.strip()] = value.strip()
    except Exception as e:
        print(f"Erreur lors de la lecture de {file_path}: {e}")
    return props

def main():
    # Définir les clés requises pour le Quiz Editor
    required_keys = [
        'quizEditor.title',
        'quizEditor.selectQuiz',
        'quizEditor.questionNumber',
        'quizEditor.question',
        'quizEditor.options',
        'quizEditor.answer',
        'quizEditor.difficultyLevel',
        'quizEditor.previous',
        'quizEditor.next',
        'quizEditor.updateFile',
        'quizEditor.error.noQuestions',
        'quizEditor.error.loadingQuestions',
        'quizEditor.error.loadingQuizList',
        'quizEditor.error.noQuestionSelected',
        'quizEditor.error.updatingQuestion',
        'quizEditor.success.questionUpdated',
        'menu.editquizzes'
    ]

    # Charger tous les fichiers de traduction
    base_path = Path('src/main/resources')
    translation_files = {
        'English (default)': base_path / 'messages.properties',
        'English': base_path / 'messages_en.properties',
        'French': base_path / 'messages_fr.properties',
        'Italian': base_path / 'messages_it.properties'
    }

    print("=" * 80)
    print("Vérification des traductions du Quiz Editor")
    print("=" * 80)
    print()

    all_ok = True

    for lang_name, file_path in translation_files.items():
        print(f"\n📝 Vérification de {lang_name}: {file_path.name}")
        print("-" * 80)

        if not file_path.exists():
            print(f"❌ Fichier non trouvé: {file_path}")
            all_ok = False
            continue

        props = load_properties(file_path)

        missing_keys = []
        for key in required_keys:
            if key not in props:
                missing_keys.append(key)
            else:
                print(f"✅ {key} = {props[key][:50]}..." if len(props[key]) > 50 else f"✅ {key} = {props[key]}")

        if missing_keys:
            print(f"\n❌ Clés manquantes dans {lang_name}:")
            for key in missing_keys:
                print(f"   - {key}")
            all_ok = False
        else:
            print(f"\n✅ Toutes les clés sont présentes dans {lang_name}!")

    print("\n" + "=" * 80)
    if all_ok:
        print("✅ SUCCÈS: Toutes les traductions du Quiz Editor sont présentes!")
    else:
        print("❌ ÉCHEC: Certaines traductions sont manquantes.")
    print("=" * 80)

    return 0 if all_ok else 1

if __name__ == '__main__':
    exit(main())

