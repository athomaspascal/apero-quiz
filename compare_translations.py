import re

# Read all properties files
with open('src/main/resources/messages_en.properties', 'r', encoding='utf-8') as f:
    en_lines = f.readlines()
with open('src/main/resources/messages_fr.properties', 'r', encoding='utf-8') as f:
    fr_lines = f.readlines()
with open('src/main/resources/messages_it.properties', 'r', encoding='utf-8') as f:
    it_lines = f.readlines()

# Extract keys (lines that are not comments and not empty)
def extract_keys(lines):
    keys = set()
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key = line.split('=')[0].strip()
            keys.add(key)
    return keys

en_keys = extract_keys(en_lines)
fr_keys = extract_keys(fr_lines)
it_keys = extract_keys(it_lines)

print('Keys in FR but not in EN:')
for key in sorted(fr_keys - en_keys):
    print(f'  {key}')

print('\nKeys in EN but not in FR:')
for key in sorted(en_keys - fr_keys):
    print(f'  {key}')

print('\nKeys in EN but not in IT:')
for key in sorted(en_keys - it_keys):
    print(f'  {key}')

print(f'\nTotal EN keys: {len(en_keys)}')
print(f'Total FR keys: {len(fr_keys)}')
print(f'Total IT keys: {len(it_keys)}')

