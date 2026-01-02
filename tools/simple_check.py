import json

log = open('validation_log.txt', 'w', encoding='utf-8')

def log_print(msg):
    log.write(msg + '\n')
    log.flush()

try:
    log_print("Starting validation...")

    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    log_print(f"Total quizzes: {len(data['quizzes'])}")

    # List all quizzes
    log_print("\nAll quizzes:")
    for i, quiz in enumerate(data['quizzes']):
        log_print(f"{i+1}. {quiz['name']} - {len(quiz['questions'])} questions")

    # Find Disney
    disney = None
    for quiz in data['quizzes']:
        if 'Disney' in quiz['name']:
            disney = quiz
            break

    if disney:
        log_print(f"\nDisney quiz found!")
        log_print(f"Name: {disney['name']}")
        log_print(f"Image: {disney['imageFileName']}")
        log_print(f"Questions: {len(disney['questions'])}")

        log_print(f"\nFirst question:")
        q = disney['questions'][0]
        log_print(f"ID: {q['id']}")
        log_print(f"Question: {q['question']}")
        log_print(f"Options: {q['options']}")
        log_print(f"Answer: {q['answer']}")
        log_print(f"Difficulty: {q['difficulty_level']}")

        log_print(f"\nLast question:")
        q = disney['questions'][-1]
        log_print(f"ID: {q['id']}")
        log_print(f"Question: {q['question']}")
        log_print(f"Options: {q['options']}")
        log_print(f"Answer: {q['answer']}")
    else:
        log_print("\nDisney quiz NOT found!")

    log_print("\nValidation complete!")

except Exception as e:
    log_print(f"\nERROR: {str(e)}")
    import traceback
    log_print(traceback.format_exc())

log.close()
print("Done - check validation_log.txt")

