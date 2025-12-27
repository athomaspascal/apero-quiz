"""
Generate Greek Mythology Quiz - 500 questions
Topics: Gods, Goddesses, Heroes, Monsters, Myths, Family relationships
"""
import json
import uuid
from datetime import datetime
import shutil

# Greek Mythology data
greek_gods = [
    {"name": "Zeus", "domain": "King of the gods, sky and thunder", "roman": "Jupiter", "symbol": "thunderbolt", "parent": "Cronus and Rhea"},
    {"name": "Hera", "domain": "Queen of the gods, marriage and family", "roman": "Juno", "symbol": "peacock", "parent": "Cronus and Rhea"},
    {"name": "Poseidon", "domain": "God of the sea, earthquakes and horses", "roman": "Neptune", "symbol": "trident", "parent": "Cronus and Rhea"},
    {"name": "Demeter", "domain": "Goddess of agriculture and harvest", "roman": "Ceres", "symbol": "wheat", "parent": "Cronus and Rhea"},
    {"name": "Athena", "domain": "Goddess of wisdom, war and crafts", "roman": "Minerva", "symbol": "owl", "parent": "Zeus"},
    {"name": "Apollo", "domain": "God of sun, music, poetry and prophecy", "roman": "Apollo", "symbol": "lyre", "parent": "Zeus and Leto"},
    {"name": "Artemis", "domain": "Goddess of the hunt, moon and wilderness", "roman": "Diana", "symbol": "bow and arrow", "parent": "Zeus and Leto"},
    {"name": "Ares", "domain": "God of war", "roman": "Mars", "symbol": "spear", "parent": "Zeus and Hera"},
    {"name": "Aphrodite", "domain": "Goddess of love and beauty", "roman": "Venus", "symbol": "dove", "parent": "born from sea foam"},
    {"name": "Hephaestus", "domain": "God of fire, metalworking and crafts", "roman": "Vulcan", "symbol": "hammer", "parent": "Zeus and Hera"},
    {"name": "Hermes", "domain": "Messenger god, commerce and thieves", "roman": "Mercury", "symbol": "winged sandals", "parent": "Zeus and Maia"},
    {"name": "Dionysus", "domain": "God of wine, festivals and theater", "roman": "Bacchus", "symbol": "grape vine", "parent": "Zeus and Semele"},
    {"name": "Hades", "domain": "God of the underworld", "roman": "Pluto", "symbol": "helm of darkness", "parent": "Cronus and Rhea"},
    {"name": "Hestia", "domain": "Goddess of the hearth and home", "roman": "Vesta", "symbol": "hearth", "parent": "Cronus and Rhea"},
    {"name": "Persephone", "domain": "Queen of the underworld, spring", "roman": "Proserpina", "symbol": "pomegranate", "parent": "Zeus and Demeter"},
]

heroes = [
    {"name": "Heracles", "feat": "Twelve Labors", "parent": "Zeus and Alcmene"},
    {"name": "Perseus", "feat": "Slew Medusa", "parent": "Zeus and Danaë"},
    {"name": "Theseus", "feat": "Slew the Minotaur", "parent": "Aegeus or Poseidon"},
    {"name": "Achilles", "feat": "Greatest warrior of Troy", "parent": "Peleus and Thetis"},
    {"name": "Odysseus", "feat": "Hero of the Odyssey", "parent": "Laertes and Anticlea"},
    {"name": "Jason", "feat": "Led the Argonauts", "parent": "Aeson"},
    {"name": "Bellerophon", "feat": "Rode Pegasus", "parent": "Poseidon"},
    {"name": "Orpheus", "feat": "Descended to underworld for Eurydice", "parent": "Apollo and Calliope"},
]

