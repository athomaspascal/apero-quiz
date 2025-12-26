import json

# Charger le fichier JSON
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("LISTE COMPLÈTE DES QUIZ DISPONIBLES")
print("=" * 80)
print(f"\nNombre total de quiz: {len(data['quizzes'])}")
print(f"Nombre total de questions: {sum(len(q['questions']) for q in data['quizzes'])}")
print("\n" + "-" * 80)

for i, quiz in enumerate(data['quizzes'], 1):
    print(f"\n{i:2d}. {quiz['name']}")
    print(f"    📊 Questions: {len(quiz['questions'])}")
    print(f"    🖼️  Image: {quiz.get('imageFileName', 'N/A')}")

    # Afficher un aperçu de quelques thèmes
    if len(quiz['questions']) > 0:
        first_q = quiz['questions'][0]['question']
        print(f"    📝 Exemple: {first_q[:60]}{'...' if len(first_q) > 60 else ''}")

print("\n" + "=" * 80)
print("✅ Tous les quiz sont prêts à être utilisés!")
print("=" * 80)

