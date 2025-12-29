import json
import sys
import os
from collections import defaultdict

def check_duplicates():
    """Verifie les questions en double dans le fichier quiz-questions.json"""

    file_path = r'src\main\resources\quiz-questions.json'

    if not os.path.exists(file_path):
        print(f"Erreur: Fichier non trouve: {file_path}")
        return -1

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("=" * 80)
    print("VERIFICATION DES QUESTIONS EN DOUBLE")
    print("=" * 80)
    print()

    total_questions = 0
    total_duplicates = 0

    for quiz in data:
        quiz_name = quiz.get('name', 'Sans nom')
        questions = quiz.get('questions', [])

        print(f"\nQuiz: {quiz_name}")
        print(f"   Nombre de questions: {len(questions)}")

        # Dictionnaire pour compter les questions identiques
        question_count = defaultdict(list)

        for q in questions:
            question_text = q.get('question', '').strip().lower()
            question_id = q.get('id', 'N/A')
            uuid = q.get('uuid', 'N/A')

            question_count[question_text].append({
                'id': question_id,
                'uuid': uuid,
                'original': q.get('question', '')
            })

        # Trouver les doublons
        duplicates = {q: items for q, items in question_count.items() if len(items) > 1}

        if duplicates:
            print(f"   ATTENTION - DOUBLONS TROUVES: {len(duplicates)} questions en double")
            total_duplicates += len(duplicates)

            for question_text, items in list(duplicates.items())[:5]:  # Afficher max 5 exemples
                print(f"\n   Question en double ({len(items)} fois):")
                print(f"   '{items[0]['original'][:80]}...'")
                for item in items:
                    print(f"      - ID: {item['id']}, UUID: {item['uuid'][:8]}...")

            if len(duplicates) > 5:
                print(f"   ... et {len(duplicates) - 5} autres questions en double")
        else:
            print(f"   OK - Aucun doublon trouve")

        total_questions += len(questions)

    print("\n" + "=" * 80)
    print("RESUME")
    print("=" * 80)
    print(f"Nombre total de quiz: {len(data)}")
    print(f"Nombre total de questions: {total_questions}")

    if total_duplicates > 0:
        print(f"ATTENTION - TOTAL DE QUESTIONS EN DOUBLE: {total_duplicates}")
        print("\nRECOMMANDATION: Nettoyer les doublons pour ameliorer la qualite du quiz")
    else:
        print("OK - AUCUN DOUBLON TROUVE - Tous les quiz sont uniques!")

    print("=" * 80)

    return total_duplicates

if __name__ == "__main__":
    try:
        duplicates_count = check_duplicates()
        exit(0 if duplicates_count == 0 else 1)
    except FileNotFoundError:
        print("ERREUR: Fichier quiz-questions.json non trouve")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"ERREUR de parsing JSON: {e}")
        exit(1)
    except Exception as e:
        print(f"ERREUR inattendue: {e}")
        exit(1)