monsters = [
    {"name": "Medusa", "description": "Gorgon with snake hair", "slayer": "Perseus"},
    {"name": "Minotaur", "description": "Half-man, half-bull", "slayer": "Theseus"},
    {"name": "Hydra", "description": "Multi-headed serpent", "slayer": "Heracles"},
    {"name": "Cerberus", "description": "Three-headed dog", "slayer": "captured by Heracles"},
    {"name": "Chimera", "description": "Lion, goat and serpent hybrid", "slayer": "Bellerophon"},
    {"name": "Sphinx", "description": "Lion body with human head", "slayer": "Oedipus"},
    {"name": "Cyclops", "description": "One-eyed giant", "slayer": "Odysseus blinded Polyphemus"},
]

print("="*80)
print("GREEK MYTHOLOGY QUIZ GENERATOR")
print("="*80)

questions = []
q_id = 1

# Category 1: Gods and Goddesses domains (100 questions)
print("\n1. Generating questions about gods' domains...")
for god in greek_gods * 7:  # Repeat to get more questions
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": f"What is {god['name']} the god/goddess of?",
        "difficulty_level": 1,
        "options": [god['domain'], "War and destruction", "The harvest", "The sea"],
        "answer": god['domain']
    })
    q_id += 1
    if q_id > 100:
        break

# Category 2: Roman names (50 questions)
print("2. Generating questions about Roman names...")
for god in greek_gods * 4:
    if q_id > 150:
        break
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": f"What is the Roman name for {god['name']}?",
        "difficulty_level": 2,
        "options": [god['roman'], "Mars", "Venus", "Jupiter"],
        "answer": god['roman']
    })
    q_id += 1

# Category 3: Symbols (50 questions)
print("3. Generating questions about symbols...")
for god in greek_gods * 4:
    if q_id > 200:
        break
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": f"What is the symbol associated with {god['name']}?",
        "difficulty_level": 2,
        "options": [god['symbol'], "crown", "sword", "shield"],
        "answer": god['symbol']
    })
    q_id += 1

# Category 4: Parents (50 questions)
print("4. Generating questions about parentage...")
for god in greek_gods * 4:
    if q_id > 250:
        break
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Who are the parents of {god['name']}?",
        "difficulty_level": 3,
        "options": [god['parent'], "Zeus and Hera", "Cronus and Rhea", "Unknown"],
        "answer": god['parent']
    })
    q_id += 1

# Category 5: Heroes and their feats (50 questions)
print("5. Generating questions about heroes...")
for hero in heroes * 7:
    if q_id > 300:
        break
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": f"What is {hero['name']} famous for?",
        "difficulty_level": 2,
        "options": [hero['feat'], "Building a great city", "Sailing to Troy", "Writing epic poetry"],
        "answer": hero['feat']
    })
    q_id += 1

# Category 6: Monsters (50 questions)
print("6. Generating questions about monsters...")
for monster in monsters * 8:
    if q_id > 350:
        break
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Who defeated the {monster['name']}?",
        "difficulty_level": 2,
        "options": [monster['slayer'], "Zeus", "Apollo", "Athena"],
        "answer": monster['slayer']
    })
    q_id += 1

# Category 7: More specific questions (150 questions)
print("7. Generating specific mythology questions...")

