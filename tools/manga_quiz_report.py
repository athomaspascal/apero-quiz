import json

quiz_file = r'C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions.json'

with open(quiz_file, 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# Trouver le quiz manga
manga_quiz = None
for quiz in quiz_data['quizzes']:
    if 'Famous Manga Series' in quiz['name']:
        manga_quiz = quiz
        break

if manga_quiz:
    print("=" * 80)
    print("QUIZ MANGA - RÉSUMÉ COMPLET")
    print("=" * 80)
    print(f"\nNom du quiz: {manga_quiz['name']}")
    print(f"Image: {manga_quiz['imageFileName']}")
    print(f"Nombre total de questions: {len(manga_quiz['questions'])}")

    # Analyser les questions par catégorie
    categories = {
        'auteur': 0,
        'personnage': 0,
        'date': 0,
        'volumes': 0,
        'terminé': 0,
        'thème': 0,
        'type': 0,
        'autres': 0
    }

    for q in manga_quiz['questions']:
        question_lower = q['question'].lower()
        if 'auteur' in question_lower or 'créé' in question_lower:
            categories['auteur'] += 1
        elif 'personnage' in question_lower:
            categories['personnage'] += 1
        elif 'année' in question_lower or 'publié' in question_lower or 'décennie' in question_lower:
            categories['date'] += 1
        elif 'volume' in question_lower or 'combien' in question_lower:
            categories['volumes'] += 1
        elif 'terminé' in question_lower or 'en cours' in question_lower:
            categories['terminé'] += 1
        elif 'thème' in question_lower:
            categories['thème'] += 1
        elif 'type' in question_lower:
            categories['type'] += 1
        else:
            categories['autres'] += 1

    print("\n" + "=" * 80)
    print("RÉPARTITION DES QUESTIONS PAR CATÉGORIE")
    print("=" * 80)
    for category, count in categories.items():
        percentage = (count / len(manga_quiz['questions'])) * 100
        print(f"{category.capitalize():15} : {count:4} questions ({percentage:5.1f}%)")

    print("\n" + "=" * 80)
    print("EXEMPLES DE QUESTIONS")
    print("=" * 80)

    # Afficher des exemples pour chaque catégorie
    examples = {
        'Auteur': None,
        'Personnage': None,
        'Date de publication': None,
        'Nombre de volumes': None,
        'Série terminée': None,
        'Thème du manga': None,
        'Type de manga': None
    }

    for q in manga_quiz['questions']:
        question_lower = q['question'].lower()
        if not examples['Auteur'] and 'auteur' in question_lower:
            examples['Auteur'] = q
        elif not examples['Personnage'] and 'personnage' in question_lower:
            examples['Personnage'] = q
        elif not examples['Date de publication'] and 'année' in question_lower and 'publié' in question_lower:
            examples['Date de publication'] = q
        elif not examples['Nombre de volumes'] and 'combien de volumes' in question_lower:
            examples['Nombre de volumes'] = q
        elif not examples['Série terminée'] and 'terminé' in question_lower:
            examples['Série terminée'] = q
        elif not examples['Thème du manga'] and 'thème principal' in question_lower:
            examples['Thème du manga'] = q
        elif not examples['Type de manga'] and 'type du manga' in question_lower:
            examples['Type de manga'] = q

    for category, question in examples.items():
        if question:
            print(f"\n{category}:")
            print(f"  Q: {question['question']}")
            print(f"  Options: {', '.join(question['options'])}")
            print(f"  Réponse: {question['answer']}")
            print(f"  Difficulté: {question['difficulty_level']}/10")

    # Analyser les niveaux de difficulté
    print("\n" + "=" * 80)
    print("RÉPARTITION PAR NIVEAU DE DIFFICULTÉ")
    print("=" * 80)

    difficulty_counts = {}
    for q in manga_quiz['questions']:
        level = q['difficulty_level']
        difficulty_counts[level] = difficulty_counts.get(level, 0) + 1

    for level in sorted(difficulty_counts.keys()):
        count = difficulty_counts[level]
        percentage = (count / len(manga_quiz['questions'])) * 100
        bars = '█' * int(percentage / 2)
        print(f"Niveau {level}: {bars} {count:4} questions ({percentage:5.1f}%)")

    print("\n" + "=" * 80)
    print("✓ Quiz manga généré avec succès!")
    print("✓ Le quiz contient des questions sur:")
    print("  - Les auteurs de manga")
    print("  - Les personnages principaux")
    print("  - Les dates de publication")
    print("  - Le nombre de volumes")
    print("  - L'état de la série (terminée ou en cours)")
    print("  - Les thèmes des mangas")
    print("  - Les types de manga (Shōnen, Seinen, Shōjo, etc.)")
    print("=" * 80)

