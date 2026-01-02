import json
import sys

# Read the existing quiz-questions.json
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Read the generated classical music quiz
import subprocess
result = subprocess.run(['python', 'generate_classical_music_quiz.py'],
                       capture_output=True, text=True, encoding='utf-8')
classical_quiz = json.loads(result.stdout)

print(f"Classical Music Quiz has {len(classical_quiz['questions'])} questions")

# Add the quiz to the data
data['quizzes'].append(classical_quiz)

# Write back to the file
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Quiz added successfully! Total quizzes: {len(data['quizzes'])}")

