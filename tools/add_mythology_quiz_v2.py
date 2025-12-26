import json
import uuid

print("Début du traitement...")

# Charger le fichier JSON existant
print("Chargement du fichier JSON...")
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Fichier chargé. Nombre de quiz: {len(data['quizzes'])}")

# Créer le quiz de mythologie
print("Création du quiz de mythologie...")
mythology_quiz = {
    "name": "Mythology Quiz",
    "imageFileName": "mythology.svg",
    "questions": []
}

# Questions mythologie grecque
greek_questions = [
    {"question": "Who is the king of the Greek gods?", "options": ["Apollo", "Zeus", "Poseidon", "Hades"], "answer": "Zeus"},
    {"question": "What is Athena the goddess of?", "options": ["Love", "War and Wisdom", "The Hunt", "Agriculture"], "answer": "War and Wisdom"},
    {"question": "Who is Poseidon's brother?", "options": ["Apollo", "Ares", "Zeus", "Hermes"], "answer": "Zeus"},
    {"question": "What is Aphrodite the goddess of?", "options": ["Beauty and Love", "War", "Wisdom", "The Moon"], "answer": "Beauty and Love"},
    {"question": "Who is Apollo's twin sister?", "options": ["Athena", "Aphrodite", "Artemis", "Hera"], "answer": "Artemis"},
    {"question": "What is Ares the god of?", "options": ["Love", "War", "The Sea", "Music"], "answer": "War"},
    {"question": "Who is the wife of Zeus?", "options": ["Athena", "Hera", "Demeter", "Hestia"], "answer": "Hera"},
    {"question": "What is Hermes the god of?", "options": ["War", "Messengers and Commerce", "The Sea", "Agriculture"], "answer": "Messengers and Commerce"},
    {"question": "Who is Artemis the goddess of?", "options": ["Love", "The Hunt and Moon", "War", "Wisdom"], "answer": "The Hunt and Moon"},
    {"question": "What is Hephaestus the god of?", "options": ["Fire and Metalworking", "War", "The Sea", "Wine"], "answer": "Fire and Metalworking"},
    {"question": "Who is the father of Zeus?", "options": ["Uranus", "Chronos", "Oceanus", "Atlas"], "answer": "Chronos"},
    {"question": "What is Demeter the goddess of?", "options": ["Love", "War", "Agriculture and Harvest", "The Moon"], "answer": "Agriculture and Harvest"},
    {"question": "Who is Persephone's mother?", "options": ["Hera", "Athena", "Demeter", "Aphrodite"], "answer": "Demeter"},
    {"question": "What is Dionysus the god of?", "options": ["War", "Wine and Festivities", "The Sea", "Music"], "answer": "Wine and Festivities"},
    {"question": "Who is Hades the god of?", "options": ["The Sky", "The Sea", "The Underworld", "War"], "answer": "The Underworld"},
    {"question": "Who is the mother of Athena?", "options": ["Hera", "Metis", "Demeter", "Leto"], "answer": "Metis"},
    {"question": "What is Hestia the goddess of?", "options": ["War", "The Hearth and Home", "Love", "Wisdom"], "answer": "The Hearth and Home"},
    {"question": "Who is the husband of Aphrodite?", "options": ["Zeus", "Ares", "Hephaestus", "Apollo"], "answer": "Hephaestus"},
    {"question": "What is Nike the goddess of?", "options": ["Love", "Victory", "Wisdom", "The Hunt"], "answer": "Victory"},
    {"question": "Who is the mother of Apollo and Artemis?", "options": ["Hera", "Leto", "Demeter", "Metis"], "answer": "Leto"},
    {"question": "Who are the parents of Zeus?", "options": ["Uranus and Gaia", "Chronos and Rhea", "Oceanus and Tethys", "Atlas and Pleione"], "answer": "Chronos and Rhea"},
    {"question": "What is Hecate the goddess of?", "options": ["Love", "Magic and Crossroads", "War", "The Hunt"], "answer": "Magic and Crossroads"},
    {"question": "Who is Persephone's husband?", "options": ["Zeus", "Poseidon", "Hades", "Apollo"], "answer": "Hades"},
    {"question": "What is Pan the god of?", "options": ["War", "Nature and Shepherds", "The Sea", "Wine"], "answer": "Nature and Shepherds"},
    {"question": "Who are the nine Muses daughters of?", "options": ["Zeus", "Apollo", "Zeus and Mnemosyne", "Poseidon"], "answer": "Zeus and Mnemosyne"},
]

