import json

with open('src/main/resources/quiz-questions.json', encoding='utf-8') as f:
    data = json.load(f)

print('Total quizzes:', len(data['quizzes']))
q1 = data['quizzes'][0]['questions'][0]
print('First question keys:', list(q1.keys()))
print('Has difficulty_level:', 'difficulty_level' in q1)
print('Sample question:', json.dumps(q1, indent=2, ensure_ascii=False)[:500])

