"""
Script to validate quiz-questions.json against the JSON schema
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, Draft7Validator
except ImportError:
    print("Error: jsonschema module not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])
    import jsonschema
    from jsonschema import validate, Draft7Validator


def validate_quiz_json(json_file_path, schema_file_path):
    """
    Validate a quiz JSON file against the schema
    """
    print(f"Validating: {json_file_path}")
    print(f"Using schema: {schema_file_path}")
    print("-" * 80)

    # Load the schema
    try:
        with open(schema_file_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        print("✓ Schema loaded successfully")
    except Exception as e:
        print(f"✗ Error loading schema: {e}")
        return False

    # Load the JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ JSON file loaded successfully")
    except Exception as e:
        print(f"✗ Error loading JSON file: {e}")
        return False

    # Validate
    try:
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))

        if not errors:
            print("✓ Validation successful!")
            print("-" * 80)

            # Print statistics
            num_quizzes = len(data.get('quizzes', []))
            total_questions = sum(len(quiz.get('questions', [])) for quiz in data.get('quizzes', []))

            print(f"\nStatistics:")
            print(f"  - Total quizzes: {num_quizzes}")
            print(f"  - Total questions: {total_questions}")

            # List all quizzes
            print(f"\nQuiz names:")
            for i, quiz in enumerate(data.get('quizzes', []), 1):
                quiz_name = quiz.get('name', 'Unknown')
                num_q = len(quiz.get('questions', []))
                img_file = quiz.get('imageFileName', 'N/A')
                print(f"  {i}. {quiz_name} ({num_q} questions) - Image: {img_file}")

            return True
        else:
            print(f"✗ Validation failed with {len(errors)} error(s):")
            print("-" * 80)

            for i, error in enumerate(errors[:10], 1):  # Show first 10 errors
                path = " -> ".join(str(p) for p in error.path)
                print(f"\nError {i}:")
                print(f"  Path: {path if path else 'root'}")
                print(f"  Message: {error.message}")
                if error.validator:
                    print(f"  Validator: {error.validator}")

            if len(errors) > 10:
                print(f"\n... and {len(errors) - 10} more error(s)")

            return False

    except Exception as e:
        print(f"✗ Unexpected error during validation: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_answer_in_options(json_file_path):
    """
    Additional validation: Check that each answer is in the options list
    """
    print("\n" + "=" * 80)
    print("Additional validation: Checking answers match options...")
    print("=" * 80)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        errors = []
        for quiz_idx, quiz in enumerate(data.get('quizzes', [])):
            quiz_name = quiz.get('name', f'Quiz {quiz_idx + 1}')
            for q_idx, question in enumerate(quiz.get('questions', [])):
                answer = question.get('answer')
                options = question.get('options', [])
                q_id = question.get('id', 'N/A')

                if answer not in options:
                    errors.append({
                        'quiz': quiz_name,
                        'question_id': q_id,
                        'question': question.get('question', 'N/A')[:60] + '...',
                        'answer': answer,
                        'options': options
                    })

        if not errors:
            print("✓ All answers are valid (found in their options)")
            return True
        else:
            print(f"✗ Found {len(errors)} question(s) where answer is not in options:")
            for i, err in enumerate(errors[:5], 1):
                print(f"\n{i}. Quiz: {err['quiz']}")
                print(f"   Question ID: {err['question_id']}")
                print(f"   Question: {err['question']}")
                print(f"   Answer: '{err['answer']}'")
                print(f"   Options: {err['options']}")

            if len(errors) > 5:
                print(f"\n... and {len(errors) - 5} more error(s)")

            return False

    except Exception as e:
        print(f"✗ Error during answer validation: {e}")
        return False


def check_unique_uuids(json_file_path):
    """
    Additional validation: Check that all UUIDs are unique across all quizzes
    """
    print("\n" + "=" * 80)
    print("Additional validation: Checking UUID uniqueness...")
    print("=" * 80)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        uuid_map = {}
        duplicates = []

        for quiz_idx, quiz in enumerate(data.get('quizzes', [])):
            quiz_name = quiz.get('name', f'Quiz {quiz_idx + 1}')
            for q_idx, question in enumerate(quiz.get('questions', [])):
                uuid = question.get('uuid')
                q_id = question.get('id', 'N/A')

                if uuid:
                    if uuid in uuid_map:
                        duplicates.append({
                            'uuid': uuid,
                            'first': uuid_map[uuid],
                            'second': {
                                'quiz': quiz_name,
                                'question_id': q_id,
                                'question': question.get('question', 'N/A')[:60] + '...'
                            }
                        })
                    else:
                        uuid_map[uuid] = {
                            'quiz': quiz_name,
                            'question_id': q_id,
                            'question': question.get('question', 'N/A')[:60] + '...'
                        }

        if not duplicates:
            print(f"✓ All {len(uuid_map)} UUIDs are unique")
            return True
        else:
            print(f"✗ Found {len(duplicates)} duplicate UUID(s):")
            for i, dup in enumerate(duplicates[:5], 1):
                print(f"\n{i}. UUID: {dup['uuid']}")
                print(f"   First occurrence: {dup['first']['quiz']} - Q{dup['first']['question_id']}")
                print(f"   Duplicate in: {dup['second']['quiz']} - Q{dup['second']['question_id']}")

            if len(duplicates) > 5:
                print(f"\n... and {len(duplicates) - 5} more duplicate(s)")

            return False

    except Exception as e:
        print(f"✗ Error during UUID validation: {e}")
        return False


if __name__ == "__main__":
    # Determine file paths
    script_dir = Path(__file__).parent
    resources_dir = script_dir / "src" / "main" / "resources"

    json_file = resources_dir / "quiz-questions.json"
    schema_file = resources_dir / "quiz-questions-schema.json"

    # Check if files exist
    if not json_file.exists():
        print(f"Error: JSON file not found: {json_file}")
        sys.exit(1)

    if not schema_file.exists():
        print(f"Error: Schema file not found: {schema_file}")
        sys.exit(1)

    # Validate
    print("=" * 80)
    print("QUIZ JSON VALIDATION")
    print("=" * 80)
    print()

    is_valid = validate_quiz_json(json_file, schema_file)
    answers_valid = check_answer_in_options(json_file)
    uuids_unique = check_unique_uuids(json_file)

    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Schema validation: {'✓ PASS' if is_valid else '✗ FAIL'}")
    print(f"Answer validation: {'✓ PASS' if answers_valid else '✗ FAIL'}")
    print(f"UUID uniqueness:   {'✓ PASS' if uuids_unique else '✗ FAIL'}")
    print("=" * 80)

    if is_valid and answers_valid and uuids_unique:
        print("\n✓ All validations passed!")
        sys.exit(0)
    else:
        print("\n✗ Some validations failed. Please check the errors above.")
        sys.exit(1)

