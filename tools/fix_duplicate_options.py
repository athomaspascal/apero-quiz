"""
Fix duplicate options in quiz questions
"""
import json
from datetime import datetime
import shutil

json_file = r"src\main\resources\quiz-questions.json"
backup_file = f"src\\main\\resources\\quiz-questions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

print("="*80)
print("FIXING DUPLICATE OPTIONS")
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

# Fix
print(f"\n3. Fixing duplicate options...")

alternative_options = [
    "Neptune", "Pluto", "Minerva", "Mercury", "Diana", "Vulcan", "Bacchus",
    "Ceres", "Proserpina", "Vesta", "Apollo", "Juno", "Saturn", "Uranus",
    "Unknown", "Various", "Multiple gods", "Not specified", "Titans", "Olympians"
]

fixed = 0

for quiz_idx, quiz in enumerate(data['quizzes']):
    for q in quiz['questions']:
        options = q.get('options', [])

        # Check for duplicates
        if len(options) != len(set(options)):
            # Has duplicates
            answer = q['answer']

            # Create new unique options
            new_options = []
            seen = set()

            for opt in options:
                if opt not in seen:
                    new_options.append(opt)
                    seen.add(opt)

            # Fill with alternatives until we have 4 options
            alt_idx = 0
            while len(new_options) < 4:
                if alternative_options[alt_idx] not in new_options:
                    new_options.append(alternative_options[alt_idx])
                alt_idx += 1

            # Make sure answer is in options
            if answer not in new_options:
                new_options[0] = answer

            q['options'] = new_options[:4]
            fixed += 1

print(f"   ✓ Fixed {fixed} questions with duplicate options")

# Save
print(f"\n4. Saving...")
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"   ✓ Saved")

print("\n" + "="*80)
print(f"✓ SUCCESS - Fixed {fixed} questions")
print("="*80)

