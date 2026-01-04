import re
import os
from pathlib import Path

# Extract all translation keys used in Java files
def extract_keys_from_java(java_dir):
    keys = set()
    pattern = r'translationService\.translate\(["\']([^"\']+)["\']'
    pattern2 = r'@Menu\(.*?title\s*=\s*["\']([^"\']+)["\']'
    pattern3 = r'@PageTitle\(["\']([^"\']+)["\']'

    for java_file in Path(java_dir).rglob('*.java'):
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                keys.update(re.findall(pattern, content))
                keys.update(re.findall(pattern2, content))
                keys.update(re.findall(pattern3, content))
        except Exception as e:
            print(f"Error reading {java_file}: {e}")

    return keys

# Extract keys from properties file
def extract_keys_from_properties(prop_file):
    keys = set()
    try:
        with open(prop_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    keys.add(key)
    except Exception as e:
        print(f"Error reading {prop_file}: {e}")

    return keys

# Main
java_dir = 'src/main/java'
en_file = 'src/main/resources/messages_en.properties'
fr_file = 'src/main/resources/messages_fr.properties'
it_file = 'src/main/resources/messages_it.properties'

print("Extracting keys from Java files...")
used_keys = extract_keys_from_java(java_dir)
print(f"Found {len(used_keys)} keys used in Java code\n")

print("Extracting keys from properties files...")
en_keys = extract_keys_from_properties(en_file)
fr_keys = extract_keys_from_properties(fr_file)
it_keys = extract_keys_from_properties(it_file)

print(f"EN keys: {len(en_keys)}")
print(f"FR keys: {len(fr_keys)}")
print(f"IT keys: {len(it_keys)}\n")

# Find missing keys
missing_in_en = used_keys - en_keys
missing_in_fr = used_keys - fr_keys
missing_in_it = used_keys - it_keys

if missing_in_en:
    print("Keys used in code but missing in EN:")
    for key in sorted(missing_in_en):
        print(f"  {key}")
else:
    print("All used keys are present in EN")

print()

if missing_in_fr:
    print("Keys used in code but missing in FR:")
    for key in sorted(missing_in_fr):
        print(f"  {key}")
else:
    print("All used keys are present in FR")

print()

if missing_in_it:
    print("Keys used in code but missing in IT:")
    for key in sorted(missing_in_it):
        print(f"  {key}")
else:
    print("All used keys are present in IT")

# Also check FR and IT have all EN keys
print("\n" + "="*60)
print("Checking completeness against EN file...")
print("="*60 + "\n")

missing_fr = en_keys - fr_keys
missing_it = en_keys - it_keys

if missing_fr:
    print(f"Keys in EN but missing in FR ({len(missing_fr)}):")
    for key in sorted(missing_fr):
        print(f"  {key}")
else:
    print("FR has all EN keys ✓")

print()

if missing_it:
    print(f"Keys in EN but missing in IT ({len(missing_it)}):")
    for key in sorted(missing_it):
        print(f"  {key}")
else:
    print("IT has all EN keys ✓")

