import json
import uuid

# Load existing quiz file
quiz_file = "C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json"
with open(quiz_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the Classical Music Composers quiz
quiz_index = None
for i, quiz in enumerate(data['quizzes']):
    if quiz['name'] == 'Classical Music Composers':
        quiz_index = i
        break

if quiz_index is None:
    print("Quiz 'Classical Music Composers' non trouvé!")
    exit(1)

print(f"Quiz trouvé à l'index {quiz_index}")
print(f"Nombre de questions actuelles: {len(data['quizzes'][quiz_index]['questions'])}")

# Generate all 510+ questions
all_questions = []
question_id = 1

# Import questions from the complete generator
import subprocess
import sys

# Run the generator script and capture output
print("Génération de toutes les questions depuis generate_classical_music_quiz.py...")
result = subprocess.run(
    [sys.executable, 'generate_classical_music_quiz.py'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    cwd='C:/Users/athom/IdeaProjects/quizz1/tools'
)

if result.returncode != 0:
    print(f"Erreur lors de la génération: {result.stderr}")
    exit(1)

# Parse the JSON output
import json as json_module
try:
    generated_quiz = json_module.loads(result.stdout)
    questions_data_full = []

    # Extract question data from generated quiz
    for q in generated_quiz['questions']:
        questions_data_full.append((
            q['question'],
            q['options'],
            q['answer'],
            q['difficulty_level']
        ))

    print(f"✓ {len(questions_data_full)} questions chargées depuis le générateur")
except Exception as e:
    print(f"Erreur lors du parsing: {e}")
    exit(1)

# Replace the questions
for q_text, options, answer, difficulty in questions_data_full:
    question = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q_text,
        "difficulty_level": difficulty,
        "options": options,
        "answer": answer
    }
    all_questions.append(question)
    question_id += 1

# Update the quiz
data['quizzes'][quiz_index]['questions'] = all_questions

print(f"Mise à jour du quiz avec {len(all_questions)} questions")

# Save file
with open(quiz_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Fichier sauvegardé avec succès!")

