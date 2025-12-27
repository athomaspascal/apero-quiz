"""
Script to fix UUID issues in quiz-questions.json
- Replace invalid UUID formats with valid UUID v4
- Replace duplicate UUIDs with new unique UUIDs
"""
import json
import uuid
import sys
from pathlib import Path
from datetime import datetime
import shutil


def backup_file(file_path):
    """Create a backup of the file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    shutil.copy2(file_path, backup_path)
    print(f"✓ Backup created: {backup_path.name}")
    return backup_path


def is_valid_uuid(uuid_string):
    """Check if a string is a valid UUID v4 format"""
    import re
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return re.match(pattern, str(uuid_string).lower()) is not None


def fix_quiz_json(json_file_path):
    """
    Fix all UUID issues in the quiz JSON file
    """
    print("=" * 80, flush=True)
    print("FIXING QUIZ JSON UUIDs", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)

    # Create backup
    backup_path = backup_file(json_file_path)

    # Load the JSON data
    print(f"Loading: {json_file_path}", flush=True)
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ JSON file loaded successfully", flush=True)
    except Exception as e:
        print(f"✗ Error loading JSON file: {e}", flush=True)
        return False

    # Track all UUIDs and fixes
    all_uuids = set()
    invalid_uuids_fixed = 0
    duplicate_uuids_fixed = 0

    print("\nProcessing quizzes...")
    print("-" * 80)

    # Process each quiz
    for quiz_idx, quiz in enumerate(data.get('quizzes', [])):
        quiz_name = quiz.get('name', f'Quiz {quiz_idx + 1}')
        questions = quiz.get('questions', [])

        print(f"\n{quiz_idx + 1}. {quiz_name} ({len(questions)} questions)")

        quiz_invalid = 0
        quiz_duplicates = 0

        for q_idx, question in enumerate(questions):
            old_uuid = question.get('uuid')

            # Check if UUID is invalid or duplicate
            needs_replacement = False
            reason = ""

            if not old_uuid:
                needs_replacement = True
                reason = "missing"
            elif not is_valid_uuid(old_uuid):
                needs_replacement = True
                reason = "invalid format"
                quiz_invalid += 1
                invalid_uuids_fixed += 1
            elif old_uuid in all_uuids:
                needs_replacement = True
                reason = "duplicate"
                quiz_duplicates += 1
                duplicate_uuids_fixed += 1

            # Replace if needed
            if needs_replacement:
                new_uuid = str(uuid.uuid4())
                question['uuid'] = new_uuid
                all_uuids.add(new_uuid)

                q_id = question.get('id', 'N/A')
                if q_idx < 5 or (q_idx == 5 and (quiz_invalid > 0 or quiz_duplicates > 0)):
                    # Show first few fixes per quiz
                    print(f"   Q{q_id}: {reason} UUID replaced")
                    print(f"       Old: {old_uuid}")
                    print(f"       New: {new_uuid}")
            else:
                all_uuids.add(old_uuid)

        if quiz_invalid > 5:
            print(f"   ... and {quiz_invalid - 5} more invalid UUIDs fixed")
        if quiz_duplicates > 0:
            print(f"   Fixed {quiz_duplicates} duplicate UUID(s)")

        if quiz_invalid == 0 and quiz_duplicates == 0:
            print(f"   ✓ All UUIDs valid and unique")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Invalid UUIDs fixed: {invalid_uuids_fixed}")
    print(f"Duplicate UUIDs fixed: {duplicate_uuids_fixed}")
    print(f"Total UUIDs replaced: {invalid_uuids_fixed + duplicate_uuids_fixed}")
    print(f"Total unique UUIDs: {len(all_uuids)}")

    # Save the fixed JSON
    print("\nSaving fixed JSON...")
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Fixed JSON saved to: {json_file_path}")
        print(f"✓ Original backed up to: {backup_path.name}")
        return True
    except Exception as e:
        print(f"✗ Error saving JSON file: {e}")
        # Restore from backup
        print("Restoring from backup...")
        shutil.copy2(backup_path, json_file_path)
        return False


def verify_fixes(json_file_path):
    """
    Verify that all UUIDs are now valid and unique
    """
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_uuids = []
        invalid_count = 0

        for quiz in data.get('quizzes', []):
            for question in quiz.get('questions', []):
                uuid_str = question.get('uuid')
                if uuid_str:
                    all_uuids.append(uuid_str)
                    if not is_valid_uuid(uuid_str):
                        invalid_count += 1

        duplicates = len(all_uuids) - len(set(all_uuids))

        print(f"Total UUIDs: {len(all_uuids)}")
        print(f"Unique UUIDs: {len(set(all_uuids))}")
        print(f"Invalid format: {invalid_count}")
        print(f"Duplicates: {duplicates}")

        if invalid_count == 0 and duplicates == 0:
            print("\n✓ ALL ISSUES FIXED! JSON is now valid.")
            return True
        else:
            print("\n✗ Some issues remain. Please check the file.")
            return False

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return False


if __name__ == "__main__":
    # Determine file paths
    script_dir = Path(__file__).parent
    resources_dir = script_dir / "src" / "main" / "resources"
    json_file = resources_dir / "quiz-questions.json"

    if not json_file.exists():
        print(f"Error: JSON file not found: {json_file}")
        sys.exit(1)

    # Fix the file
    success = fix_quiz_json(json_file)

    if success:
        # Verify fixes
        verified = verify_fixes(json_file)

        if verified:
            print("\n" + "=" * 80)
            print("✓ SUCCESS! Quiz JSON has been fixed and verified.")
            print("=" * 80)
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("\n✗ Failed to fix JSON file.")
        sys.exit(1)