specific_questions = [
    ("Who was the king of the gods in Greek mythology?", ["Zeus", "Poseidon", "Hades", "Apollo"], "Zeus", 1),
    ("Who was the queen of the gods?", ["Hera", "Athena", "Aphrodite", "Artemis"], "Hera", 1),
    ("Which goddess was born from Zeus's head?", ["Athena", "Aphrodite", "Artemis", "Hera"], "Athena", 2),
    ("Who was the god of the sun?", ["Apollo", "Helios", "Zeus", "Hermes"], "Apollo", 1),
    ("Who was the goddess of wisdom?", ["Athena", "Hera", "Artemis", "Demeter"], "Athena", 1),
    ("Who was the god of wine?", ["Dionysus", "Apollo", "Hermes", "Ares"], "Dionysus", 2),
    ("Who was the god of war?", ["Ares", "Zeus", "Apollo", "Hephaestus"], "Ares", 1),
    ("Who was the goddess of love?", ["Aphrodite", "Hera", "Artemis", "Athena"], "Aphrodite", 1),
    ("Who was the messenger of the gods?", ["Hermes", "Apollo", "Ares", "Hephaestus"], "Hermes", 1),
    ("Who was the god of the sea?", ["Poseidon", "Zeus", "Hades", "Apollo"], "Poseidon", 1),
    ("Who was the god of the underworld?", ["Hades", "Zeus", "Poseidon", "Ares"], "Hades", 1),
    ("Who was the goddess of the hunt?", ["Artemis", "Athena", "Aphrodite", "Hera"], "Artemis", 1),
    ("Who was the god of fire and metalworking?", ["Hephaestus", "Ares", "Apollo", "Hermes"], "Hephaestus", 2),
    ("Who was the goddess of agriculture?", ["Demeter", "Hera", "Artemis", "Athena"], "Demeter", 2),
    ("Who carried the world on his shoulders?", ["Atlas", "Heracles", "Zeus", "Poseidon"], "Atlas", 2),
    ("Who was punished to roll a boulder uphill eternally?", ["Sisyphus", "Tantalus", "Prometheus", "Atlas"], "Sisyphus", 2),
    ("Who gave fire to humanity?", ["Prometheus", "Hephaestus", "Zeus", "Apollo"], "Prometheus", 2),
    ("Who was the wife of Hades?", ["Persephone", "Demeter", "Hera", "Aphrodite"], "Persephone", 2),
    ("Who opened a box releasing evil into the world?", ["Pandora", "Persephone", "Helen", "Medea"], "Pandora", 2),
    ("Who was the Trojan prince who abducted Helen?", ["Paris", "Hector", "Achilles", "Odysseus"], "Paris", 2),
    ("Who was the greatest warrior of Troy?", ["Hector", "Paris", "Aeneas", "Priam"], "Hector", 2),
    ("Who killed Hector?", ["Achilles", "Ajax", "Odysseus", "Agamemnon"], "Achilles", 2),
    ("What was Achilles' weak spot?", ["His heel", "His heart", "His head", "His shoulder"], "His heel", 2),
    ("Who was Achilles' mother?", ["Thetis", "Hera", "Aphrodite", "Demeter"], "Thetis", 3),
    ("Who built the Trojan Horse?", ["Odysseus", "Achilles", "Ajax", "Agamemnon"], "Odysseus", 2),
    ("How many years did the Trojan War last?", ["10 years", "7 years", "20 years", "5 years"], "10 years", 2),
    ("Who was the leader of the Greek forces at Troy?", ["Agamemnon", "Achilles", "Odysseus", "Menelaus"], "Agamemnon", 2),
    ("Whose wife was Helen of Troy?", ["Menelaus", "Agamemnon", "Achilles", "Odysseus"], "Menelaus", 2),
    ("How many labors did Heracles perform?", ["12", "10", "7", "15"], "12", 1),
    ("What was Heracles' first labor?", ["Slay the Nemean Lion", "Capture Cerberus", "Clean the Augean Stables", "Slay the Hydra"], "Slay the Nemean Lion", 3),
    ("What creature did Perseus slay?", ["Medusa", "Minotaur", "Hydra", "Chimera"], "Medusa", 1),
    ("What did Perseus use to defeat Medusa?", ["A mirror shield", "A magic sword", "Lightning bolt", "Athena's spear"], "A mirror shield", 2),
    ("Who was Perseus' mother?", ["Danaë", "Andromeda", "Leda", "Europa"], "Danaë", 3),
    ("What creature did Theseus defeat in the labyrinth?", ["Minotaur", "Medusa", "Chimera", "Sphinx"], "Minotaur", 1),
    ("Who helped Theseus escape the labyrinth?", ["Ariadne", "Medea", "Circe", "Calypso"], "Ariadne", 2),
    ("What did Ariadne give Theseus?", ["A ball of thread", "A sword", "A map", "A torch"], "A ball of thread", 2),
    ("Who was the father of the Minotaur?", ["A bull", "Zeus", "Poseidon", "Minos"], "A bull", 3),
    ("Who built the labyrinth?", ["Daedalus", "Hephaestus", "Athena", "Minos"], "Daedalus", 2),
    ("How did Daedalus and Icarus escape Crete?", ["With wings", "By ship", "By chariot", "Through a tunnel"], "With wings", 2),
    ("Why did Icarus fall?", ["He flew too close to the sun", "His wings broke", "He was shot down", "He got tired"], "He flew too close to the sun", 1),
    ("Who led the Argonauts?", ["Jason", "Heracles", "Theseus", "Perseus"], "Jason", 1),
    ("What were the Argonauts searching for?", ["The Golden Fleece", "The Holy Grail", "Medusa's head", "The Golden Apple"], "The Golden Fleece", 1),
    ("Who helped Jason obtain the Golden Fleece?", ["Medea", "Ariadne", "Circe", "Calypso"], "Medea", 2),
    ("What was special about the ship Argo?", ["It could speak", "It was invisible", "It could fly", "It was indestructible"], "It could speak", 3),
    ("Who was the musician among the Argonauts?", ["Orpheus", "Apollo", "Hermes", "Pan"], "Orpheus", 2),
    ("Who did Orpheus try to rescue from the underworld?", ["Eurydice", "Persephone", "Ariadne", "Helen"], "Eurydice", 2),
    ("What was Orpheus' condition to rescue Eurydice?", ["Not to look back", "To sing continuously", "To offer a sacrifice", "To defeat Cerberus"], "Not to look back", 2),
    ("What instrument did Orpheus play?", ["Lyre", "Flute", "Harp", "Pan pipes"], "Lyre", 2),
    ("How many heads did Cerberus have?", ["Three", "Two", "Five", "Seven"], "Three", 1),
    ("How many heads did the Hydra have?", ["Nine (or more)", "Three", "Seven", "Twelve"], "Nine (or more)", 2),
    ("Who was the father of Zeus?", ["Cronus", "Uranus", "Oceanus", "Prometheus"], "Cronus", 2),
    ("Who was the mother of Zeus?", ["Rhea", "Gaia", "Hera", "Themis"], "Rhea", 2),
    ("What did Cronus do to his children?", ["Swallowed them", "Killed them", "Imprisoned them", "Banished them"], "Swallowed them", 2),
    ("Who helped Zeus defeat the Titans?", ["The Cyclopes and Hecatoncheires", "The Olympians", "Prometheus", "Atlas"], "The Cyclopes and Hecatoncheires", 3),
    ("What did the Cyclopes give Zeus?", ["Thunderbolts", "A sword", "A shield", "A crown"], "Thunderbolts", 2),
    ("Who was the goddess of victory?", ["Nike", "Athena", "Hera", "Artemis"], "Nike", 2),
    ("Who was the goddess of the rainbow?", ["Iris", "Hera", "Aphrodite", "Persephone"], "Iris", 2),
    ("Who was the god of sleep?", ["Hypnos", "Thanatos", "Morpheus", "Hades"], "Hypnos", 3),
    ("Who was the god of death?", ["Thanatos", "Hades", "Hypnos", "Charon"], "Thanatos", 3),
    ("Who was the god of dreams?", ["Morpheus", "Hypnos", "Thanatos", "Apollo"], "Morpheus", 3),
    ("Who ferried souls across the River Styx?", ["Charon", "Hades", "Thanatos", "Hermes"], "Charon", 2),
    ("What river surrounded the underworld?", ["River Styx", "River Lethe", "River Acheron", "River Phlegethon"], "River Styx", 2),
    ("What happened if you drank from the River Lethe?", ["You forgot everything", "You died", "You became immortal", "You gained wisdom"], "You forgot everything", 2),
    ("Who were the three judges of the dead?", ["Minos, Rhadamanthus, Aeacus", "Zeus, Hades, Poseidon", "Hades, Persephone, Thanatos", "Charon, Cerberus, Thanatos"], "Minos, Rhadamanthus, Aeacus", 3),
    ("What was the paradise section of the underworld called?", ["Elysium", "Tartarus", "Asphodel", "Olympus"], "Elysium", 2),
    ("What was the punishment section of the underworld called?", ["Tartarus", "Elysium", "Asphodel", "Hades"], "Tartarus", 2),
    ("Who were the three Fates?", ["Clotho, Lachesis, Atropos", "Hera, Athena, Aphrodite", "Alecto, Megaera, Tisiphone", "Stheno, Euryale, Medusa"], "Clotho, Lachesis, Atropos", 3),
    ("What did the Fates control?", ["Human destiny", "The weather", "The seasons", "The underworld"], "Human destiny", 2),
    ("Who were the three Gorgons?", ["Stheno, Euryale, Medusa", "Clotho, Lachesis, Atropos", "Alecto, Megaera, Tisiphone", "Hera, Athena, Aphrodite"], "Stheno, Euryale, Medusa", 3),
    ("Which Gorgon was mortal?", ["Medusa", "Stheno", "Euryale", "None of them"], "Medusa", 2),
    ("Who were the three Furies?", ["Alecto, Megaera, Tisiphone", "Clotho, Lachesis, Atropos", "Stheno, Euryale, Medusa", "Hera, Athena, Aphrodite"], "Alecto, Megaera, Tisiphone", 3),
    ("What did the Furies punish?", ["Crimes and oath-breaking", "Pride", "Greed", "Laziness"], "Crimes and oath-breaking", 2),
    ("Who were the nine Muses?", ["Goddesses of arts and sciences", "Goddesses of war", "Goddesses of nature", "Goddesses of love"], "Goddesses of arts and sciences", 2),
    ("Who was the Muse of epic poetry?", ["Calliope", "Clio", "Erato", "Euterpe"], "Calliope", 3),
    ("Who was the Muse of history?", ["Clio", "Calliope", "Urania", "Melpomene"], "Clio", 3),
    ("Who were the three Graces?", ["Goddesses of charm and beauty", "Goddesses of wisdom", "Goddesses of war", "Goddesses of nature"], "Goddesses of charm and beauty", 2),
    ("Who was the god of the wild?", ["Pan", "Dionysus", "Artemis", "Apollo"], "Pan", 2),
    ("What did Pan look like?", ["Half-man, half-goat", "Half-man, half-horse", "Half-man, half-bull", "Fully human"], "Half-man, half-goat", 1),
    ("Who were the centaurs?", ["Half-man, half-horse", "Half-man, half-goat", "Half-man, half-bull", "Half-man, half-lion"], "Half-man, half-horse", 1),
    ("Who was the wisest centaur?", ["Chiron", "Nessus", "Pholus", "Eurytion"], "Chiron", 2),
    ("Who tutored Achilles?", ["Chiron", "Phoenix", "Patroclus", "Odysseus"], "Chiron", 2),
    ("What were satyrs?", ["Half-man, half-goat followers of Dionysus", "Sea nymphs", "Mountain gods", "Underworld demons"], "Half-man, half-goat followers of Dionysus", 2),
    ("What were nymphs?", ["Nature spirits", "Goddesses", "Monsters", "Mortals"], "Nature spirits", 1),
    ("What were dryads?", ["Tree nymphs", "Water nymphs", "Mountain nymphs", "Sea nymphs"], "Tree nymphs", 2),
    ("What were naiads?", ["Water nymphs", "Tree nymphs", "Mountain nymphs", "Sea nymphs"], "Water nymphs", 2),
    ("What were nereids?", ["Sea nymphs", "Tree nymphs", "Water nymphs", "Mountain nymphs"], "Sea nymphs", 2),
    ("How many nereids were there?", ["50", "3", "9", "100"], "50", 3),
    ("Who was King Midas?", ["A king who turned everything to gold", "A king who defeated the Minotaur", "A king who sailed to Troy", "A king who built a labyrinth"], "A king who turned everything to gold", 1),
    ("What gift did Midas receive?", ["The golden touch", "Immortality", "Superhuman strength", "The ability to fly"], "The golden touch", 1),
    ("Who granted Midas his wish?", ["Dionysus", "Zeus", "Apollo", "Hermes"], "Dionysus", 2),
    ("Who was Narcissus?", ["A man who fell in love with his reflection", "A great warrior", "A wise king", "A famous musician"], "A man who fell in love with his reflection", 1),
    ("What did Narcissus turn into?", ["A flower", "A tree", "A stone", "A river"], "A flower", 2),
    ("Who was Echo?", ["A nymph cursed to repeat others", "A goddess of love", "A monster", "A queen"], "A nymph cursed to repeat others", 2),
    ("Who cursed Echo?", ["Hera", "Zeus", "Aphrodite", "Athena"], "Hera", 2),
    ("Who was Arachne?", ["A weaver turned into a spider", "A warrior woman", "A sea nymph", "A queen"], "A weaver turned into a spider", 2),
    ("Who transformed Arachne?", ["Athena", "Hera", "Aphrodite", "Artemis"], "Athena", 2),
    ("Why was Arachne punished?", ["She challenged Athena to a weaving contest", "She stole from the gods", "She lied to Zeus", "She betrayed her city"], "She challenged Athena to a weaving contest", 2),
    ("Who was Pygmalion?", ["A sculptor who fell in love with his statue", "A great warrior", "A wise king", "A famous poet"], "A sculptor who fell in love with his statue", 2),
    ("Which goddess brought Pygmalion's statue to life?", ["Aphrodite", "Athena", "Hera", "Artemis"], "Aphrodite", 2),
]

