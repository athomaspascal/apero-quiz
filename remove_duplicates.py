import re
from pathlib import Path

def remove_duplicates(file_path):
    """Remove duplicate property keys from a properties file, keeping the first occurrence."""
    print(f"\nProcessing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    seen_keys = set()
    output_lines = []
    duplicates_removed = 0

    for line in lines:
        stripped = line.strip()

        # Keep comments and empty lines
        if not stripped or stripped.startswith('#'):
            output_lines.append(line)
            continue

        # Extract key
        if '=' in stripped:
            key = stripped.split('=')[0].strip()

            if key in seen_keys:
                print(f"  Removing duplicate: {key}")
                duplicates_removed += 1
                continue
            else:
                seen_keys.add(key)
                output_lines.append(line)
        else:
            output_lines.append(line)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

    print(f"  Removed {duplicates_removed} duplicates")
    print(f"  Total unique keys: {len(seen_keys)}")

# Process all properties files
files = [
    'src/main/resources/messages_en.properties',
    'src/main/resources/messages_fr.properties',
    'src/main/resources/messages_it.properties'
]

for file_path in files:
    remove_duplicates(file_path)

print("\n✓ All files processed successfully!")

