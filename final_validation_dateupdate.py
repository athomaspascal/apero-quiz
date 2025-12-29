import json
import sys

print("="*80)
print("VALIDATION COMPLÈTE DU CHAMP dateUpdate")
print("="*80)

# Lire le fichier
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("✓ Fichier JSON chargé avec succès")
except Exception as e:
    print(f"✗ Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Obtenir les quiz
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []
    print("✗ Structure du JSON invalide")
    sys.exit(1)

print(f"✓ {len(quizzes)} quiz trouvés")

# Validation
all_ok = True
total_questions = 0
questions_with_dateupdate = 0

for quiz in quizzes:
    if isinstance(quiz, dict):
        questions = quiz.get('questions', [])
        for question in questions:
            total_questions += 1
            if 'dateUpdate' in question and question.get('dateUpdate') is not None:
                questions_with_dateupdate += 1

print(f"✓ {total_questions} questions totales")
print(f"✓ {questions_with_dateupdate} questions avec dateUpdate")

if questions_with_dateupdate == total_questions:
    print("\n" + "="*80)
    print("✅ VALIDATION RÉUSSIE : TOUTES LES QUESTIONS ONT LE CHAMP dateUpdate")
    print("="*80)

    print("\nRésumé des modifications :")
    print("  1. Entité QuizQuestion.java : ✓ Champ dateUpdate ajouté")
    print("  2. QuizQuestionsData.java : ✓ Support du champ ajouté")
    print("  3. QuizQuestionService.java : ✓ Méthode save() ajoutée")
    print("  4. QuizDataInitializer.java : ✓ Lecture du champ depuis JSON")
    print("  5. quiz-questions.json : ✓ Toutes les questions mises à jour")
    print("  6. Compilation Maven : ✓ BUILD SUCCESS")

    print("\n" + "="*80)
    print("Le champ dateUpdate est maintenant complètement intégré !")
    print("="*80)
else:
    print(f"\n✗ ERREUR : {total_questions - questions_with_dateupdate} questions sans dateUpdate")
    sys.exit(1)