# Questions mythologie romaine
roman_questions = [
    {"question": "What is Jupiter's Greek equivalent?", "options": ["Apollo", "Zeus", "Ares", "Hermes"], "answer": "Zeus"},
    {"question": "What is Mars the god of in Roman mythology?", "options": ["Love", "War", "The Sea", "Wine"], "answer": "War"},
    {"question": "Who is Venus in Roman mythology?", "options": ["Goddess of War", "Goddess of Love", "Goddess of Wisdom", "Goddess of the Hunt"], "answer": "Goddess of Love"},
    {"question": "What is Neptune the god of?", "options": ["The Sky", "The Sea", "The Underworld", "Fire"], "answer": "The Sea"},
    {"question": "Who is Minerva in Roman mythology?", "options": ["Goddess of Love", "Goddess of Wisdom", "Goddess of the Hunt", "Goddess of Agriculture"], "answer": "Goddess of Wisdom"},
    {"question": "What is Pluto the god of in Roman mythology?", "options": ["The Sky", "The Sea", "The Underworld", "War"], "answer": "The Underworld"},
    {"question": "Who is Juno in Roman mythology?", "options": ["Wife of Jupiter", "Goddess of Love", "Goddess of the Hunt", "Goddess of Agriculture"], "answer": "Wife of Jupiter"},
    {"question": "What is Mercury the god of?", "options": ["War", "Messengers and Commerce", "The Sea", "Fire"], "answer": "Messengers and Commerce"},
    {"question": "Who is Diana in Roman mythology?", "options": ["Goddess of Love", "Goddess of the Hunt", "Goddess of War", "Goddess of Wisdom"], "answer": "Goddess of the Hunt"},
    {"question": "What is Vulcan the god of?", "options": ["Fire and Metalworking", "War", "The Sea", "Wine"], "answer": "Fire and Metalworking"},
]

# Questions mythologie nordique
norse_questions = [
    {"question": "Who is the king of the Norse gods?", "options": ["Thor", "Odin", "Loki", "Freyr"], "answer": "Odin"},
    {"question": "What is Thor the god of?", "options": ["War", "Thunder and Lightning", "The Sea", "Wisdom"], "answer": "Thunder and Lightning"},
    {"question": "Who is Loki in Norse mythology?", "options": ["God of War", "Trickster God", "God of Thunder", "God of the Sea"], "answer": "Trickster God"},
    {"question": "What is Freyja the goddess of?", "options": ["War", "Love and Fertility", "Wisdom", "The Sea"], "answer": "Love and Fertility"},
    {"question": "Who is Thor's father?", "options": ["Loki", "Odin", "Freyr", "Baldur"], "answer": "Odin"},
    {"question": "What is Heimdall the god of?", "options": ["War", "Guardian of Bifrost", "Thunder", "The Sea"], "answer": "Guardian of Bifrost"},
    {"question": "Who is Frigg in Norse mythology?", "options": ["Goddess of Love", "Wife of Odin", "Goddess of War", "Goddess of the Hunt"], "answer": "Wife of Odin"},
    {"question": "What is Tyr the god of?", "options": ["Thunder", "War and Justice", "The Sea", "Wisdom"], "answer": "War and Justice"},
    {"question": "Who is Baldur in Norse mythology?", "options": ["God of Light and Purity", "God of War", "God of Thunder", "Trickster God"], "answer": "God of Light and Purity"},
    {"question": "Who is Baldur's mother?", "options": ["Freyja", "Frigg", "Sif", "Idun"], "answer": "Frigg"},
]

