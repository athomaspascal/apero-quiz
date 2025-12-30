import json
import shutil
from datetime import datetime

# Chemins
quiz_file = r'C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions.json'
manga_temp_file = r'C:\Users\athom\IdeaProjects\quizz1\manga_quiz_temp.json'

# Créer une sauvegarde avec timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = rf'C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions-backup-{timestamp}.json'

print(f"Création de la sauvegarde: {backup_file}")
shutil.copy(quiz_file, backup_file)
print("Sauvegarde créée avec succès!")

# Charger le fichier quiz existant
print("\nChargement du fichier quiz existant...")
with open(quiz_file, 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

print(f"Nombre de quiz existants: {len(quiz_data['quizzes'])}")

# Charger le nouveau quiz manga
print("\nChargement du quiz manga...")
with open(manga_temp_file, 'r', encoding='utf-8') as f:
    manga_quiz = json.load(f)

print(f"Quiz manga: {manga_quiz['name']}")
print(f"Nombre de questions: {len(manga_quiz['questions'])}")

# Vérifier si un quiz manga existe déjà
existing_manga = None
for i, quiz in enumerate(quiz_data['quizzes']):
    if 'manga' in quiz['name'].lower():
        existing_manga = i
        break

if existing_manga is not None:
    print(f"\nRemplacement du quiz manga existant à l'index {existing_manga}")
    quiz_data['quizzes'][existing_manga] = manga_quiz
else:
    print("\nAjout du nouveau quiz manga")
    quiz_data['quizzes'].append(manga_quiz)

# Sauvegarder le fichier mis à jour
print(f"\nSauvegarde du fichier quiz mis à jour...")
with open(quiz_file, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Quiz manga ajouté avec succès!")
print(f"✓ Nombre total de quiz: {len(quiz_data['quizzes'])}")
print(f"✓ Nombre de questions dans le quiz manga: {len(manga_quiz['questions'])}")

