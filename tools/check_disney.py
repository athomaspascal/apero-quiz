import json

with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Disney quiz
disney_quiz = None
for quiz in data['quizzes']:
    if quiz['name'] == 'Disney Animation Movies':
        disney_quiz = quiz
        break

if disney_quiz:
    print(f"Disney quiz found!")
    print(f"Name: {disney_quiz['name']}")
    print(f"Image: {disney_quiz['imageFileName']}")
    print(f"Number of questions: {len(disney_quiz['questions'])}")
    print(f"\nFirst 5 questions:")
    for i, q in enumerate(disney_quiz['questions'][:5], 1):
        print(f"\n{i}. Q{q['id']}: {q['question']}")
        print(f"   Options: {q['options']}")
        print(f"   Answer: {q['answer']}")
        print(f"   Difficulty: {q['difficulty_level']}")

    print(f"\nLast question:")
    last = disney_quiz['questions'][-1]
    print(f"Q{last['id']}: {last['question']}")
    print(f"Options: {last['options']}")
    print(f"Answer: {last['answer']}")

    # Check for duplicates
    ids = [q['id'] for q in disney_quiz['questions']]
    if len(ids) != len(set(ids)):
        print("\nWARNING: Duplicate IDs found!")
    else:
        print("\n✓ All IDs are unique")

    # Check UUIDs
    uuids = [q['uuid'] for q in disney_quiz['questions']]
    if len(uuids) != len(set(uuids)):
        print("WARNING: Duplicate UUIDs found!")
    else:
        print("✓ All UUIDs are unique")

else:
    print("Disney quiz NOT found!")

print(f"\nTotal quizzes in file: {len(data['quizzes'])}")