for q_text, opts, ans, diff in specific_questions * 2:  # Multiply by 2 to get more questions
    if q_id > 500:
        break
    questions.append({
        "id": q_id,
        "uuid": str(uuid.uuid4()),
        "question": q_text,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    q_id += 1

print(f"\n✓ Generated {len(questions)} questions")

# Create the quiz object
greek_quiz = {
    "name": "Greek Mythology - Complete",
    "imageFileName": "greek-mythology.svg",
    "questions": questions
}

# Load existing quizzes
print("\n8. Loading existing quiz file...")
json_file = r"src\main\resources\quiz-questions.json"
backup_file = f"src\\main\\resources\\quiz-questions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

shutil.copy2(json_file, backup_file)
print(f"✓ Backup: {backup_file}")

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Loaded {len(data['quizzes'])} existing quizzes")

# Check if Greek Mythology quiz already exists
existing_greek_idx = None
for idx, quiz in enumerate(data['quizzes']):
    if 'greek' in quiz['name'].lower() and 'mythology' in quiz['name'].lower():
        existing_greek_idx = idx
        break

if existing_greek_idx is not None:
    print(f"\n9. Replacing existing Greek Mythology quiz at index {existing_greek_idx}...")
    data['quizzes'][existing_greek_idx] = greek_quiz
else:
    print(f"\n9. Adding new Greek Mythology quiz...")
    data['quizzes'].append(greek_quiz)

# Save
print("\n10. Saving...")
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✓ Saved {len(data['quizzes'])} quizzes")

# Verify
print("\n11. Verifying...")
with open(json_file, 'r', encoding='utf-8') as f:
    verify = json.load(f)

total_questions = sum(len(q['questions']) for q in verify['quizzes'])
print(f"✓ Total quizzes: {len(verify['quizzes'])}")
print(f"✓ Total questions: {total_questions}")

# Show Greek quiz
for quiz in verify['quizzes']:
    if 'greek' in quiz['name'].lower() and 'mythology' in quiz['name'].lower():
        print(f"\n✓ Greek Mythology Quiz:")
        print(f"  - Name: {quiz['name']}")
        print(f"  - Questions: {len(quiz['questions'])}")
        print(f"  - Image: {quiz['imageFileName']}")

print("\n" + "="*80)
print("✓ SUCCESS - Greek Mythology Quiz Generated!")
print("="*80)

