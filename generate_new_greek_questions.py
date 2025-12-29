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

# Nouvelles questions à ajouter
new_questions = [
    # Titans et généalogie
    {
        "question": "Who were the parents of Zeus?",
        "options": ["Cronus and Rhea", "Uranus and Gaia", "Oceanus and Tethys", "Hyperion and Theia"],
        "answer": "Cronus and Rhea"
    },
    {
        "question": "Which Titan was condemned to hold up the sky?",
        "options": ["Atlas", "Prometheus", "Epimetheus", "Cronus"],
        "answer": "Atlas"
    },
    {
        "question": "Who was the Titan of forethought who stole fire from the gods?",
        "options": ["Prometheus", "Epimetheus", "Atlas", "Cronus"],
        "answer": "Prometheus"
    },
    {
        "question": "What was the name of Zeus's first wife?",
        "options": ["Metis", "Hera", "Leto", "Demeter"],
        "answer": "Metis"
    },
    {
        "question": "Who was the primordial goddess of the Earth?",
        "options": ["Gaia", "Rhea", "Demeter", "Hera"],
        "answer": "Gaia"
    },
    {
        "question": "Which Titan was the god of the sun before Apollo?",
        "options": ["Helios", "Hyperion", "Apollo", "Ra"],
        "answer": "Helios"
    },
    {
        "question": "Who was the Titan goddess of memory and mother of the Muses?",
        "options": ["Mnemosyne", "Themis", "Tethys", "Phoebe"],
        "answer": "Mnemosyne"
    },
    {
        "question": "What was Cronus's Roman name?",
        "options": ["Saturn", "Jupiter", "Neptune", "Pluto"],
        "answer": "Saturn"
    },
    # Héros et leurs exploits
    {
        "question": "Which hero killed the Minotaur in the labyrinth?",
        "options": ["Theseus", "Perseus", "Heracles", "Jason"],
        "answer": "Theseus"
    },
    {
        "question": "Who gave Theseus the thread to escape the labyrinth?",
        "options": ["Ariadne", "Phaedra", "Medea", "Helen"],
        "answer": "Ariadne"
    },
    {
        "question": "Which hero flew too close to the sun with wax wings?",
        "options": ["Icarus", "Daedalus", "Perseus", "Bellerophon"],
        "answer": "Icarus"
    },
    {
        "question": "Who was the father of Icarus?",
        "options": ["Daedalus", "Minos", "Aegeus", "Poseidon"],
        "answer": "Daedalus"
    },
    {
        "question": "Which hero killed Medusa?",
        "options": ["Perseus", "Theseus", "Heracles", "Bellerophon"],
        "answer": "Perseus"
    },
    {
        "question": "What did Perseus use to avoid looking directly at Medusa?",
        "options": ["A polished shield", "A mirror", "Closed eyes", "A blindfold"],
        "answer": "A polished shield"
    },
    {
        "question": "Who led the Argonauts in search of the Golden Fleece?",
        "options": ["Jason", "Heracles", "Theseus", "Odysseus"],
        "answer": "Jason"
    },
    {
        "question": "Which sorceress helped Jason obtain the Golden Fleece?",
        "options": ["Medea", "Circe", "Calypso", "Ariadne"],
        "answer": "Medea"
    },
    {
        "question": "What was the name of Jason's ship?",
        "options": ["Argo", "Odyssey", "Olympus", "Pegasus"],
        "answer": "Argo"
    },
    {
        "question": "Which hero rode the winged horse Pegasus?",
        "options": ["Bellerophon", "Perseus", "Heracles", "Theseus"],
        "answer": "Bellerophon"
    },
    {
        "question": "What monster did Bellerophon kill while riding Pegasus?",
        "options": ["Chimera", "Medusa", "Minotaur", "Hydra"],
        "answer": "Chimera"
    },
    # Créatures mythologiques
    {
        "question": "How many heads did the Hydra have originally?",
        "options": ["Nine", "Three", "Seven", "Twelve"],
        "answer": "Nine"
    },
    {
        "question": "What happened when you cut off one of the Hydra's heads?",
        "options": ["Two more grew back", "It died", "It became stronger", "Nothing happened"],
        "answer": "Two more grew back"
    },
    {
        "question": "What creature had the head of a lion, body of a goat, and tail of a serpent?",
        "options": ["Chimera", "Sphinx", "Manticore", "Griffin"],
        "answer": "Chimera"
    },
    {
        "question": "What riddle did the Sphinx ask travelers?",
        "options": ["What walks on four legs in the morning, two at noon, and three in the evening?", "What has eyes but cannot see?", "What flies without wings?", "What runs but never walks?"],
        "answer": "What walks on four legs in the morning, two at noon, and three in the evening?"
    },
    {
        "question": "Who solved the Sphinx's riddle?",
        "options": ["Oedipus", "Theseus", "Perseus", "Heracles"],
        "answer": "Oedipus"
    },
    {
        "question": "What was the answer to the Sphinx's riddle?",
        "options": ["Man", "Time", "Life", "Death"],
        "answer": "Man"
    },
    {
        "question": "What creatures were half-man and half-horse?",
        "options": ["Centaurs", "Minotaurs", "Satyrs", "Cyclops"],
        "answer": "Centaurs"
    },
    {
        "question": "Who was the wisest and most civilized centaur?",
        "options": ["Chiron", "Nessus", "Pholus", "Eurytion"],
        "answer": "Chiron"
    },
    {
        "question": "What creatures were half-man and half-goat?",
        "options": ["Satyrs", "Centaurs", "Minotaurs", "Fauns"],
        "answer": "Satyrs"
    },
    {
        "question": "What were the singing creatures that lured sailors to their deaths?",
        "options": ["Sirens", "Harpies", "Gorgons", "Furies"],
        "answer": "Sirens"
    },
    {
        "question": "How many eyes did Cyclops have?",
        "options": ["One", "Two", "Three", "None"],
        "answer": "One"
    },
    {
        "question": "What was the name of the Cyclops that Odysseus blinded?",
        "options": ["Polyphemus", "Brontes", "Steropes", "Arges"],
        "answer": "Polyphemus"
    },
    {
        "question": "What creature guarded the entrance to the Underworld?",
        "options": ["Cerberus", "Chimera", "Hydra", "Sphinx"],
        "answer": "Cerberus"
    },
    {
        "question": "How many heads did Cerberus have?",
        "options": ["Three", "One", "Five", "Seven"],
        "answer": "Three"
    },
    # Dieux mineurs et nymphes
    {
        "question": "Who was the god of wine and revelry?",
        "options": ["Dionysus", "Apollo", "Hermes", "Pan"],
        "answer": "Dionysus"
    },
    {
        "question": "What was Dionysus's Roman name?",
        "options": ["Bacchus", "Liber", "Vulcan", "Mercury"],
        "answer": "Bacchus"
    },
    {
        "question": "Who was the god of the wild, shepherds, and flocks?",
        "options": ["Pan", "Dionysus", "Hermes", "Apollo"],
        "answer": "Pan"
    },
    {
        "question": "What instrument did Pan invent?",
        "options": ["Pan flute", "Lyre", "Harp", "Aulos"],
        "answer": "Pan flute"
    },
    {
        "question": "Who was the goddess of the rainbow?",
        "options": ["Iris", "Eos", "Selene", "Nike"],
        "answer": "Iris"
    },
    {
        "question": "Who was the goddess of victory?",
        "options": ["Nike", "Athena", "Artemis", "Hebe"],
        "answer": "Nike"
    },
    {
        "question": "Who was the goddess of the dawn?",
        "options": ["Eos", "Selene", "Iris", "Nyx"],
        "answer": "Eos"
    },
    {
        "question": "Who was the goddess of the moon?",
        "options": ["Selene", "Artemis", "Hecate", "Phoebe"],
        "answer": "Selene"
    },
    {
        "question": "Who was the goddess of the night?",
        "options": ["Nyx", "Hecate", "Selene", "Erebus"],
        "answer": "Nyx"
    },
    {
        "question": "Who was the god of sleep?",
        "options": ["Hypnos", "Morpheus", "Thanatos", "Erebus"],
        "answer": "Hypnos"
    },
    {
        "question": "Who was the god of dreams?",
        "options": ["Morpheus", "Hypnos", "Phantasus", "Thanatos"],
        "answer": "Morpheus"
    },
    {
        "question": "Who was the god of death?",
        "options": ["Thanatos", "Hades", "Hypnos", "Charon"],
        "answer": "Thanatos"
    },
    {
        "question": "Who was the ferryman of the Underworld?",
        "options": ["Charon", "Thanatos", "Hades", "Hermes"],
        "answer": "Charon"
    },
    {
        "question": "What payment did Charon require to ferry souls across the Styx?",
        "options": ["A coin", "A prayer", "A sacrifice", "Nothing"],
        "answer": "A coin"
    },
    # Guerre de Troie
    {
        "question": "What event started the Trojan War?",
        "options": ["The abduction of Helen", "The murder of Agamemnon", "The theft of the Golden Fleece", "The killing of Achilles"],
        "answer": "The abduction of Helen"
    },
    {
        "question": "Who abducted Helen of Troy?",
        "options": ["Paris", "Hector", "Achilles", "Agamemnon"],
        "answer": "Paris"
    },
    {
        "question": "What was Helen known as?",
        "options": ["The most beautiful woman in the world", "The wisest woman", "The strongest woman", "The fastest woman"],
        "answer": "The most beautiful woman in the world"
    },
    {
        "question": "Who was Helen's husband before Paris abducted her?",
        "options": ["Menelaus", "Agamemnon", "Odysseus", "Achilles"],
        "answer": "Menelaus"
    },
    {
        "question": "Who led the Greek forces in the Trojan War?",
        "options": ["Agamemnon", "Achilles", "Odysseus", "Menelaus"],
        "answer": "Agamemnon"
    },
    {
        "question": "Who was the greatest warrior on the Greek side?",
        "options": ["Achilles", "Hector", "Ajax", "Odysseus"],
        "answer": "Achilles"
    },
    {
        "question": "What was Achilles's only vulnerable spot?",
        "options": ["His heel", "His heart", "His head", "His back"],
        "answer": "His heel"
    },
    {
        "question": "Who killed Achilles?",
        "options": ["Paris", "Hector", "Agamemnon", "Priam"],
        "answer": "Paris"
    },
    {
        "question": "Who was the greatest Trojan warrior?",
        "options": ["Hector", "Paris", "Aeneas", "Priam"],
        "answer": "Hector"
    },
    {
        "question": "Who killed Hector?",
        "options": ["Achilles", "Paris", "Ajax", "Odysseus"],
        "answer": "Achilles"
    },
    {
        "question": "What stratagem ended the Trojan War?",
        "options": ["The Trojan Horse", "A peace treaty", "The death of Paris", "A siege"],
        "answer": "The Trojan Horse"
    },
    {
        "question": "Who devised the plan for the Trojan Horse?",
        "options": ["Odysseus", "Achilles", "Agamemnon", "Menelaus"],
        "answer": "Odysseus"
    },
    {
        "question": "Who was the king of Troy?",
        "options": ["Priam", "Hector", "Paris", "Aeneas"],
        "answer": "Priam"
    },
    # Odyssée
    {
        "question": "How long did Odysseus's journey home take?",
        "options": ["10 years", "7 years", "20 years", "5 years"],
        "answer": "10 years"
    },
    {
        "question": "What was the name of Odysseus's wife?",
        "options": ["Penelope", "Helen", "Andromache", "Hecuba"],
        "answer": "Penelope"
    },
    {
        "question": "What was the name of Odysseus's son?",
        "options": ["Telemachus", "Orestes", "Pylades", "Neoptolemus"],
        "answer": "Telemachus"
    },
    {
        "question": "What did Penelope weave to delay choosing a new husband?",
        "options": ["A shroud", "A tapestry", "A sail", "A dress"],
        "answer": "A shroud"
    },
    {
        "question": "Which goddess helped Odysseus throughout his journey?",
        "options": ["Athena", "Hera", "Aphrodite", "Artemis"],
        "answer": "Athena"
    },
    {
        "question": "Which god hindered Odysseus's journey?",
        "options": ["Poseidon", "Zeus", "Ares", "Hades"],
        "answer": "Poseidon"
    },
    {
        "question": "What did Odysseus tell Polyphemus his name was?",
        "options": ["Nobody", "Odysseus", "Zeus", "A god"],
        "answer": "Nobody"
    },
    {
        "question": "Which sorceress turned Odysseus's men into pigs?",
        "options": ["Circe", "Medea", "Calypso", "Hecate"],
        "answer": "Circe"
    },
    {
        "question": "How long did Calypso keep Odysseus on her island?",
        "options": ["7 years", "10 years", "5 years", "3 years"],
        "answer": "7 years"
    },
    {
        "question": "How did Odysseus's crew resist the Sirens' song?",
        "options": ["They plugged their ears with wax", "They sang louder", "They closed their eyes", "They tied themselves down"],
        "answer": "They plugged their ears with wax"
    },
    {
        "question": "What did Odysseus do to hear the Sirens' song without danger?",
        "options": ["Tied himself to the mast", "Plugged his ears", "Covered his eyes", "Stayed below deck"],
        "answer": "Tied himself to the mast"
    },
    {
        "question": "What were Scylla and Charybdis?",
        "options": ["A monster and a whirlpool", "Two monsters", "Two islands", "Two goddesses"],
        "answer": "A monster and a whirlpool"
    },
    {
        "question": "How many heads did Scylla have?",
        "options": ["Six", "Three", "Nine", "Twelve"],
        "answer": "Six"
    },
    # Objets magiques et lieux
    {
        "question": "What gave Hermes the ability to fly?",
        "options": ["Winged sandals", "A magic cloak", "Feathered wings", "A chariot"],
        "answer": "Winged sandals"
    },
    {
        "question": "What was the name of Poseidon's weapon?",
        "options": ["Trident", "Sword", "Spear", "Hammer"],
        "answer": "Trident"
    },
    {
        "question": "What was the name of Zeus's weapon?",
        "options": ["Thunderbolt", "Trident", "Sword", "Spear"],
        "answer": "Thunderbolt"
    },
    {
        "question": "What did Hades use to become invisible?",
        "options": ["A helmet of invisibility", "A magic ring", "A cloak", "A spell"],
        "answer": "A helmet of invisibility"
    },
    {
        "question": "What instrument did Apollo play?",
        "options": ["Lyre", "Flute", "Harp", "Pan flute"],
        "answer": "Lyre"
    },
    {
        "question": "Where did the gods live?",
        "options": ["Mount Olympus", "Mount Parnassus", "Mount Vesuvius", "Mount Etna"],
        "answer": "Mount Olympus"
    },
    {
        "question": "What was the name of the paradise where heroes went after death?",
        "options": ["Elysium", "Olympus", "Tartarus", "Asphodel"],
        "answer": "Elysium"
    },
    {
        "question": "What was the name of the pit of torment in the Underworld?",
        "options": ["Tartarus", "Asphodel", "Elysium", "Styx"],
        "answer": "Tartarus"
    },
    {
        "question": "What river did souls cross to enter the Underworld?",
        "options": ["Styx", "Lethe", "Acheron", "Cocytus"],
        "answer": "Styx"
    },
    {
        "question": "What river caused forgetfulness when drunk?",
        "options": ["Lethe", "Styx", "Acheron", "Cocytus"],
        "answer": "Lethe"
    },
    {
        "question": "Where was the Oracle of Apollo located?",
        "options": ["Delphi", "Olympia", "Athens", "Corinth"],
        "answer": "Delphi"
    },
    {
        "question": "What was the Oracle of Delphi also known as?",
        "options": ["Pythia", "Sibyl", "Cassandra", "Medea"],
        "answer": "Pythia"
    },
    # Mythes d'amour et de transformation
    {
        "question": "Who fell in love with his own reflection?",
        "options": ["Narcissus", "Adonis", "Hyacinth", "Ganymede"],
        "answer": "Narcissus"
    },
    {
        "question": "What flower did Narcissus turn into?",
        "options": ["Narcissus (daffodil)", "Rose", "Lily", "Hyacinth"],
        "answer": "Narcissus (daffodil)"
    },
    {
        "question": "Who loved Narcissus but was rejected?",
        "options": ["Echo", "Psyche", "Ariadne", "Daphne"],
        "answer": "Echo"
    },
    {
        "question": "What was Echo's curse?",
        "options": ["She could only repeat others' words", "She was invisible", "She was mute", "She was deaf"],
        "answer": "She could only repeat others' words"
    },
    {
        "question": "Who was turned into a laurel tree to escape Apollo?",
        "options": ["Daphne", "Echo", "Ariadne", "Psyche"],
        "answer": "Daphne"
    },
    {
        "question": "Who was the mortal lover of Aphrodite?",
        "options": ["Adonis", "Narcissus", "Hyacinth", "Ganymede"],
        "answer": "Adonis"
    },
    {
        "question": "What killed Adonis?",
        "options": ["A wild boar", "A serpent", "A lion", "Disease"],
        "answer": "A wild boar"
    },
    {
        "question": "Who was Eros's mortal love?",
        "options": ["Psyche", "Ariadne", "Helen", "Andromeda"],
        "answer": "Psyche"
    },
    {
        "question": "What did Psyche have to do to be with Eros?",
        "options": ["Complete impossible tasks", "Die first", "Climb Mount Olympus", "Defeat a monster"],
        "answer": "Complete impossible tasks"
    },
    {
        "question": "Who abducted Persephone to the Underworld?",
        "options": ["Hades", "Zeus", "Poseidon", "Ares"],
        "answer": "Hades"
    },
    {
        "question": "What did Persephone eat in the Underworld that bound her there?",
        "options": ["Pomegranate seeds", "Ambrosia", "Nectar", "Apples"],
        "answer": "Pomegranate seeds"
    },
    {
        "question": "How many pomegranate seeds did Persephone eat?",
        "options": ["Six", "Three", "Twelve", "One"],
        "answer": "Six"
    },
    {
        "question": "How many months does Persephone spend in the Underworld?",
        "options": ["Six", "Three", "Four", "Nine"],
        "answer": "Six"
    },
    {
        "question": "What do Persephone's months in the Underworld represent?",
        "options": ["Winter", "Summer", "Spring", "Autumn"],
        "answer": "Winter"
    },
    {
        "question": "Who was turned into a spider for challenging Athena?",
        "options": ["Arachne", "Medusa", "Ariadne", "Andromeda"],
        "answer": "Arachne"
    },
    {
        "question": "What was Arachne's skill?",
        "options": ["Weaving", "Hunting", "Singing", "Running"],
        "answer": "Weaving"
    },
    {
        "question": "Who was transformed into stone for looking at Medusa?",
        "options": ["Many warriors", "Perseus", "Athena", "No one"],
        "answer": "Many warriors"
    },
    {
        "question": "Who turned Medusa into a monster?",
        "options": ["Athena", "Hera", "Aphrodite", "Zeus"],
        "answer": "Athena"
    },
    {
        "question": "What did King Midas wish for?",
        "options": ["Everything he touched to turn to gold", "Immortality", "Wisdom", "Power"],
        "answer": "Everything he touched to turn to gold"
    },
    {
        "question": "Who granted King Midas his wish?",
        "options": ["Dionysus", "Zeus", "Apollo", "Hermes"],
        "answer": "Dionysus"
    },
    {
        "question": "What was the problem with Midas's golden touch?",
        "options": ["He couldn't eat or drink", "He became lonely", "He went blind", "He lost his family"],
        "answer": "He couldn't eat or drink"
    },
    # Les Muses
    {
        "question": "How many Muses were there?",
        "options": ["Nine", "Three", "Seven", "Twelve"],
        "answer": "Nine"
    },
    {
        "question": "Who was the father of the Muses?",
        "options": ["Zeus", "Apollo", "Dionysus", "Hermes"],
        "answer": "Zeus"
    },
    {
        "question": "Who was the mother of the Muses?",
        "options": ["Mnemosyne", "Hera", "Leto", "Demeter"],
        "answer": "Mnemosyne"
    },
    {
        "question": "Which Muse was associated with epic poetry?",
        "options": ["Calliope", "Clio", "Erato", "Thalia"],
        "answer": "Calliope"
    },
    {
        "question": "Which Muse was associated with history?",
        "options": ["Clio", "Calliope", "Urania", "Melpomene"],
        "answer": "Clio"
    },
    {
        "question": "Which Muse was associated with tragedy?",
        "options": ["Melpomene", "Thalia", "Terpsichore", "Euterpe"],
        "answer": "Melpomene"
    },
    {
        "question": "Which Muse was associated with comedy?",
        "options": ["Thalia", "Melpomene", "Erato", "Polyhymnia"],
        "answer": "Thalia"
    },
    {
        "question": "Which Muse was associated with dance?",
        "options": ["Terpsichore", "Thalia", "Euterpe", "Erato"],
        "answer": "Terpsichore"
    },
    {
        "question": "Which Muse was associated with love poetry?",
        "options": ["Erato", "Calliope", "Euterpe", "Polyhymnia"],
        "answer": "Erato"
    },
    # Punitions divines
    {
        "question": "What was Sisyphus condemned to do in Tartarus?",
        "options": ["Roll a boulder up a hill eternally", "Be chained to a rock", "Starve while surrounded by food", "Burn forever"],
        "answer": "Roll a boulder up a hill eternally"
    },
    {
        "question": "What was Tantalus's punishment?",
        "options": ["Eternal hunger and thirst despite being surrounded by food and water", "Rolling a boulder", "Being chained", "Being tortured by Furies"],
        "answer": "Eternal hunger and thirst despite being surrounded by food and water"
    },
    {
        "question": "Why was Tantalus punished?",
        "options": ["He served his son as food to the gods", "He stole from the gods", "He betrayed Zeus", "He killed his wife"],
        "answer": "He served his son as food to the gods"
    },
    {
        "question": "What was Prometheus's punishment for stealing fire?",
        "options": ["Chained to a rock with an eagle eating his liver daily", "Thrown into Tartarus", "Turned mortal", "Exiled from Olympus"],
        "answer": "Chained to a rock with an eagle eating his liver daily"
    },
    {
        "question": "Who eventually freed Prometheus?",
        "options": ["Heracles", "Zeus", "Chiron", "Perseus"],
        "answer": "Heracles"
    },
    {
        "question": "What were the Furies goddesses of?",
        "options": ["Vengeance", "Love", "Wisdom", "War"],
        "answer": "Vengeance"
    },
    {
        "question": "How many Furies were there?",
        "options": ["Three", "Nine", "Seven", "Twelve"],
        "answer": "Three"
    },
    {
        "question": "What was another name for the Furies?",
        "options": ["Erinyes", "Gorgons", "Harpies", "Sirens"],
        "answer": "Erinyes"
    },
    # Prophéties et malédictions
    {
        "question": "Who killed his father and married his mother as prophesied?",
        "options": ["Oedipus", "Orestes", "Theseus", "Perseus"],
        "answer": "Oedipus"
    },
    {
        "question": "What city did Oedipus rule?",
        "options": ["Thebes", "Athens", "Sparta", "Corinth"],
        "answer": "Thebes"
    },
    {
        "question": "Who was Oedipus's mother and wife?",
        "options": ["Jocasta", "Antigone", "Ismene", "Eurydice"],
        "answer": "Jocasta"
    },
    {
        "question": "What did Oedipus do when he learned the truth?",
        "options": ["Blinded himself", "Killed himself", "Fled the city", "Went mad"],
        "answer": "Blinded himself"
    },
    {
        "question": "Who was cursed to always speak the truth but never be believed?",
        "options": ["Cassandra", "Pythia", "Medea", "Circe"],
        "answer": "Cassandra"
    },
    {
        "question": "Who cursed Cassandra?",
        "options": ["Apollo", "Zeus", "Hera", "Athena"],
        "answer": "Apollo"
    },
    {
        "question": "Why did Apollo curse Cassandra?",
        "options": ["She refused his advances", "She lied to him", "She betrayed Troy", "She stole from him"],
        "answer": "She refused his advances"
    },
    # Objets et quêtes
    {
        "question": "What was the Golden Fleece?",
        "options": ["The fleece of a golden ram", "A golden cloth", "A magical cloak", "A golden shield"],
        "answer": "The fleece of a golden ram"
    },
    {
        "question": "Where was the Golden Fleece kept?",
        "options": ["Colchis", "Troy", "Crete", "Athens"],
        "answer": "Colchis"
    },
    {
        "question": "What guarded the Golden Fleece?",
        "options": ["A dragon that never slept", "The Hydra", "Cerberus", "The Sphinx"],
        "answer": "A dragon that never slept"
    },
    {
        "question": "What happened to the dragon guarding the Golden Fleece?",
        "options": ["Medea put it to sleep", "Jason killed it", "It was poisoned", "It flew away"],
        "answer": "Medea put it to sleep"
    },
    {
        "question": "What was the Aegis?",
        "options": ["Zeus's shield", "Athena's weapon", "Poseidon's trident", "Hades's helmet"],
        "answer": "Zeus's shield"
    },
    {
        "question": "Who often carried the Aegis?",
        "options": ["Athena", "Zeus", "Apollo", "Ares"],
        "answer": "Athena"
    },
    {
        "question": "What was on the Aegis?",
        "options": ["Medusa's head", "A lightning bolt", "A trident", "An owl"],
        "answer": "Medusa's head"
    },
    # Relations familiales complexes
    {
        "question": "Who was both the sister and wife of Zeus?",
        "options": ["Hera", "Demeter", "Hestia", "Rhea"],
        "answer": "Hera"
    },
    {
        "question": "Who was the mother of both Zeus and Hera?",
        "options": ["Rhea", "Gaia", "Tethys", "Themis"],
        "answer": "Rhea"
    },
    {
        "question": "Which god was born from Zeus's head?",
        "options": ["Athena", "Apollo", "Hermes", "Dionysus"],
        "answer": "Athena"
    },
    {
        "question": "Which god was born from Zeus's thigh?",
        "options": ["Dionysus", "Hermes", "Apollo", "Ares"],
        "answer": "Dionysus"
    },
    {
        "question": "Who was Hephaestus's mother?",
        "options": ["Hera", "Aphrodite", "Demeter", "Leto"],
        "answer": "Hera"
    },
    {
        "question": "According to some myths, who was Hephaestus's father?",
        "options": ["Hera alone (no father)", "Zeus", "Ares", "Poseidon"],
        "answer": "Hera alone (no father)"
    },
    {
        "question": "Who was married to Hephaestus?",
        "options": ["Aphrodite", "Hera", "Athena", "Artemis"],
        "answer": "Aphrodite"
    },
    {
        "question": "Who did Aphrodite have an affair with?",
        "options": ["Ares", "Apollo", "Hermes", "Poseidon"],
        "answer": "Ares"
    },
    {
        "question": "Who were the parents of Apollo and Artemis?",
        "options": ["Zeus and Leto", "Zeus and Hera", "Zeus and Demeter", "Poseidon and Amphitrite"],
        "answer": "Zeus and Leto"
    },
    {
        "question": "Who was the mother of Hermes?",
        "options": ["Maia", "Hera", "Leto", "Demeter"],
        "answer": "Maia"
    },
    {
        "question": "What was Maia?",
        "options": ["A Pleiad (daughter of Atlas)", "A Titaness", "A nymph", "A mortal"],
        "answer": "A Pleiad (daughter of Atlas)"
    },
    # Détails sur Héraclès
    {
        "question": "What was Heracles's Roman name?",
        "options": ["Hercules", "Mercury", "Mars", "Jupiter"],
        "answer": "Hercules"
    },
    {
        "question": "Who was Heracles's divine parent?",
        "options": ["Zeus", "Poseidon", "Apollo", "Ares"],
        "answer": "Zeus"
    },
    {
        "question": "Who was Heracles's mortal mother?",
        "options": ["Alcmene", "Andromeda", "Danae", "Io"],
        "answer": "Alcmene"
    },
    {
        "question": "Which goddess hated Heracles and made his life difficult?",
        "options": ["Hera", "Athena", "Aphrodite", "Artemis"],
        "answer": "Hera"
    },
    {
        "question": "Why did Hera hate Heracles?",
        "options": ["He was Zeus's illegitimate son", "He rejected her", "He killed her favorite", "He was too proud"],
        "answer": "He was Zeus's illegitimate son"
    },
    {
        "question": "What made Heracles kill his own family?",
        "options": ["Madness sent by Hera", "A curse", "Poison", "A prophecy"],
        "answer": "Madness sent by Hera"
    },
    {
        "question": "How many labors was Heracles originally supposed to complete?",
        "options": ["Ten", "Twelve", "Seven", "Nine"],
        "answer": "Ten"
    },
    {
        "question": "Why did Heracles have to complete 12 labors instead of 10?",
        "options": ["Two didn't count because he had help", "He failed two", "It was punishment", "He volunteered for more"],
        "answer": "Two didn't count because he had help"
    },
    {
        "question": "What was Heracles's first labor?",
        "options": ["Slay the Nemean Lion", "Capture the Erymanthian Boar", "Kill the Hydra", "Clean the Augean stables"],
        "answer": "Slay the Nemean Lion"
    },
    {
        "question": "What was special about the Nemean Lion's hide?",
        "options": ["It was impenetrable", "It was golden", "It was invisible", "It was magical"],
        "answer": "It was impenetrable"
    },
    {
        "question": "How did Heracles kill the Nemean Lion?",
        "options": ["Strangled it", "Shot it with arrows", "Stabbed it", "Poisoned it"],
        "answer": "Strangled it"
    },
    {
        "question": "What did Heracles use the Nemean Lion's hide for?",
        "options": ["As armor/cloak", "As a trophy", "As a gift", "He burned it"],
        "answer": "As armor/cloak"
    },
    {
        "question": "Who helped Heracles burn the Hydra's neck stumps?",
        "options": ["Iolaus", "Theseus", "Jason", "Orpheus"],
        "answer": "Iolaus"
    },
    {
        "question": "What labor involved cleaning extremely filthy stables in one day?",
        "options": ["The Augean stables", "The Nemean Lion", "The Cretan Bull", "The Erymanthian Boar"],
        "answer": "The Augean stables"
    },
    {
        "question": "How did Heracles clean the Augean stables?",
        "options": ["Diverted two rivers through them", "Used a giant broom", "Burned them", "With divine help"],
        "answer": "Diverted two rivers through them"
    },
    {
        "question": "What did Heracles have to capture alive for one of his labors?",
        "options": ["The Erymanthian Boar", "The Nemean Lion", "The Cretan Bull", "Cerberus"],
        "answer": "The Erymanthian Boar"
    },
    {
        "question": "Which labor involved man-eating birds?",
        "options": ["The Stymphalian Birds", "The Cretan Bull", "The Mares of Diomedes", "The Cattle of Geryon"],
        "answer": "The Stymphalian Birds"
    },
    {
        "question": "What special girdle did Heracles have to obtain?",
        "options": ["The girdle of Hippolyta, Queen of the Amazons", "The girdle of Aphrodite", "The girdle of Hera", "The girdle of Athena"],
        "answer": "The girdle of Hippolyta, Queen of the Amazons"
    },
    {
        "question": "What three-bodied monster's cattle did Heracles steal?",
        "options": ["Geryon", "Cerberus", "Chimera", "Orthrus"],
        "answer": "Geryon"
    },
    {
        "question": "What magical apples did Heracles have to steal?",
        "options": ["The Golden Apples of the Hesperides", "The Apples of Discord", "The Apples of Immortality", "The Apples of Knowledge"],
        "answer": "The Golden Apples of the Hesperides"
    },
    {
        "question": "Who held up the sky while Heracles fetched the golden apples?",
        "options": ["Atlas", "Prometheus", "Heracles himself", "Zeus"],
        "answer": "Atlas"
    },
    {
        "question": "What was Heracles's final labor?",
        "options": ["Capture Cerberus", "Kill the Nemean Lion", "Steal the golden apples", "Clean the stables"],
        "answer": "Capture Cerberus"
    },
    {
        "question": "What condition did Hades give for Heracles to take Cerberus?",
        "options": ["He must do it without weapons", "He must return him", "He must fight him", "He must tame him"],
        "answer": "He must do it without weapons"
    },
    # Orphée
    {
        "question": "What was Orpheus famous for?",
        "options": ["His musical ability", "His strength", "His wisdom", "His beauty"],
        "answer": "His musical ability"
    },
    {
        "question": "What instrument did Orpheus play?",
        "options": ["Lyre", "Flute", "Harp", "Pan pipes"],
        "answer": "Lyre"
    },
    {
        "question": "Who was Orpheus's wife?",
        "options": ["Eurydice", "Ariadne", "Psyche", "Andromeda"],
        "answer": "Eurydice"
    },
    {
        "question": "How did Eurydice die?",
        "options": ["Snake bite", "Illness", "Drowning", "Fall"],
        "answer": "Snake bite"
    },
    {
        "question": "Where did Orpheus go to retrieve Eurydice?",
        "options": ["The Underworld", "Mount Olympus", "The ocean", "A far island"],
        "answer": "The Underworld"
    },
    {
        "question": "What condition did Hades give Orpheus to take Eurydice back?",
        "options": ["Don't look back until they reached the surface", "Play music constantly", "Never speak of it", "Return in a year"],
        "answer": "Don't look back until they reached the surface"
    },
    {
        "question": "What did Orpheus do that made him lose Eurydice forever?",
        "options": ["Looked back too soon", "Stopped playing", "Spoke to her", "Tried to touch her"],
        "answer": "Looked back too soon"
    },
    {
        "question": "How did Orpheus die?",
        "options": ["Torn apart by Maenads", "Killed by a monster", "Died of grief", "Drowned"],
        "answer": "Torn apart by Maenads"
    },
    # Divers
    {
        "question": "What food was reserved for the gods?",
        "options": ["Ambrosia", "Nectar", "Pomegranate", "Golden apples"],
        "answer": "Ambrosia"
    },
    {
        "question": "What drink was reserved for the gods?",
        "options": ["Nectar", "Ambrosia", "Wine", "Water from the Styx"],
        "answer": "Nectar"
    },
    {
        "question": "What made the gods immortal?",
        "options": ["Ambrosia and nectar", "Their divine nature", "A spell", "The waters of Styx"],
        "answer": "Ambrosia and nectar"
    },
    {
        "question": "Who was the cupbearer of the gods?",
        "options": ["Ganymede", "Hebe", "Hermes", "Iris"],
        "answer": "Ganymede"
    },
    {
        "question": "What was Ganymede before becoming cupbearer?",
        "options": ["A beautiful mortal prince", "A god", "A hero", "A king"],
        "answer": "A beautiful mortal prince"
    },
    {
        "question": "Who abducted Ganymede to Olympus?",
        "options": ["Zeus", "Hermes", "Apollo", "Poseidon"],
        "answer": "Zeus"
    },
    {
        "question": "In what form did Zeus abduct Ganymede?",
        "options": ["An eagle", "A swan", "A bull", "A shower of gold"],
        "answer": "An eagle"
    },
    {
        "question": "In what form did Zeus seduce Europa?",
        "options": ["A white bull", "A swan", "An eagle", "A shower of gold"],
        "answer": "A white bull"
    },
    {
        "question": "In what form did Zeus visit Leda?",
        "options": ["A swan", "A bull", "An eagle", "A shower of gold"],
        "answer": "A swan"
    },
    {
        "question": "In what form did Zeus visit Danae?",
        "options": ["A shower of gold", "A bull", "A swan", "An eagle"],
        "answer": "A shower of gold"
    },
    {
        "question": "Who was born from Leda's egg(s) after Zeus's visit?",
        "options": ["Helen and Polydeuces (and possibly Clytemnestra and Castor)", "Heracles", "Perseus", "Theseus"],
        "answer": "Helen and Polydeuces (and possibly Clytemnestra and Castor)"
    },
    {
        "question": "Who was the son of Danae and Zeus?",
        "options": ["Perseus", "Heracles", "Theseus", "Jason"],
        "answer": "Perseus"
    },
    {
        "question": "Who were Castor and Polydeuces (Pollux)?",
        "options": ["Twin brothers, the Dioscuri", "The Argonauts' leaders", "Sons of Apollo", "Trojan princes"],
        "answer": "Twin brothers, the Dioscuri"
    },
    {
        "question": "What constellation represents Castor and Polydeuces?",
        "options": ["Gemini", "Orion", "Perseus", "Hercules"],
        "answer": "Gemini"
    },
]

print(f"\nNombre de nouvelles questions préparées: {len(new_questions)}")

# Filtrer les questions qui existent déjà
filtered_questions = []
for q in new_questions:
    question_lower = q["question"].lower().strip()
    if question_lower not in existing_questions:
        filtered_questions.append(q)
        existing_questions.add(question_lower)
    else:
        print(f"Question en double ignorée: {q['question']}")

print(f"Nombre de nouvelles questions uniques: {len(filtered_questions)}")

# Ajouter les nouvelles questions avec ID et UUID
next_id = current_max_id + 1
for q in filtered_questions:
    q["id"] = next_id
    q["uuid"] = str(uuid.uuid4())
    q["difficulty_level"] = 1
    next_id += 1
    greek_quiz["questions"].append(q)

print(f"Nouvelles questions ajoutées au quiz Greek Mythology")
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

