import json
import uuid
import sys
from datetime import datetime

# Lire le fichier existant
try:
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier: {e}")
    sys.exit(1)

# Trouver le quiz Greek Mythology
greek_quiz = None
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

for quiz in quizzes:
    if isinstance(quiz, dict) and 'Greek Mythology' in quiz.get('name', ''):
        greek_quiz = quiz
        break

if not greek_quiz:
    print("Quiz Greek Mythology non trouvé!")
    sys.exit(1)

# Obtenir les questions existantes
existing_questions = set()
current_max_id = 0
for q in greek_quiz.get('questions', []):
    existing_questions.add(q.get('question', '').lower().strip())
    current_max_id = max(current_max_id, q.get('id', 0))

print(f"Questions existantes: {len(existing_questions)}")
print(f"ID maximum actuel: {current_max_id}")

# Dernières questions pour atteindre 500
new_questions = [
    # Arès
    {
        "question": "What was Ares the god of?",
        "options": ["War and bloodshed", "Wisdom and strategy", "Love", "Death"],
        "answer": "War and bloodshed"
    },
    {
        "question": "Who were Ares's parents?",
        "options": ["Zeus and Hera", "Zeus and Leto", "Poseidon and Amphitrite", "Cronus and Rhea"],
        "answer": "Zeus and Hera"
    },
    {
        "question": "Which goddess did Ares love?",
        "options": ["Aphrodite", "Athena", "Artemis", "Hera"],
        "answer": "Aphrodite"
    },
    {
        "question": "How were Ares and Aphrodite's affair discovered?",
        "options": ["Helios told Hephaestus", "Zeus revealed it", "They were caught publicly", "Hera exposed them"],
        "answer": "Helios told Hephaestus"
    },
    {
        "question": "What did Hephaestus do when he learned of the affair?",
        "options": ["Trapped them in an invisible net", "Killed Ares", "Divorced Aphrodite", "Challenged Ares"],
        "answer": "Trapped them in an invisible net"
    },
    {
        "question": "What was Ares's Roman name?",
        "options": ["Mars", "Jupiter", "Mercury", "Vulcan"],
        "answer": "Mars"
    },
    # Héphaïstos
    {
        "question": "What was Hephaestus the god of?",
        "options": ["Fire, metalworking, and crafts", "War", "Wine", "Music"],
        "answer": "Fire, metalworking, and crafts"
    },
    {
        "question": "What physical characteristic did Hephaestus have?",
        "options": ["He was lame/crippled", "He was blind", "He was deaf", "He was mute"],
        "answer": "He was lame/crippled"
    },
    {
        "question": "Why was Hephaestus lame?",
        "options": ["Zeus or Hera threw him from Olympus", "Born that way", "Injured in battle", "Cursed"],
        "answer": "Zeus or Hera threw him from Olympus"
    },
    {
        "question": "Where did Hephaestus have his workshop?",
        "options": ["Under a volcano", "On Mount Olympus", "In Athens", "In the Underworld"],
        "answer": "Under a volcano"
    },
    {
        "question": "Who were Hephaestus's assistants?",
        "options": ["Cyclopes", "Centaurs", "Satyrs", "Nymphs"],
        "answer": "Cyclopes"
    },
    {
        "question": "What famous objects did Hephaestus create?",
        "options": ["Zeus's thunderbolts, Achilles's armor, Pandora", "The Golden Fleece", "Medusa's head", "The Minotaur's labyrinth"],
        "answer": "Zeus's thunderbolts, Achilles's armor, Pandora"
    },
    {
        "question": "Who was Pandora?",
        "options": ["The first mortal woman", "A goddess", "A nymph", "A Titaness"],
        "answer": "The first mortal woman"
    },
    {
        "question": "Who created Pandora?",
        "options": ["Hephaestus on Zeus's orders", "Zeus alone", "Athena", "Prometheus"],
        "answer": "Hephaestus on Zeus's orders"
    },
    {
        "question": "What did Pandora's box (jar) contain?",
        "options": ["All the evils of the world", "Treasures", "Hope alone", "Ambrosia"],
        "answer": "All the evils of the world"
    },
    {
        "question": "What remained in Pandora's box after she opened it?",
        "options": ["Hope", "Love", "Death", "Nothing"],
        "answer": "Hope"
    },
    {
        "question": "Who did Pandora marry?",
        "options": ["Epimetheus", "Prometheus", "Zeus", "Hephaestus"],
        "answer": "Epimetheus"
    },
    {
        "question": "What was Epimetheus known for?",
        "options": ["Acting before thinking (opposite of his brother Prometheus)", "Wisdom", "Strength", "Prophecy"],
        "answer": "Acting before thinking (opposite of his brother Prometheus)"
    },
    # Hermès
    {
        "question": "What was Hermes the god of?",
        "options": ["Travelers, thieves, messengers, commerce", "War", "Love", "Sea"],
        "answer": "Travelers, thieves, messengers, commerce"
    },
    {
        "question": "What did Hermes steal on the day he was born?",
        "options": ["Apollo's cattle", "Zeus's thunderbolt", "Hera's crown", "Poseidon's trident"],
        "answer": "Apollo's cattle"
    },
    {
        "question": "What instrument did Hermes invent?",
        "options": ["The lyre", "The flute", "The harp", "The pan pipes"],
        "answer": "The lyre"
    },
    {
        "question": "What did Hermes trade to Apollo for the cattle?",
        "options": ["The lyre", "His sandals", "A staff", "Gold"],
        "answer": "The lyre"
    },
    {
        "question": "What staff did Hermes carry?",
        "options": ["Caduceus", "Trident", "Thunderbolt", "Aegis"],
        "answer": "Caduceus"
    },
    {
        "question": "What was wrapped around Hermes's caduceus?",
        "options": ["Two serpents", "Vines", "Gold thread", "Lightning"],
        "answer": "Two serpents"
    },
    {
        "question": "What role did Hermes play for the dead?",
        "options": ["Guided souls to the Underworld", "Judged them", "Punished them", "Resurrected them"],
        "answer": "Guided souls to the Underworld"
    },
    {
        "question": "What was Hermes's Roman name?",
        "options": ["Mercury", "Mars", "Jupiter", "Neptune"],
        "answer": "Mercury"
    },
    # Déméter et Hadès
    {
        "question": "What was Demeter the goddess of?",
        "options": ["Agriculture, harvest, and fertility", "Love", "War", "Wisdom"],
        "answer": "Agriculture, harvest, and fertility"
    },
    {
        "question": "What happened to crops when Persephone was in the Underworld?",
        "options": ["Nothing grew (winter)", "They flourished", "They burned", "They turned to stone"],
        "answer": "Nothing grew (winter)"
    },
    {
        "question": "What happened to crops when Persephone returned to Earth?",
        "options": ["Spring and growth returned", "They died", "Nothing changed", "They turned gold"],
        "answer": "Spring and growth returned"
    },
    {
        "question": "What was Hades the god of?",
        "options": ["The Underworld and the dead", "Death itself", "War", "Darkness"],
        "answer": "The Underworld and the dead"
    },
    {
        "question": "What was Hades's Roman name?",
        "options": ["Pluto", "Jupiter", "Mars", "Neptune"],
        "answer": "Pluto"
    },
    {
        "question": "Was Hades considered evil?",
        "options": ["No, just stern and fair", "Yes, very evil", "Sometimes", "He was neutral"],
        "answer": "No, just stern and fair"
    },
    {
        "question": "Why did people fear to say Hades's name?",
        "options": ["They feared attracting his attention and death", "He was evil", "It was forbidden", "It brought bad luck"],
        "answer": "They feared attracting his attention and death"
    },
    # Hestia
    {
        "question": "What was Hestia the goddess of?",
        "options": ["The hearth, home, and family", "Love", "War", "Wisdom"],
        "answer": "The hearth, home, and family"
    },
    {
        "question": "What vow did Hestia take?",
        "options": ["To remain a virgin forever", "To protect Olympus", "To punish mortals", "To serve Zeus"],
        "answer": "To remain a virgin forever"
    },
    {
        "question": "Which god gave up his Olympian throne for Dionysus?",
        "options": ["Hestia", "Hades", "Pan", "Hermes"],
        "answer": "Hestia"
    },
    {
        "question": "What was Hestia's Roman name?",
        "options": ["Vesta", "Diana", "Minerva", "Venus"],
        "answer": "Vesta"
    },
    {
        "question": "What were Vesta's priestesses called in Rome?",
        "options": ["Vestal Virgins", "Sibyls", "Pythias", "Vestals"],
        "answer": "Vestal Virgins"
    },
    # Atalante
    {
        "question": "What was Atalanta famous for?",
        "options": ["Being a swift huntress", "Her beauty", "Her wisdom", "Her strength"],
        "answer": "Being a swift huntress"
    },
    {
        "question": "What famous hunt did Atalanta participate in?",
        "options": ["The Calydonian Boar hunt", "The Nemean Lion", "The Erymanthian Boar", "The Stymphalian Birds"],
        "answer": "The Calydonian Boar hunt"
    },
    {
        "question": "Who sent the Calydonian Boar?",
        "options": ["Artemis (in anger)", "Zeus", "Hera", "Athena"],
        "answer": "Artemis (in anger)"
    },
    {
        "question": "How could a suitor win Atalanta's hand in marriage?",
        "options": ["Beat her in a footrace", "Defeat her in combat", "Solve her riddle", "Bring her a gift"],
        "answer": "Beat her in a footrace"
    },
    {
        "question": "What happened to suitors who lost the race against Atalanta?",
        "options": ["They were killed", "They were banished", "They became servants", "Nothing"],
        "answer": "They were killed"
    },
    {
        "question": "Who finally beat Atalanta in a race?",
        "options": ["Hippomenes (or Melanion)", "Heracles", "Theseus", "Perseus"],
        "answer": "Hippomenes (or Melanion)"
    },
    {
        "question": "How did Hippomenes win the race?",
        "options": ["Dropped golden apples that Atalanta stopped to pick up", "Ran faster", "Cheated", "Aphrodite helped him run"],
        "answer": "Dropped golden apples that Atalanta stopped to pick up"
    },
    {
        "question": "Who gave Hippomenes the golden apples?",
        "options": ["Aphrodite", "Athena", "Hera", "Artemis"],
        "answer": "Aphrodite"
    },
    {
        "question": "What happened to Atalanta and Hippomenes?",
        "options": ["Turned into lions for desecrating a temple", "Lived happily", "Died in battle", "Were separated"],
        "answer": "Turned into lions for desecrating a temple"
    },
    # Pygmalion et Galatea
    {
        "question": "Who was Pygmalion?",
        "options": ["A sculptor who fell in love with his statue", "A king", "A god", "A hero"],
        "answer": "A sculptor who fell in love with his statue"
    },
    {
        "question": "What was the name of Pygmalion's statue?",
        "options": ["Galatea", "Aphrodite", "Helen", "Psyche"],
        "answer": "Galatea"
    },
    {
        "question": "Which goddess brought Pygmalion's statue to life?",
        "options": ["Aphrodite", "Athena", "Hera", "Artemis"],
        "answer": "Aphrodite"
    },
    # Mélèagre
    {
        "question": "Who was Meleager?",
        "options": ["The hero who killed the Calydonian Boar", "A Trojan prince", "An Argonaut", "A centaur"],
        "answer": "The hero who killed the Calydonian Boar"
    },
    {
        "question": "What controlled Meleager's life span?",
        "options": ["A magical log", "A thread", "His sword", "A prophecy"],
        "answer": "A magical log"
    },
    {
        "question": "Who kept the log that controlled Meleager's life?",
        "options": ["His mother Althaea", "The Fates", "Zeus", "A witch"],
        "answer": "His mother Althaea"
    },
    {
        "question": "Why did Meleager's mother burn the log?",
        "options": ["He killed her brothers", "He betrayed her", "She was cursed", "Zeus commanded it"],
        "answer": "He killed her brothers"
    },
    {
        "question": "What happened when the log was burned?",
        "options": ["Meleager died", "He became immortal", "He was cursed", "Nothing"],
        "answer": "Meleager died"
    },
    # Phaéton
    {
        "question": "Who was Phaethon's father?",
        "options": ["Helios, the sun god", "Apollo", "Zeus", "Hermes"],
        "answer": "Helios, the sun god"
    },
    {
        "question": "What did Phaethon ask his father for?",
        "options": ["To drive the sun chariot", "Immortality", "Wealth", "Power"],
        "answer": "To drive the sun chariot"
    },
    {
        "question": "What happened when Phaethon drove the sun chariot?",
        "options": ["He lost control and nearly burned the Earth", "He succeeded", "He disappeared", "He became a god"],
        "answer": "He lost control and nearly burned the Earth"
    },
    {
        "question": "How did Zeus stop Phaethon?",
        "options": ["Struck him down with a thunderbolt", "Took away the chariot", "Asked Helios to stop him", "Imprisoned him"],
        "answer": "Struck him down with a thunderbolt"
    },
    # Autres mythes
    {
        "question": "Who was condemned to lie in a bed of fire in Tartarus?",
        "options": ["Ixion", "Sisyphus", "Tantalus", "Prometheus"],
        "answer": "Ixion"
    },
    {
        "question": "What was Ixion's crime?",
        "options": ["Tried to seduce Hera", "Killed his family", "Stole from the gods", "Betrayed Zeus"],
        "answer": "Tried to seduce Hera"
    },
    {
        "question": "What did Zeus create to trick Ixion?",
        "options": ["A cloud shaped like Hera", "An illusion", "A fake Hera", "Nothing"],
        "answer": "A cloud shaped like Hera"
    },
    {
        "question": "What race was born from Ixion and the cloud?",
        "options": ["Centaurs", "Minotaurs", "Giants", "Cyclopes"],
        "answer": "Centaurs"
    },
    {
        "question": "Who was the hero who could run on water?",
        "options": ["Euphemus", "Hermes", "Perseus", "Achilles"],
        "answer": "Euphemus"
    },
    {
        "question": "Who was the Argonaut with the sharpest eyesight?",
        "options": ["Lynceus", "Castor", "Polydeuces", "Orpheus"],
        "answer": "Lynceus"
    },
    {
        "question": "Who were the Boreads?",
        "options": ["Winged sons of Boreas, the North Wind", "Giants", "Cyclopes", "Centaurs"],
        "answer": "Winged sons of Boreas, the North Wind"
    },
    {
        "question": "What was Lamia?",
        "options": ["A child-eating monster", "A sea creature", "A goddess", "A nymph"],
        "answer": "A child-eating monster"
    },
    {
        "question": "Why did Lamia become a monster?",
        "options": ["Hera's curse after Zeus loved her", "Born that way", "Chose to be one", "Cursed by Athena"],
        "answer": "Hera's curse after Zeus loved her"
    },
    {
        "question": "What were Empusa?",
        "options": ["Shape-shifting demons", "Nymphs", "Furies", "Harpies"],
        "answer": "Shape-shifting demons"
    },
]

