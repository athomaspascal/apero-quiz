import json
import os

print("Debut du script...")

file_path = r'src\main\resources\quiz-questions.json'
print(f"Chemin: {file_path}")
print(f"Existe: {os.path.exists(file_path)}")

if os.path.exists(file_path):
    print("Chargement du fichier JSON...")
    with open(file_path, 'r', encoding='utf-8') as f:
        root = json.load(f)

    # Gerer les deux structures possibles
    if isinstance(root, dict) and 'quizzes' in root:
        data = root['quizzes']
        print("Structure: {quizzes: [...]}")
    elif isinstance(root, list):
        data = root
        print("Structure: [...]")
    else:
        print("ERREUR: Structure JSON inconnue!")
        data = []

    print(f"Nombre de quiz: {len(data)}")

    total_questions = 0
    total_duplicates = 0

    for quiz in data:
        quiz_name = quiz.get('name', 'Sans nom')
        questions = quiz.get('questions', [])

        print(f"\nQuiz: {quiz_name}")
        print(f"  Questions: {len(questions)}")

        # Compter les doublons
        question_texts = []
        for q in questions:
            question_text = q.get('question', '').strip().lower()
            question_texts.append(question_text)

        # Trouver les doublons
        unique_questions = set(question_texts)
        duplicates = len(question_texts) - len(unique_questions)

        if duplicates > 0:
            print(f"  ATTENTION: {duplicates} doublons detectes!")
            total_duplicates += duplicates
        else:
            print(f"  OK: Aucun doublon")

        total_questions += len(questions)

    print(f"\n{'='*60}")
    print(f"TOTAL: {len(data)} quiz, {total_questions} questions")
    if total_duplicates > 0:
        print(f"ATTENTION: {total_duplicates} doublons au total!")
    else:
        print("OK: Aucun doublon trouve!")
    print(f"{'='*60}")
else:
    print("ERREUR: Fichier non trouve!")

