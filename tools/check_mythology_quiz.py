import json

# Charger le fichier JSON
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Nombre total de quiz: {len(data['quizzes'])}")
print("\nListe des quiz:")
for i, quiz in enumerate(data['quizzes'], 1):
    print(f"{i}. {quiz['name']} - {len(quiz['questions'])} questions")

# Vérifier le quiz de mythologie
mythology_quiz = None
for quiz in data['quizzes']:
    if quiz['name'] == "Mythology Quiz":
        mythology_quiz = quiz
        break

if mythology_quiz:
    print(f"\n=== Quiz de Mythologie ===")
    print(f"Nom: {mythology_quiz['name']}")
    print(f"Image: {mythology_quiz['imageFileName']}")
    print(f"Nombre de questions: {len(mythology_quiz['questions'])}")

    # Vérifier que toutes les questions ont un ID
    missing_ids = []
    for q in mythology_quiz['questions']:
        if 'id' not in q:
            missing_ids.append(q.get('question', 'Question sans texte'))

    if missing_ids:
        print(f"\n⚠ {len(missing_ids)} questions sans ID:")
        for q in missing_ids[:5]:
            print(f"  - {q[:50]}...")
    else:
        print("\n✓ Toutes les questions ont un ID")

    # Afficher quelques questions
    print("\n=== Premières questions ===")
    for q in mythology_quiz['questions'][:5]:
        print(f"\nID {q['id']}: {q['question']}")
        print(f"  UUID: {q['uuid'][:8]}...")
        print(f"  Réponse: {q['answer']}")
else:
    print("\n⚠ Quiz de mythologie non trouvé!")

