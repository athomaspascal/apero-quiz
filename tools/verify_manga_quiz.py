import json

# Charger le fichier quiz
quiz_file = r'C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions.json'

print("Vérification du quiz manga...")
with open(quiz_file, 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# Trouver le quiz manga
manga_quiz = None
for quiz in quiz_data['quizzes']:
    if 'manga' in quiz['name'].lower():
        manga_quiz = quiz
        break

if manga_quiz:
    print(f"\n✓ Quiz trouvé: {manga_quiz['name']}")
    print(f"✓ Image: {manga_quiz['imageFileName']}")
    print(f"✓ Nombre de questions: {len(manga_quiz['questions'])}")

    # Vérifier quelques questions
    print("\n--- Exemples de questions ---")
    for i in [0, 10, 100, 500]:
        if i < len(manga_quiz['questions']):
            q = manga_quiz['questions'][i]
            print(f"\nQuestion {q['id']}:")
            print(f"  UUID: {q['uuid']}")
            print(f"  Question: {q['question'][:80]}...")
            print(f"  Difficulté: {q['difficulty_level']}")
            print(f"  Options: {len(q['options'])}")
            print(f"  Réponse: {q['answer']}")

    # Vérifier les attributs obligatoires
    print("\n--- Vérification des attributs ---")
    errors = []
    for i, question in enumerate(manga_quiz['questions']):
        if 'id' not in question:
            errors.append(f"Question {i}: 'id' manquant")
        if 'uuid' not in question:
            errors.append(f"Question {i}: 'uuid' manquant")
        if 'question' not in question:
            errors.append(f"Question {i}: 'question' manquant")
        if 'difficulty_level' not in question:
            errors.append(f"Question {i}: 'difficulty_level' manquant")
        if 'options' not in question:
            errors.append(f"Question {i}: 'options' manquant")
        if 'answer' not in question:
            errors.append(f"Question {i}: 'answer' manquant")

        # Vérifier que la réponse est dans les options
        if 'answer' in question and 'options' in question:
            if question['answer'] not in question['options']:
                errors.append(f"Question {question['id']}: La réponse '{question['answer']}' n'est pas dans les options")

    if errors:
        print(f"\n❌ {len(errors)} erreurs trouvées:")
        for error in errors[:10]:  # Afficher seulement les 10 premières
            print(f"  - {error}")
    else:
        print("\n✓ Tous les attributs obligatoires sont présents!")
        print("✓ Toutes les réponses sont valides!")

    # Vérifier les thèmes et types
    print("\n--- Vérification des questions sur le thème et le type ---")
    theme_questions = [q for q in manga_quiz['questions'] if 'thème' in q['question'].lower()]
    type_questions = [q for q in manga_quiz['questions'] if 'type' in q['question'].lower()]

    print(f"✓ Questions sur le thème: {len(theme_questions)}")
    print(f"✓ Questions sur le type: {len(type_questions)}")

    if theme_questions:
        print("\nExemple de question sur le thème:")
        q = theme_questions[0]
        print(f"  {q['question']}")
        print(f"  Réponse: {q['answer']}")

    if type_questions:
        print("\nExemple de question sur le type:")
        q = type_questions[0]
        print(f"  {q['question']}")
        print(f"  Réponse: {q['answer']}")

else:
    print("❌ Quiz manga non trouvé!")

print("\n--- Liste de tous les quiz ---")
for i, quiz in enumerate(quiz_data['quizzes'], 1):
    print(f"{i}. {quiz['name']} ({len(quiz['questions'])} questions)")