# Questions mythologie égyptienne
egyptian_questions = [
    {"question": "Who is Ra in Egyptian mythology?", "options": ["God of War", "God of the Sun", "God of the Dead", "God of the Nile"], "answer": "God of the Sun"},
    {"question": "What is Anubis the god of?", "options": ["The Sun", "Mummification and the Dead", "War", "The Nile"], "answer": "Mummification and the Dead"},
    {"question": "Who is Osiris in Egyptian mythology?", "options": ["God of the Sun", "God of the Underworld", "God of War", "God of Wisdom"], "answer": "God of the Underworld"},
    {"question": "What is Isis the goddess of?", "options": ["War", "Magic and Motherhood", "The Sun", "The Hunt"], "answer": "Magic and Motherhood"},
    {"question": "Who is Isis's husband?", "options": ["Ra", "Osiris", "Anubis", "Set"], "answer": "Osiris"},
    {"question": "What is Horus the god of?", "options": ["The Sun", "The Sky and Kingship", "The Dead", "War"], "answer": "The Sky and Kingship"},
    {"question": "Who is Horus's mother?", "options": ["Hathor", "Isis", "Bastet", "Sekhmet"], "answer": "Isis"},
    {"question": "What is Set the god of?", "options": ["The Sun", "Chaos and Storms", "The Dead", "Wisdom"], "answer": "Chaos and Storms"},
    {"question": "Who is Thoth in Egyptian mythology?", "options": ["God of War", "God of Wisdom and Writing", "God of the Sun", "God of the Dead"], "answer": "God of Wisdom and Writing"},
    {"question": "What is Bastet the goddess of?", "options": ["War", "Cats and Protection", "The Sun", "Magic"], "answer": "Cats and Protection"},
]

# Questions mythologie hindoue
hindu_questions = [
    {"question": "Who is Brahma in Hindu mythology?", "options": ["God of Destruction", "Creator God", "Preserver God", "God of War"], "answer": "Creator God"},
    {"question": "What is Vishnu the god of?", "options": ["Destruction", "Preservation", "Creation", "War"], "answer": "Preservation"},
    {"question": "What is Shiva the god of?", "options": ["Creation", "Preservation", "Destruction and Transformation", "War"], "answer": "Destruction and Transformation"},
    {"question": "Who is Lakshmi in Hindu mythology?", "options": ["Goddess of War", "Goddess of Wealth and Prosperity", "Goddess of Knowledge", "Goddess of Power"], "answer": "Goddess of Wealth and Prosperity"},
    {"question": "Who is Lakshmi's consort?", "options": ["Brahma", "Vishnu", "Shiva", "Ganesha"], "answer": "Vishnu"},
    {"question": "What is Saraswati the goddess of?", "options": ["Wealth", "Knowledge and Arts", "War", "Power"], "answer": "Knowledge and Arts"},
    {"question": "Who is Saraswati's consort?", "options": ["Brahma", "Vishnu", "Shiva", "Indra"], "answer": "Brahma"},
    {"question": "What is Parvati the goddess of?", "options": ["Wealth", "Knowledge", "Power and Devotion", "War"], "answer": "Power and Devotion"},
    {"question": "Who is Parvati's consort?", "options": ["Brahma", "Vishnu", "Shiva", "Krishna"], "answer": "Shiva"},
    {"question": "Who is Ganesha in Hindu mythology?", "options": ["God of War", "God of Wisdom and Remover of Obstacles", "God of Love", "God of Fire"], "answer": "God of Wisdom and Remover of Obstacles"},
    {"question": "Who are Ganesha's parents?", "options": ["Brahma and Saraswati", "Vishnu and Lakshmi", "Shiva and Parvati", "Indra and Indrani"], "answer": "Shiva and Parvati"},
    {"question": "What is Hanuman the god of?", "options": ["War", "Strength and Devotion", "Knowledge", "Wealth"], "answer": "Strength and Devotion"},
    {"question": "What is Indra the god of?", "options": ["Fire", "Thunder and Rain", "Wind", "Earth"], "answer": "Thunder and Rain"},
    {"question": "What is Agni the god of?", "options": ["Water", "Fire", "Wind", "Earth"], "answer": "Fire"},
    {"question": "What is Kali in Hindu mythology?", "options": ["Goddess of Wealth", "Goddess of Time and Death", "Goddess of Knowledge", "Goddess of Love"], "answer": "Goddess of Time and Death"},
]

# Combiner toutes les questions
all_questions = greek_questions + roman_questions + norse_questions + egyptian_questions + hindu_questions

# Ajouter les IDs et UUIDs
for i, q in enumerate(all_questions, 1):
    q['id'] = i
    q['uuid'] = str(uuid.uuid4())

mythology_quiz['questions'] = all_questions

print(f"Quiz créé avec {len(mythology_quiz['questions'])} questions")

# Ajouter le quiz de mythologie
data['quizzes'].append(mythology_quiz)

print("Sauvegarde du fichier JSON...")
# Sauvegarder le fichier JSON modifié
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Quiz de mythologie ajouté avec succès!")
print(f"Nombre total de quiz: {len(data['quizzes'])}")

