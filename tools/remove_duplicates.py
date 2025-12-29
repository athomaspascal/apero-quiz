import json
import os
from datetime import datetime
from collections import OrderedDict

def remove_duplicates():
    """Nettoie les doublons du fichier quiz-questions.json"""

    file_path = r'src\main\resources\quiz-questions.json'

    if not os.path.exists(file_path):
        print(f"ERREUR: Fichier non trouve: {file_path}")
        return

    # Faire une sauvegarde
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = f'quiz-questions-backup-{timestamp}.json'

    print(f"Creation de la sauvegarde: {backup_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Charger le fichier JSON
    print("Chargement du fichier JSON...")
    with open(file_path, 'r', encoding='utf-8') as f:
        root = json.load(f)

    # Gerer la structure
    if isinstance(root, dict) and 'quizzes' in root:
        data = root['quizzes']
    elif isinstance(root, list):
        data = root
    else:
        print("ERREUR: Structure JSON inconnue!")
        return

    print(f"\nNombre de quiz: {len(data)}\n")

    total_before = 0
    total_after = 0
    total_removed = 0

    for quiz in data:
        quiz_name = quiz.get('name', 'Sans nom')
        questions = quiz.get('questions', [])

        original_count = len(questions)
        total_before += original_count

        print(f"Quiz: {quiz_name}")
        print(f"  Questions originales: {original_count}")

        # Nettoyer les doublons en gardant la premiere occurrence
        seen = OrderedDict()
        unique_questions = []

        for q in questions:
            question_text = q.get('question', '').strip().lower()
            if question_text not in seen:
                seen[question_text] = True
                unique_questions.append(q)

        new_count = len(unique_questions)
        removed = original_count - new_count

        if removed > 0:
            print(f"  NETTOYAGE: {removed} doublons supprimes")
            quiz['questions'] = unique_questions
            total_removed += removed

            # Reassigner les IDs pour maintenir la sequence
            for idx, q in enumerate(unique_questions, 1):
                q['id'] = idx

            print(f"  Questions restantes: {new_count}")
        else:
            print(f"  OK: Aucun doublon")

        total_after += new_count

    print(f"\n{'='*60}")
    print(f"RESUME")
    print(f"{'='*60}")
    print(f"Questions avant nettoyage: {total_before}")
    print(f"Questions apres nettoyage: {total_after}")
    print(f"Total doublons supprimes: {total_removed}")
    print(f"{'='*60}")

    if total_removed > 0:
        # Sauvegarder le fichier nettoye
        print(f"\nEnregistrement du fichier nettoye...")

        if isinstance(root, dict) and 'quizzes' in root:
            root['quizzes'] = data
            output = root
        else:
            output = data

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"OK: Fichier nettoye enregistre!")
        print(f"Sauvegarde disponible: {backup_path}")
    else:
        print("\nAucun nettoyage necessaire.")

if __name__ == "__main__":
    try:
        remove_duplicates()
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()

