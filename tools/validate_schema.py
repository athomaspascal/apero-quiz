#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation du fichier JSON avec le schéma"""
import json
import jsonschema
from jsonschema import validate, ValidationError
import sys

def validate_json_file():
    """Valide le fichier JSON avec le schéma"""
    try:
        # Charger le schéma
        with open('src/main/resources/quiz-questions-schema.json', 'r', encoding='utf-8') as f:
            schema = json.load(f)

        # Charger le fichier JSON
        with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Valider
        validate(instance=data, schema=schema)

        print("✓ Le fichier JSON est valide selon le schéma !")
        print(f"\nStatistiques :")
        print(f"- Nombre de quiz : {len(data['quizzes'])}")

        for quiz in data['quizzes']:
            print(f"  • {quiz['name']} : {len(quiz['questions'])} questions")

        # Vérifier spécifiquement le quiz Disney
        disney_quiz = next((q for q in data['quizzes'] if q['name'] == 'Disney'), None)
        if disney_quiz:
            print(f"\n✓ Quiz Disney trouvé avec {len(disney_quiz['questions'])} questions")

            # Vérifier la structure de quelques questions
            errors = []
            for i, question in enumerate(disney_quiz['questions'][:10]):
                if 'uuid' not in question:
                    errors.append(f"Question {i+1} : manque UUID")
                if 'difficulty_level' not in question:
                    errors.append(f"Question {i+1} : manque difficulty_level")
                if 'answer' not in question.get('options', []):
                    errors.append(f"Question {i+1} : réponse non dans les options")

            if errors:
                print("\n⚠ Erreurs détectées dans les 10 premières questions :")
                for error in errors:
                    print(f"  - {error}")
            else:
                print("✓ Les 10 premières questions sont correctement structurées")

        return True

    except ValidationError as e:
        print(f"✗ Erreur de validation : {e.message}")
        print(f"  Chemin : {' -> '.join(str(p) for p in e.path)}")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ Erreur de parsing JSON : {e}")
        return False
    except Exception as e:
        print(f"✗ Erreur : {e}")
        return False

if __name__ == '__main__':
    success = validate_json_file()
    sys.exit(0 if success else 1)

