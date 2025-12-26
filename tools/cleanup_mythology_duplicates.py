import json

# Charger le fichier JSON
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Nombre de quiz avant nettoyage: {len(data['quizzes'])}")

# Supprimer tous les quiz de mythologie existants
mythology_quizzes = []
other_quizzes = []

for quiz in data['quizzes']:
    if quiz['name'] == "Mythology Quiz":
        mythology_quizzes.append(quiz)
    else:
        other_quizzes.append(quiz)

print(f"Trouvé {len(mythology_quizzes)} quiz de mythologie")

# Garder seulement le dernier (le plus complet)
if mythology_quizzes:
    # Trouver celui avec le plus de questions
    best_quiz = max(mythology_quizzes, key=lambda q: len(q['questions']))
    print(f"Garder le quiz avec {len(best_quiz['questions'])} questions")
    other_quizzes.append(best_quiz)

# Reconstruire la liste
data['quizzes'] = other_quizzes

print(f"Nombre de quiz après nettoyage: {len(data['quizzes'])}")

# Sauvegarder
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Nettoyage terminé!")

