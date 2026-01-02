import json
import sys

try:
    # Load the quiz file
    print("Loading quiz file...")
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ File loaded successfully")
    print(f"✓ Total quizzes: {len(data['quizzes'])}")

    # Find Disney quiz
    disney_quiz = None
    for idx, quiz in enumerate(data['quizzes']):
        if quiz['name'] == 'Disney Animation Movies':
            disney_quiz = quiz
            print(f"✓ Disney quiz found at index {idx}")
            break

    if not disney_quiz:
        print("✗ Disney quiz NOT found!")
        sys.exit(1)

    # Validate Disney quiz
    print(f"\n=== Disney Quiz Details ===")
    print(f"Name: {disney_quiz['name']}")
    print(f"Image: {disney_quiz['imageFileName']}")
    print(f"Number of questions: {len(disney_quiz['questions'])}")

    # Check structure
    errors = []

    for i, q in enumerate(disney_quiz['questions']):
        # Check required fields
        if 'id' not in q:
            errors.append(f"Question {i+1} missing 'id'")
        if 'uuid' not in q:
            errors.append(f"Question {i+1} missing 'uuid'")
        if 'question' not in q:
            errors.append(f"Question {i+1} missing 'question'")
        if 'options' not in q:
            errors.append(f"Question {i+1} missing 'options'")
        if 'answer' not in q:
            errors.append(f"Question {i+1} missing 'answer'")
        if 'difficulty_level' not in q:
            errors.append(f"Question {i+1} missing 'difficulty_level'")

        # Check ID sequence
        if 'id' in q and q['id'] != i + 1:
            errors.append(f"Question {i+1} has wrong ID: {q['id']}")

        # Check answer is in options
        if 'answer' in q and 'options' in q:
            if q['answer'] not in q['options']:
                errors.append(f"Question {i+1}: answer '{q['answer']}' not in options")

    if errors:
        print(f"\n✗ Found {len(errors)} errors:")
        for err in errors[:10]:  # Show first 10
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors)-10} more errors")
    else:
        print(f"\n✓ All questions are valid!")

    # Show sample questions
    print(f"\n=== Sample Questions ===")
    for i in [0, 1, 2, len(disney_quiz['questions'])-1]:
        q = disney_quiz['questions'][i]
        print(f"\nQ{q['id']}: {q['question'][:80]}...")
        print(f"  Options: {q['options']}")
        print(f"  Answer: {q['answer']}")
        print(f"  Difficulty: {q['difficulty_level']}")

    print(f"\n{'='*50}")
    print(f"✓ VALIDATION COMPLETE")
    print(f"✓ Disney quiz has {len(disney_quiz['questions'])} questions")
    print(f"✓ File is ready to use!")

    # Write summary to file
    with open('disney_validation_summary.txt', 'w', encoding='utf-8') as f:
        f.write(f"Disney Quiz Validation Summary\n")
        f.write(f"=" * 50 + "\n\n")
        f.write(f"Quiz Name: {disney_quiz['name']}\n")
        f.write(f"Image File: {disney_quiz['imageFileName']}\n")
        f.write(f"Total Questions: {len(disney_quiz['questions'])}\n")
        f.write(f"Errors Found: {len(errors)}\n")
        f.write(f"Status: {'FAILED' if errors else 'PASSED'}\n")

    print(f"\n✓ Summary written to disney_validation_summary.txt")

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

