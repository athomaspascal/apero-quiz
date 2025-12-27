import json
import uuid
import re
from datetime import datetime
import shutil

# Paths
json_file = r"src\main\resources\quiz-questions.json"
backup_file = f"src\\main\\resources\\quiz-questions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

print("="*80)
print("UUID FIXER")
print("="*80)

# Backup
print(f"\n1. Creating backup...")
shutil.copy2(json_file, backup_file)
print(f"   ✓ Backup: {backup_file}")

# Load
print(f"\n2. Loading JSON...")
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"   ✓ Loaded {len(data['quizzes'])} quizzes")

# Process
print(f"\n3. Fixing UUIDs...")
uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
all_uuids = set()
invalid = 0
duplicates = 0

for quiz in data['quizzes']:
    for question in quiz['questions']:
        old = question.get('uuid', '')
        valid = bool(re.match(uuid_pattern, old.lower()))

        if not old or not valid:
            question['uuid'] = str(uuid.uuid4())
            invalid += 1
            all_uuids.add(question['uuid'])
        elif old in all_uuids:
            question['uuid'] = str(uuid.uuid4())
            duplicates += 1
            all_uuids.add(question['uuid'])
        else:
            all_uuids.add(old)

print(f"   ✓ Fixed {invalid} invalid UUIDs")
print(f"   ✓ Fixed {duplicates} duplicate UUIDs")

# Save
print(f"\n4. Saving...")
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"   ✓ Saved")

# Verify
print(f"\n5. Verifying...")
with open(json_file, 'r', encoding='utf-8') as f:
    verify = json.load(f)

check_uuids = []
for quiz in verify['quizzes']:
    for q in quiz['questions']:
        check_uuids.append(q['uuid'])

bad = sum(1 for u in check_uuids if not re.match(uuid_pattern, u.lower()))
dups = len(check_uuids) - len(set(check_uuids))

print(f"   Total UUIDs: {len(check_uuids)}")
print(f"   Unique: {len(set(check_uuids))}")
print(f"   Invalid: {bad}")
print(f"   Duplicates: {dups}")

if bad == 0 and dups == 0:
    print("\n✓ SUCCESS - All UUIDs fixed!")
else:
    print("\n✗ FAILED - Issues remain")

print("="*80)

