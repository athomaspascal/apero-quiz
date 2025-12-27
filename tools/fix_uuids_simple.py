"""
Direct UUID fixer - simpler version with immediate output
"""
import json
import uuid
import sys
import os
from datetime import datetime
import shutil

print("Starting UUID fixer...", flush=True)
sys.stdout.flush()

# File paths
json_file = r"C:\Users\athom\IdeaProjects\quizz1\src\main\resources\quiz-questions.json"

# Create backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = json_file.replace(".json", f"_backup_{timestamp}.json")
print(f"\nCreating backup: {os.path.basename(backup_file)}", flush=True)
shutil.copy2(json_file, backup_file)
print("✓ Backup created", flush=True)

# Load JSON
print(f"\nLoading JSON file...", flush=True)
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"✓ Loaded {len(data['quizzes'])} quizzes", flush=True)

# Fix UUIDs
print("\n" + "="*80, flush=True)
print("PROCESSING QUIZZES", flush=True)
print("="*80, flush=True)

all_uuids = set()
total_invalid = 0
total_duplicates = 0

for quiz_idx, quiz in enumerate(data['quizzes']):
    quiz_name = quiz['name']
    questions = quiz['questions']

    print(f"\n{quiz_idx + 1}. {quiz_name} ({len(questions)} questions)", flush=True)

    quiz_fixes = 0

    for question in questions:
        old_uuid = question.get('uuid', '')

        # Check if valid UUID format
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        is_valid = re.match(uuid_pattern, old_uuid.lower()) is not None

        needs_fix = False
        reason = ""

        if not old_uuid:
            needs_fix = True
            reason = "missing"
        elif not is_valid:
            needs_fix = True
            reason = "invalid format"
            total_invalid += 1
        elif old_uuid in all_uuids:
            needs_fix = True
            reason = "duplicate"
            total_duplicates += 1

        if needs_fix:
            new_uuid = str(uuid.uuid4())
            question['uuid'] = new_uuid
            all_uuids.add(new_uuid)
            quiz_fixes += 1

            if quiz_fixes <= 3:
                print(f"   Fixed Q{question['id']}: {reason}", flush=True)
        else:
            all_uuids.add(old_uuid)

    if quiz_fixes > 3:
        print(f"   ... and {quiz_fixes - 3} more fixes", flush=True)
    elif quiz_fixes == 0:
        print(f"   ✓ All UUIDs OK", flush=True)

print("\n" + "="*80, flush=True)
print("SUMMARY", flush=True)
print("="*80, flush=True)
print(f"Invalid UUIDs fixed: {total_invalid}", flush=True)
print(f"Duplicate UUIDs fixed: {total_duplicates}", flush=True)
print(f"Total fixes: {total_invalid + total_duplicates}", flush=True)
print(f"Total unique UUIDs: {len(all_uuids)}", flush=True)

# Save
print("\nSaving fixed JSON...", flush=True)
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("✓ File saved", flush=True)

# Verify
print("\n" + "="*80, flush=True)
print("VERIFICATION", flush=True)
print("="*80, flush=True)

with open(json_file, 'r', encoding='utf-8') as f:
    verify_data = json.load(f)

verify_uuids = []
verify_invalid = 0

for quiz in verify_data['quizzes']:
    for question in quiz['questions']:
        u = question.get('uuid', '')
        verify_uuids.append(u)
        if not re.match(uuid_pattern, u.lower()):
            verify_invalid += 1

verify_duplicates = len(verify_uuids) - len(set(verify_uuids))

print(f"Total UUIDs: {len(verify_uuids)}", flush=True)
print(f"Unique UUIDs: {len(set(verify_uuids))}", flush=True)
print(f"Invalid format: {verify_invalid}", flush=True)
print(f"Duplicates: {verify_duplicates}", flush=True)

if verify_invalid == 0 and verify_duplicates == 0:
    print("\n✓ SUCCESS! All UUIDs are now valid and unique.", flush=True)
else:
    print("\n✗ Some issues remain.", flush=True)

print("="*80, flush=True)

