import json
import uuid
import sys

print("=== Mise à jour du quiz Classical Music Composers ===")

# Step 1: Generate all questions from the generator
print("\nÉtape 1: Génération des questions...")
exec(open('generate_classical_music_quiz.py', encoding='utf-8').read())
print(f"✓ Quiz généré avec {len(quiz['questions'])} questions")

# Step 2: Load the main quiz file
print("\nÉtape 2: Chargement du fichier principal...")
quiz_file = "C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json"
try:
    with open(quiz_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Fichier chargé: {len(data['quizzes'])} quiz trouvés")
except Exception as e:
    print(f"✗ Erreur lors du chargement: {e}")
    sys.exit(1)

# Step 3: Find and update the Classical Music quiz
print("\nÉtape 3: Recherche du quiz...")
quiz_index = None
for i, q in enumerate(data['quizzes']):
    if q['name'] == 'Classical Music Composers':
        quiz_index = i
        print(f"✓ Quiz trouvé à l'index {i}")
        print(f"  Questions actuelles: {len(q['questions'])}")
        break

if quiz_index is None:
    print("✗ Quiz 'Classical Music Composers' non trouvé!")
    sys.exit(1)

# Step 4: Replace questions
print("\nÉtape 4: Remplacement des questions...")
data['quizzes'][quiz_index]['questions'] = quiz['questions']
print(f"✓ {len(quiz['questions'])} questions ajoutées")

# Step 5: Save file
print("\nÉtape 5: Sauvegarde du fichier...")
try:
    with open(quiz_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✓ Fichier sauvegardé avec succès!")
except Exception as e:
    print(f"✗ Erreur lors de la sauvegarde: {e}")
    sys.exit(1)

print("\n=== Mise à jour terminée avec succès! ===")
print(f"Le quiz 'Classical Music Composers' contient maintenant {len(quiz['questions'])} questions")