print(f"\nNombre de nouvelles questions préparées: {len(new_questions)}")

# Filtrer les questions qui existent déjà
filtered_questions = []
duplicate_count = 0
for q in new_questions:
    question_lower = q["question"].lower().strip()
    if question_lower not in existing_questions:
        filtered_questions.append(q)
        existing_questions.add(question_lower)
    else:
        duplicate_count += 1

print(f"Questions en double trouvées: {duplicate_count}")
print(f"Nombre de nouvelles questions uniques: {len(filtered_questions)}")

# Ajouter les nouvelles questions avec ID et UUID
next_id = current_max_id + 1
for q in filtered_questions:
    q["id"] = next_id
    q["uuid"] = str(uuid.uuid4())
    q["difficulty_level"] = 1
    next_id += 1
    greek_quiz["questions"].append(q)

print(f"\nNouvelles questions ajoutées au quiz Greek Mythology")
print(f"Nombre total de questions: {len(greek_quiz['questions'])}")
print(f"Objectif de 500 questions: {'ATTEINT ✓' if len(greek_quiz['questions']) >= 500 else 'Presque là!'}")

# Sauvegarder le fichier avec backup
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_file = f"quiz-questions-backup-{timestamp}.json"

try:
    # Backup
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nBackup créé: {backup_file}")

    # Sauvegarder la version mise à jour
    with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Fichier quiz-questions.json mis à jour avec succès!")

except Exception as e:
    print(f"Erreur lors de la sauvegarde: {e}")
    sys.exit(1)

