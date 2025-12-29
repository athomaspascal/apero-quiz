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
greek_index = -1
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

for i, quiz in enumerate(quizzes):
    if isinstance(quiz, dict) and 'Greek Mythology' in quiz.get('name', ''):
        greek_quiz = quiz
        greek_index = i
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

# Nouvelles questions à ajouter - Partie 2
new_questions = [
    # Les Gorgones
    {
        "question": "How many Gorgons were there?",
        "options": ["Three", "Two", "Five", "Seven"],
        "answer": "Three"
    },
    {
        "question": "Which Gorgon was mortal?",
        "options": ["Medusa", "Stheno", "Euryale", "All of them"],
        "answer": "Medusa"
    },
    {
        "question": "What were the names of Medusa's immortal sisters?",
        "options": ["Stheno and Euryale", "Scylla and Charybdis", "Echo and Ariadne", "Thalia and Melpomene"],
        "answer": "Stheno and Euryale"
    },
    {
        "question": "What happened to those who looked at Medusa directly?",
        "options": ["They turned to stone", "They died", "They went blind", "They went mad"],
        "answer": "They turned to stone"
    },
    {
        "question": "What sprang from Medusa's neck when Perseus beheaded her?",
        "options": ["Pegasus and Chrysaor", "Blood and snakes", "Fire and smoke", "Nothing"],
        "answer": "Pegasus and Chrysaor"
    },
    {
        "question": "Who was Chrysaor?",
        "options": ["A giant with a golden sword", "A winged horse", "A dragon", "A hero"],
        "answer": "A giant with a golden sword"
    },
    {
        "question": "What did Perseus do with Medusa's head?",
        "options": ["Gave it to Athena", "Kept it as a weapon", "Buried it", "Destroyed it"],
        "answer": "Gave it to Athena"
    },
    # Les Harpies
    {
        "question": "What were Harpies?",
        "options": ["Winged spirits with women's faces and bird bodies", "Three-headed dogs", "Snake-haired monsters", "Fire-breathing creatures"],
        "answer": "Winged spirits with women's faces and bird bodies"
    },
    {
        "question": "What did Harpies do?",
        "options": ["Stole food and caused famine", "Sang deadly songs", "Turned people to stone", "Guarded treasures"],
        "answer": "Stole food and caused famine"
    },
    {
        "question": "Who was tormented by Harpies stealing his food?",
        "options": ["Phineus", "Tantalus", "Sisyphus", "Prometheus"],
        "answer": "Phineus"
    },
    {
        "question": "Who drove away the Harpies from Phineus?",
        "options": ["The Boreads (sons of Boreas)", "Jason", "Heracles", "Perseus"],
        "answer": "The Boreads (sons of Boreas)"
    },
    # Amazones
    {
        "question": "What were the Amazons?",
        "options": ["A nation of warrior women", "Goddesses", "Monsters", "Priestesses"],
        "answer": "A nation of warrior women"
    },
    {
        "question": "Who was the most famous Amazon queen?",
        "options": ["Hippolyta", "Penthesilea", "Antiope", "Thalestris"],
        "answer": "Hippolyta"
    },
    {
        "question": "Which Amazon queen fought in the Trojan War?",
        "options": ["Penthesilea", "Hippolyta", "Antiope", "Thalestris"],
        "answer": "Penthesilea"
    },
    {
        "question": "Who killed Penthesilea?",
        "options": ["Achilles", "Hector", "Ajax", "Odysseus"],
        "answer": "Achilles"
    },
    {
        "question": "What happened to Achilles after he killed Penthesilea?",
        "options": ["He fell in love with her after her death", "He was cursed", "He went mad", "He felt no remorse"],
        "answer": "He fell in love with her after her death"
    },
    # Les Grées
    {
        "question": "How many Graeae (Grey Sisters) were there?",
        "options": ["Three", "Two", "Five", "Seven"],
        "answer": "Three"
    },
    {
        "question": "What did the Graeae share among them?",
        "options": ["One eye and one tooth", "One heart", "One brain", "One voice"],
        "answer": "One eye and one tooth"
    },
    {
        "question": "Who stole the eye of the Graeae?",
        "options": ["Perseus", "Heracles", "Theseus", "Jason"],
        "answer": "Perseus"
    },
    {
        "question": "Why did Perseus steal the Graeae's eye?",
        "options": ["To force them to tell him where Medusa was", "To blind them", "As a trophy", "For Athena"],
        "answer": "To force them to tell him where Medusa was"
    },
    # Nymphes
    {
        "question": "What were Nymphs?",
        "options": ["Minor female nature deities", "Goddesses", "Mortals", "Monsters"],
        "answer": "Minor female nature deities"
    },
    {
        "question": "What were tree nymphs called?",
        "options": ["Dryads", "Naiads", "Nereids", "Oreads"],
        "answer": "Dryads"
    },
    {
        "question": "What were water nymphs called?",
        "options": ["Naiads", "Dryads", "Oreads", "Oceanids"],
        "answer": "Naiads"
    },
    {
        "question": "What were sea nymphs called?",
        "options": ["Nereids", "Naiads", "Dryads", "Oreads"],
        "answer": "Nereids"
    },
    {
        "question": "What were mountain nymphs called?",
        "options": ["Oreads", "Naiads", "Dryads", "Nereids"],
        "answer": "Oreads"
    },
    {
        "question": "How many Nereids were there?",
        "options": ["Fifty", "Seven", "Nine", "Twelve"],
        "answer": "Fifty"
    },
    {
        "question": "Who were the parents of the Nereids?",
        "options": ["Nereus and Doris", "Poseidon and Amphitrite", "Oceanus and Tethys", "Zeus and Thetis"],
        "answer": "Nereus and Doris"
    },
    {
        "question": "Which Nereid was the mother of Achilles?",
        "options": ["Thetis", "Amphitrite", "Galatea", "Doris"],
        "answer": "Thetis"
    },
    {
        "question": "Who was Peleus?",
        "options": ["The mortal father of Achilles", "A Trojan prince", "A god", "A centaur"],
        "answer": "The mortal father of Achilles"
    },
    {
        "question": "How did Thetis try to make Achilles immortal as a baby?",
        "options": ["Dipped him in the River Styx", "Fed him ambrosia", "Bathed him in fire", "Prayed to Zeus"],
        "answer": "Dipped him in the River Styx"
    },
    {
        "question": "What part of Achilles didn't touch the Styx?",
        "options": ["His heel", "His head", "His heart", "His hand"],
        "answer": "His heel"
    },
    # Evénements mythologiques
    {
        "question": "What caused the conflict that led to the Trojan War?",
        "options": ["The Judgment of Paris", "The death of Agamemnon", "The theft of the Golden Fleece", "A prophecy"],
        "answer": "The Judgment of Paris"
    },
    {
        "question": "Which goddess wasn't invited to the wedding of Peleus and Thetis?",
        "options": ["Eris (goddess of discord)", "Hera", "Aphrodite", "Artemis"],
        "answer": "Eris (goddess of discord)"
    },
    {
        "question": "What did Eris throw at the wedding?",
        "options": ["A golden apple inscribed 'to the fairest'", "A curse", "A lightning bolt", "A prophecy"],
        "answer": "A golden apple inscribed 'to the fairest'"
    },
    {
        "question": "Which three goddesses claimed the golden apple?",
        "options": ["Hera, Athena, and Aphrodite", "Hera, Demeter, and Artemis", "Aphrodite, Artemis, and Hestia", "Athena, Artemis, and Hera"],
        "answer": "Hera, Athena, and Aphrodite"
    },
    {
        "question": "Who was chosen to judge which goddess was fairest?",
        "options": ["Paris", "Zeus", "Hermes", "Apollo"],
        "answer": "Paris"
    },
    {
        "question": "What did Hera offer Paris?",
        "options": ["Power and kingdoms", "Wisdom", "The most beautiful woman", "Immortality"],
        "answer": "Power and kingdoms"
    },
    {
        "question": "What did Athena offer Paris?",
        "options": ["Wisdom and victory in battle", "Power", "Love", "Wealth"],
        "answer": "Wisdom and victory in battle"
    },
    {
        "question": "What did Aphrodite offer Paris?",
        "options": ["The most beautiful woman in the world", "Power", "Wisdom", "Immortality"],
        "answer": "The most beautiful woman in the world"
    },
    {
        "question": "Who did Paris choose as the fairest?",
        "options": ["Aphrodite", "Hera", "Athena", "He couldn't decide"],
        "answer": "Aphrodite"
    },
    # La Toison d'Or
    {
        "question": "Why did Jason seek the Golden Fleece?",
        "options": ["To reclaim his throne from his uncle Pelias", "For glory", "To win a bride", "Zeus commanded it"],
        "answer": "To reclaim his throne from his uncle Pelias"
    },
    {
        "question": "Who was Jason's uncle who usurped his throne?",
        "options": ["Pelias", "Aeson", "Creon", "Aeetes"],
        "answer": "Pelias"
    },
    {
        "question": "Who was the king of Colchis?",
        "options": ["Aeetes", "Pelias", "Aeson", "Creon"],
        "answer": "Aeetes"
    },
    {
        "question": "Who was Medea's father?",
        "options": ["Aeetes", "Pelias", "Zeus", "Helios"],
        "answer": "Aeetes"
    },
    {
        "question": "What tasks did Aeetes set for Jason?",
        "options": ["Yoke fire-breathing bulls and sow dragon's teeth", "Kill a dragon", "Solve a riddle", "Fight warriors"],
        "answer": "Yoke fire-breathing bulls and sow dragon's teeth"
    },
    {
        "question": "What grew from the dragon's teeth Jason sowed?",
        "options": ["Armed warriors", "Dragons", "Trees", "Monsters"],
        "answer": "Armed warriors"
    },
    {
        "question": "How did Jason defeat the warriors that grew from dragon's teeth?",
        "options": ["Made them fight each other by throwing a stone among them", "Killed them all", "Used magic", "Ran away"],
        "answer": "Made them fight each other by throwing a stone among them"
    },
    {
        "question": "What happened to Medea after she helped Jason?",
        "options": ["She fled with him to Greece", "She was imprisoned", "She was killed", "She stayed in Colchis"],
        "answer": "She fled with him to Greece"
    },
    {
        "question": "What terrible thing did Medea do to help Jason escape?",
        "options": ["Killed and dismembered her own brother", "Killed her father", "Burned the city", "Caused a plague"],
        "answer": "Killed and dismembered her own brother"
    },
    {
        "question": "Who did Jason eventually abandon Medea for?",
        "options": ["Glauce (or Creusa)", "Ariadne", "Helen", "Andromeda"],
        "answer": "Glauce (or Creusa)"
    },
    {
        "question": "What did Medea do in revenge?",
        "options": ["Killed Jason's new bride and her own children", "Killed Jason", "Cursed Jason", "Left peacefully"],
        "answer": "Killed Jason's new bride and her own children"
    },
    # Thésée et Athènes
    {
        "question": "Who was Theseus's father?",
        "options": ["Aegeus (mortal) and possibly Poseidon (divine)", "Zeus", "Heracles", "Minos"],
        "answer": "Aegeus (mortal) and possibly Poseidon (divine)"
    },
    {
        "question": "What did Theseus have to lift to prove his identity?",
        "options": ["A rock hiding his father's sword and sandals", "A boulder", "A golden fleece", "A shield"],
        "answer": "A rock hiding his father's sword and sandals"
    },
    {
        "question": "What color sail did Theseus's ship have when he left for Crete?",
        "options": ["Black", "White", "Red", "Blue"],
        "answer": "Black"
    },
    {
        "question": "What was Theseus supposed to do if he succeeded?",
        "options": ["Change the sail to white", "Light a beacon", "Send a messenger", "Return quickly"],
        "answer": "Change the sail to white"
    },
    {
        "question": "What did Theseus forget to do on his return?",
        "options": ["Change the black sail to white", "Tell Ariadne", "Thank the gods", "Bring gifts"],
        "answer": "Change the black sail to white"
    },
    {
        "question": "What happened to Aegeus when he saw the black sail?",
        "options": ["He threw himself into the sea in grief", "He died of a heart attack", "He went mad", "He was murdered"],
        "answer": "He threw himself into the sea in grief"
    },
    {
        "question": "What sea is named after Aegeus?",
        "options": ["The Aegean Sea", "The Adriatic Sea", "The Ionian Sea", "The Mediterranean Sea"],
        "answer": "The Aegean Sea"
    },
    {
        "question": "What happened to Ariadne after Theseus abandoned her?",
        "options": ["Dionysus married her", "She died", "She returned home", "She became a goddess on her own"],
        "answer": "Dionysus married her"
    },
    {
        "question": "Where did Theseus abandon Ariadne?",
        "options": ["The island of Naxos", "Crete", "Athens", "Delos"],
        "answer": "The island of Naxos"
    },
    # Persée
    {
        "question": "Who was Perseus's mother?",
        "options": ["Danae", "Andromeda", "Leda", "Europa"],
        "answer": "Danae"
    },
    {
        "question": "Why was Danae imprisoned by her father?",
        "options": ["A prophecy said her son would kill him", "She was disobedient", "She was cursed", "For her protection"],
        "answer": "A prophecy said her son would kill him"
    },
    {
        "question": "Who was Danae's father?",
        "options": ["Acrisius", "Aegeus", "Aeson", "Aeetes"],
        "answer": "Acrisius"
    },
    {
        "question": "How did Danae and baby Perseus escape the tower?",
        "options": ["Cast into the sea in a chest", "They climbed down", "Zeus rescued them", "They flew"],
        "answer": "Cast into the sea in a chest"
    },
    {
        "question": "Who found Danae and Perseus?",
        "options": ["Dictys, a fisherman", "A king", "Athena", "No one, they survived alone"],
        "answer": "Dictys, a fisherman"
    },
    {
        "question": "Who wanted to marry Danae and sent Perseus on a dangerous quest?",
        "options": ["Polydectes", "Acrisius", "Dictys", "Aegeus"],
        "answer": "Polydectes"
    },
    {
        "question": "What gift did Athena give Perseus?",
        "options": ["A polished shield", "A sword", "Winged sandals", "A helmet"],
        "answer": "A polished shield"
    },
    {
        "question": "What gift did Hermes give Perseus?",
        "options": ["A sword and winged sandals", "A shield", "A helmet", "A rope"],
        "answer": "A sword and winged sandals"
    },
    {
        "question": "What gift did Hades give Perseus?",
        "options": ["A helmet of invisibility", "A sword", "A shield", "Winged sandals"],
        "answer": "A helmet of invisibility"
    },
    {
        "question": "Who did Perseus rescue from a sea monster?",
        "options": ["Andromeda", "Ariadne", "Psyche", "Helen"],
        "answer": "Andromeda"
    },
    {
        "question": "Why was Andromeda chained to a rock?",
        "options": ["Her mother boasted she was more beautiful than the Nereids", "She angered Athena", "A prophecy", "A curse"],
        "answer": "Her mother boasted she was more beautiful than the Nereids"
    },
    {
        "question": "Who was Andromeda's mother?",
        "options": ["Cassiopeia", "Jocasta", "Hecuba", "Clytemnestra"],
        "answer": "Cassiopeia"
    },
    {
        "question": "What did Perseus do with Medusa's head to save Andromeda?",
        "options": ["Turned the sea monster to stone", "Scared it away", "Used it as a weapon", "Nothing, he fought with a sword"],
        "answer": "Turned the sea monster to stone"
    },
    {
        "question": "Did the prophecy about Acrisius come true?",
        "options": ["Yes, Perseus accidentally killed him with a discus", "No, it was prevented", "Yes, Perseus killed him intentionally", "Yes, he died of fright"],
        "answer": "Yes, Perseus accidentally killed him with a discus"
    },
    # Dionysos
    {
        "question": "Who was Dionysus's mortal mother?",
        "options": ["Semele", "Io", "Europa", "Danae"],
        "answer": "Semele"
    },
    {
        "question": "How did Semele die?",
        "options": ["Saw Zeus in his true form and was incinerated", "Hera killed her", "In childbirth", "Poison"],
        "answer": "Saw Zeus in his true form and was incinerated"
    },
    {
        "question": "Who tricked Semele into asking to see Zeus's true form?",
        "options": ["Hera in disguise", "A Titan", "A mortal", "Herself"],
        "answer": "Hera in disguise"
    },
    {
        "question": "Where did Zeus hide the unborn Dionysus after Semele died?",
        "options": ["In his thigh", "In Hera's garden", "On Mount Olympus", "With nymphs"],
        "answer": "In his thigh"
    },
    {
        "question": "Who raised Dionysus?",
        "options": ["Nymphs and satyrs", "Hera", "Athena", "Hermes"],
        "answer": "Nymphs and satyrs"
    },
    {
        "question": "What did Dionysus discover?",
        "options": ["Wine-making", "Music", "Theater", "Agriculture"],
        "answer": "Wine-making"
    },
    {
        "question": "What were Dionysus's female followers called?",
        "options": ["Maenads or Bacchantes", "Amazons", "Nymphs", "Furies"],
        "answer": "Maenads or Bacchantes"
    },
    {
        "question": "What were Maenads known for?",
        "options": ["Frenzied ecstatic dancing and rituals", "Wisdom", "Fighting", "Prophecy"],
        "answer": "Frenzied ecstatic dancing and rituals"
    },
    {
        "question": "Who opposed Dionysus's worship in Thebes and was punished?",
        "options": ["Pentheus", "Oedipus", "Creon", "Lycurgus"],
        "answer": "Pentheus"
    },
    {
        "question": "How did Pentheus die?",
        "options": ["Torn apart by Maenads including his own mother", "Struck by lightning", "In battle", "Poison"],
        "answer": "Torn apart by Maenads including his own mother"
    },
    # Apollon
    {
        "question": "What was Apollo the god of (multiple domains)?",
        "options": ["Music, poetry, sun, prophecy, healing", "War and wisdom", "Sea and earthquakes", "Wine and celebration"],
        "answer": "Music, poetry, sun, prophecy, healing"
    },
    {
        "question": "Who was Apollo's twin sister?",
        "options": ["Artemis", "Athena", "Aphrodite", "Hera"],
        "answer": "Artemis"
    },
    {
        "question": "Where were Apollo and Artemis born?",
        "options": ["The island of Delos", "Mount Olympus", "Thebes", "Athens"],
        "answer": "The island of Delos"
    },
    {
        "question": "Why did Leto have trouble finding a place to give birth?",
        "options": ["Hera forbade any land to shelter her", "She was cursed", "Zeus abandoned her", "She was lost"],
        "answer": "Hera forbade any land to shelter her"
    },
    {
        "question": "What monster did Apollo kill as a young god?",
        "options": ["Python", "Medusa", "Chimera", "Hydra"],
        "answer": "Python"
    },
    {
        "question": "Where did Apollo kill Python?",
        "options": ["Delphi", "Athens", "Olympus", "Thebes"],
        "answer": "Delphi"
    },
    {
        "question": "What games did Apollo establish to commemorate his victory over Python?",
        "options": ["The Pythian Games", "The Olympic Games", "The Isthmian Games", "The Nemean Games"],
        "answer": "The Pythian Games"
    },
    {
        "question": "Who challenged Apollo to a music contest and lost?",
        "options": ["Marsyas the satyr", "Pan", "Orpheus", "Hermes"],
        "answer": "Marsyas the satyr"
    },
    {
        "question": "What was Marsyas's punishment for losing?",
        "options": ["Flayed alive", "Exiled", "Turned into an animal", "Lost his instrument"],
        "answer": "Flayed alive"
    },
    {
        "question": "Who else competed with Apollo in music?",
        "options": ["Pan", "Marsyas", "Orpheus", "Hermes"],
        "answer": "Pan"
    },
    {
        "question": "What punishment did King Midas receive for judging against Apollo?",
        "options": ["Donkey ears", "Golden touch", "Blindness", "Deafness"],
        "answer": "Donkey ears"
    },
    {
        "question": "Who was Apollo's greatest love who died young?",
        "options": ["Hyacinth", "Daphne", "Cassandra", "Coronis"],
        "answer": "Hyacinth"
    },
    {
        "question": "How did Hyacinth die?",
        "options": ["Struck by a discus thrown by Apollo (accident)", "Disease", "Murdered", "Old age"],
        "answer": "Struck by a discus thrown by Apollo (accident)"
    },
    {
        "question": "What flower sprang from Hyacinth's blood?",
        "options": ["Hyacinth", "Rose", "Lily", "Narcissus"],
        "answer": "Hyacinth"
    },
    {
        "question": "Who was the mother of Apollo's son Asclepius?",
        "options": ["Coronis", "Daphne", "Cassandra", "Marpessa"],
        "answer": "Coronis"
    },
    {
        "question": "Who was Asclepius?",
        "options": ["The god of medicine and healing", "A great warrior", "A wise king", "A prophet"],
        "answer": "The god of medicine and healing"
    },
    {
        "question": "Why did Zeus kill Asclepius?",
        "options": ["He brought people back from the dead", "He challenged Zeus", "He was too powerful", "He angered Hera"],
        "answer": "He brought people back from the dead"
    },
    # Artémis
    {
        "question": "What was Artemis the goddess of?",
        "options": ["Hunt, wilderness, and the moon", "Love", "War", "Wisdom"],
        "answer": "Hunt, wilderness, and the moon"
    },
    {
        "question": "What did Artemis value most?",
        "options": ["Her virginity and independence", "Power", "Beauty", "Wisdom"],
        "answer": "Her virginity and independence"
    },
    {
        "question": "Who accidentally saw Artemis bathing and was punished?",
        "options": ["Actaeon", "Orion", "Pan", "Endymion"],
        "answer": "Actaeon"
    },
    {
        "question": "What did Artemis turn Actaeon into?",
        "options": ["A stag", "A tree", "Stone", "A wolf"],
        "answer": "A stag"
    },
    {
        "question": "How did Actaeon die?",
        "options": ["Torn apart by his own hunting dogs", "Killed by Artemis", "Fell from a cliff", "Drowned"],
        "answer": "Torn apart by his own hunting dogs"
    },
    {
        "question": "Who was Artemis's hunting companion that she accidentally killed?",
        "options": ["Orion", "Actaeon", "Atalanta", "Meleager"],
        "answer": "Orion"
    },
    {
        "question": "What caused Artemis to kill Orion?",
        "options": ["Apollo tricked her (various versions exist)", "Orion attacked her", "Zeus commanded it", "An accident"],
        "answer": "Apollo tricked her (various versions exist)"
    },
    {
        "question": "What constellation represents Orion?",
        "options": ["Orion the Hunter", "Ursa Major", "Leo", "Scorpius"],
        "answer": "Orion the Hunter"
    },
    {
        "question": "Who boasted she was a better hunter than Artemis?",
        "options": ["Niobe (who boasted about her children, not hunting) - Actually it was Arachne for weaving", "Atalanta", "Medea", "Penthesilea"],
        "answer": "Niobe (who boasted about her children, not hunting) - Actually it was Arachne for weaving"
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
        print(f"Question en double ignorée: {q['question']}")

print(f"\nQuestions en double trouvées: {duplicate_count}")
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

