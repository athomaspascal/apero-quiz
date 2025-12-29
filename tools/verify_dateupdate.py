import json
import sys

# Lire le fichier
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Obtenir les quiz
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

print("="*60)
print("VÉRIFICATION DU CHAMP dateUpdate")
print("="*60)

total_questions = 0
questions_with_dateupdate = 0
questions_without_dateupdate = []

for quiz in quizzes:
    if isinstance(quiz, dict):
        quiz_name = quiz.get('name', 'Sans nom')
        questions = quiz.get('questions', [])

        for i, question in enumerate(questions):
            total_questions += 1
            if 'dateUpdate' in question and question.get('dateUpdate') is not None:
                questions_with_dateupdate += 1
            else:
                questions_without_dateupdate.append(f"{quiz_name} - Question {i+1}")

print(f"\nQuestions totales: {total_questions}")
print(f"Questions avec dateUpdate: {questions_with_dateupdate}")
print(f"Questions sans dateUpdate: {len(questions_without_dateupdate)}")

if questions_without_dateupdate:
    print("\n⚠ Questions manquantes (premières 10):")
    for q in questions_without_dateupdate[:10]:
        print(f"  - {q}")
else:
    print("\n✓ Toutes les questions ont le champ dateUpdate!")

print("\n" + "="*60)
print("EXEMPLE DE QUESTIONS AVEC dateUpdate")
print("="*60)

# Afficher quelques exemples
count = 0
for quiz in quizzes:
    if isinstance(quiz, dict) and count < 3:
        quiz_name = quiz.get('name', 'Sans nom')
        questions = quiz.get('questions', [])

        if questions:
            print(f"\nQuiz: {quiz_name}")
            q = questions[0]
            print(f"  Question: {q.get('question', '')[:60]}...")
            print(f"  dateUpdate: {q.get('dateUpdate', 'N/A')}")
            count += 1

print("\n" + "="*60)

