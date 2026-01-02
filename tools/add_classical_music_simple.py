import json
import uuid

print("Génération du quiz de musique classique...")

# Génération du quiz
quiz = {
    "name": "Classical Music Composers",
    "imageFileName": "classical-music.svg",
    "questions": []
}

questions_data = [
    # Mozart
    ("What is Wolfgang Amadeus Mozart's birth year?", ["1756", "1770", "1750", "1760"], "1756", 1),
    ("In which city was Mozart born?", ["Salzburg", "Vienna", "Prague", "Munich"], "Salzburg", 1),
    ("What was Mozart's full name?", ["Wolfgang Amadeus Mozart", "Johann Sebastian Mozart", "Ludwig Wolfgang Mozart", "Franz Wolfgang Mozart"], "Wolfgang Amadeus Mozart", 2),
    ("At what age did Mozart compose his first piece?", ["5", "8", "10", "12"], "5", 2),
    ("What year did Mozart die?", ["1791", "1800", "1785", "1795"], "1791", 1),
    ("How many symphonies did Mozart compose?", ["41", "50", "35", "60"], "41", 3),
    ("What is Mozart's most famous opera?", ["The Magic Flute", "Carmen", "La Traviata", "Aida"], "The Magic Flute", 2),
    ("Who was Mozart's main rival in Vienna?", ["Antonio Salieri", "Joseph Haydn", "Ludwig van Beethoven", "Franz Schubert"], "Antonio Salieri", 2),
    ("What was Mozart's Requiem Mass commissioned for?", ["His own funeral", "A wealthy patron", "The Emperor", "A church"], "A wealthy patron", 3),
    ("In which language are most of Mozart's operas?", ["Italian", "German", "French", "Latin"], "Italian", 2),

    # Beethoven
    ("What year was Ludwig van Beethoven born?", ["1770", "1756", "1780", "1765"], "1770", 1),
    ("In which city was Beethoven born?", ["Bonn", "Vienna", "Leipzig", "Berlin"], "Bonn", 1),
    ("How many symphonies did Beethoven compose?", ["9", "12", "7", "15"], "9", 1),
    ("Which symphony is known as the 'Choral Symphony'?", ["Symphony No. 9", "Symphony No. 5", "Symphony No. 3", "Symphony No. 6"], "Symphony No. 9", 2),
    ("What major affliction did Beethoven suffer from?", ["Deafness", "Blindness", "Paralysis", "Tuberculosis"], "Deafness", 1),
    ("What is the nickname of Beethoven's Symphony No. 6?", ["Pastoral", "Heroic", "Fate", "Romantic"], "Pastoral", 2),
    ("What year did Beethoven die?", ["1827", "1830", "1820", "1835"], "1827", 1),
    ("Which symphony is dedicated to Napoleon?", ["Symphony No. 3 (Eroica)", "Symphony No. 5", "Symphony No. 9", "Symphony No. 7"], "Symphony No. 3 (Eroica)", 3),
    ("What is Beethoven's only opera?", ["Fidelio", "Don Giovanni", "The Magic Flute", "Carmen"], "Fidelio", 2),
    ("Who was Beethoven's teacher in Vienna?", ["Joseph Haydn", "Antonio Salieri", "Wolfgang Amadeus Mozart", "Franz Schubert"], "Joseph Haydn", 3),
]

# Convert to quiz format
question_id = 1
for q_text, options, answer, difficulty in questions_data:
    question = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q_text,
        "difficulty_level": difficulty,
        "options": options,
        "answer": answer
    }
    quiz["questions"].append(question)
    question_id += 1

print(f"Nombre de questions générées: {len(quiz['questions'])}")

# Load existing quiz file
quiz_file = "C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json"
try:
    with open(quiz_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Fichier quiz-questions.json chargé: {len(data['quizzes'])} quiz existants")
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    exit(1)

# Check if quiz already exists
quiz_names = [q['name'] for q in data['quizzes']]
if quiz['name'] in quiz_names:
    print(f"Le quiz '{quiz['name']}' existe déjà!")
    exit(0)

# Add quiz
data['quizzes'].append(quiz)
print(f"Quiz ajouté. Nouveau total: {len(data['quizzes'])} quiz")

# Save file
try:
    with open(quiz_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Fichier sauvegardé avec succès!")
except Exception as e:
    print(f"Erreur lors de la sauvegarde: {e}")
    exit(1)

