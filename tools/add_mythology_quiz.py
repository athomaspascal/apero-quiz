import json
import uuid
import sys

# Charger le fichier JSON existant
try:
    with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Fichier chargé avec succès. Clés: {list(data.keys())}")
except Exception as e:
    print(f"Erreur lors du chargement: {e}")
    sys.exit(1)

# Créer le quiz de mythologie
mythology_quiz = {
    "name": "Mythology Quiz",
    "imageFileName": "mythology.svg",
    "questions": [
        # Mythologie grecque
        {
            "id": 1,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the king of the Greek gods?",
            "options": ["Apollo", "Zeus", "Poseidon", "Hades"],
            "answer": "Zeus"
        },
        {
            "id": 2,
            "uuid": str(uuid.uuid4()),
            "question": "What is Athena the goddess of?",
            "options": ["Love", "War and Wisdom", "The Hunt", "Agriculture"],
            "answer": "War and Wisdom"
        },
        {
            "id": 3,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Poseidon's brother?",
            "options": ["Apollo", "Ares", "Zeus", "Hermes"],
            "answer": "Zeus"
        },
        {
            "id": 4,
            "uuid": str(uuid.uuid4()),
            "question": "What is Aphrodite the goddess of?",
            "options": ["Beauty and Love", "War", "Wisdom", "The Moon"],
            "answer": "Beauty and Love"
        },
        {
            "id": 5,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Apollo's twin sister?",
            "options": ["Athena", "Aphrodite", "Artemis", "Hera"],
            "answer": "Artemis"
        },
        {
            "id": 6,
            "uuid": str(uuid.uuid4()),
            "question": "What is Ares the god of?",
            "options": ["Love", "War", "The Sea", "Music"],
            "answer": "War"
        },
        {
            "id": 7,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the wife of Zeus?",
            "options": ["Athena", "Hera", "Demeter", "Hestia"],
            "answer": "Hera"
        },
        {
            "id": 8,
            "uuid": str(uuid.uuid4()),
            "question": "What is Hermes the god of?",
            "options": ["War", "Messengers and Commerce", "The Sea", "Agriculture"],
            "answer": "Messengers and Commerce"
        },
        {
            "id": 9,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Artemis the goddess of?",
            "options": ["Love", "The Hunt and Moon", "War", "Wisdom"],
            "answer": "The Hunt and Moon"
        },
        {
            "id": 10,
            "uuid": str(uuid.uuid4()),
            "question": "What is Hephaestus the god of?",
            "options": ["Fire and Metalworking", "War", "The Sea", "Wine"],
            "answer": "Fire and Metalworking"
        },
        {
            "id": 11,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the father of Zeus?",
            "options": ["Uranus", "Chronos", "Oceanus", "Atlas"],
            "answer": "Chronos"
        },
        {
            "id": 12,
            "uuid": str(uuid.uuid4()),
            "question": "What is Demeter the goddess of?",
            "options": ["Love", "War", "Agriculture and Harvest", "The Moon"],
            "answer": "Agriculture and Harvest"
        },
        {
            "id": 13,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Persephone's mother?",
            "options": ["Hera", "Athena", "Demeter", "Aphrodite"],
            "answer": "Demeter"
        },
        {
            "id": 14,
            "uuid": str(uuid.uuid4()),
            "question": "What is Dionysus the god of?",
            "options": ["War", "Wine and Festivities", "The Sea", "Music"],
            "answer": "Wine and Festivities"
        },
        {
            "id": 15,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Hades the god of?",
            "options": ["The Sky", "The Sea", "The Underworld", "War"],
            "answer": "The Underworld"
        },
        {
            "id": 16,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the mother of Athena?",
            "options": ["Hera", "Metis", "Demeter", "Leto"],
            "answer": "Metis"
        },
        {
            "id": 17,
            "uuid": str(uuid.uuid4()),
            "question": "What is Hestia the goddess of?",
            "options": ["War", "The Hearth and Home", "Love", "Wisdom"],
            "answer": "The Hearth and Home"
        },
        {
            "id": 18,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the husband of Aphrodite?",
            "options": ["Zeus", "Ares", "Hephaestus", "Apollo"],
            "answer": "Hephaestus"
        },
        {
            "id": 19,
            "uuid": str(uuid.uuid4()),
            "question": "What is Nike the goddess of?",
            "options": ["Love", "Victory", "Wisdom", "The Hunt"],
            "answer": "Victory"
        },
        {
            "id": 20,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the mother of Apollo and Artemis?",
            "options": ["Hera", "Leto", "Demeter", "Metis"],
            "answer": "Leto"
        },
        # Mythologie romaine
        {
            "id": 21,
            "uuid": str(uuid.uuid4()),
            "question": "What is Jupiter's Greek equivalent?",
            "options": ["Apollo", "Zeus", "Ares", "Hermes"],
            "answer": "Zeus"
        },
        {
            "id": 22,
            "uuid": str(uuid.uuid4()),
            "question": "What is Mars the god of in Roman mythology?",
            "options": ["Love", "War", "The Sea", "Wine"],
            "answer": "War"
        },
        {
            "id": 23,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Venus in Roman mythology?",
            "options": ["Goddess of War", "Goddess of Love", "Goddess of Wisdom", "Goddess of the Hunt"],
            "answer": "Goddess of Love"
        },
        {
            "id": 24,
            "uuid": str(uuid.uuid4()),
            "question": "What is Neptune the god of?",
            "options": ["The Sky", "The Sea", "The Underworld", "Fire"],
            "answer": "The Sea"
        },
        {
            "id": 25,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Minerva in Roman mythology?",
            "options": ["Goddess of Love", "Goddess of Wisdom", "Goddess of the Hunt", "Goddess of Agriculture"],
            "answer": "Goddess of Wisdom"
        },
        {
            "id": 26,
            "uuid": str(uuid.uuid4()),
            "question": "What is Pluto the god of in Roman mythology?",
            "options": ["The Sky", "The Sea", "The Underworld", "War"],
            "answer": "The Underworld"
        },
        {
            "id": 27,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Juno in Roman mythology?",
            "options": ["Wife of Jupiter", "Goddess of Love", "Goddess of the Hunt", "Goddess of Agriculture"],
            "answer": "Wife of Jupiter"
        },
        {
            "id": 28,
            "uuid": str(uuid.uuid4()),
            "question": "What is Mercury the god of?",
            "options": ["War", "Messengers and Commerce", "The Sea", "Fire"],
            "answer": "Messengers and Commerce"
        },
        {
            "id": 29,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Diana in Roman mythology?",
            "options": ["Goddess of Love", "Goddess of the Hunt", "Goddess of War", "Goddess of Wisdom"],
            "answer": "Goddess of the Hunt"
        },
        {
            "id": 30,
            "uuid": str(uuid.uuid4()),
            "question": "What is Vulcan the god of?",
            "options": ["Fire and Metalworking", "War", "The Sea", "Wine"],
            "answer": "Fire and Metalworking"
        },
        # Mythologie nordique
        {
            "id": 31,
            "uuid": str(uuid.uuid4()),
            "question": "Who is the king of the Norse gods?",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "answer": "Odin"
        },
        {
            "id": 32,
            "uuid": str(uuid.uuid4()),
            "question": "What is Thor the god of?",
            "options": ["War", "Thunder and Lightning", "The Sea", "Wisdom"],
            "answer": "Thunder and Lightning"
        },
        {
            "id": 33,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Loki in Norse mythology?",
            "options": ["God of War", "Trickster God", "God of Thunder", "God of the Sea"],
            "answer": "Trickster God"
        },
        {
            "id": 34,
            "uuid": str(uuid.uuid4()),
            "question": "What is Freyja the goddess of?",
            "options": ["War", "Love and Fertility", "Wisdom", "The Sea"],
            "answer": "Love and Fertility"
        },
        {
            "id": 35,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Thor's father?",
            "options": ["Loki", "Odin", "Freyr", "Baldur"],
            "answer": "Odin"
        },
        {
            "id": 36,
            "uuid": str(uuid.uuid4()),
            "question": "What is Heimdall the god of?",
            "options": ["War", "Guardian of Bifrost", "Thunder", "The Sea"],
            "answer": "Guardian of Bifrost"
        },
        {
            "id": 37,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Frigg in Norse mythology?",
            "options": ["Goddess of Love", "Wife of Odin", "Goddess of War", "Goddess of the Hunt"],
            "answer": "Wife of Odin"
        },
        {
            "id": 38,
            "uuid": str(uuid.uuid4()),
            "question": "What is Tyr the god of?",
            "options": ["Thunder", "War and Justice", "The Sea", "Wisdom"],
            "answer": "War and Justice"
        },
        {
            "id": 39,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Baldur in Norse mythology?",
            "options": ["God of Light and Purity", "God of War", "God of Thunder", "Trickster God"],
            "answer": "God of Light and Purity"
        },
        {
            "id": 40,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Baldur's mother?",
            "options": ["Freyja", "Frigg", "Sif", "Idun"],
            "answer": "Frigg"
        },
        # Mythologie égyptienne
        {
            "id": 41,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Ra in Egyptian mythology?",
            "options": ["God of War", "God of the Sun", "God of the Dead", "God of the Nile"],
            "answer": "God of the Sun"
        },
        {
            "id": 42,
            "uuid": str(uuid.uuid4()),
            "question": "What is Anubis the god of?",
            "options": ["The Sun", "Mummification and the Dead", "War", "The Nile"],
            "answer": "Mummification and the Dead"
        },
        {
            "id": 43,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Osiris in Egyptian mythology?",
            "options": ["God of the Sun", "God of the Underworld", "God of War", "God of Wisdom"],
            "answer": "God of the Underworld"
        },
        {
            "id": 44,
            "uuid": str(uuid.uuid4()),
            "question": "What is Isis the goddess of?",
            "options": ["War", "Magic and Motherhood", "The Sun", "The Hunt"],
            "answer": "Magic and Motherhood"
        },
        {
            "id": 45,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Isis's husband?",
            "options": ["Ra", "Osiris", "Anubis", "Set"],
            "answer": "Osiris"
        },
        {
            "id": 46,
            "uuid": str(uuid.uuid4()),
            "question": "What is Horus the god of?",
            "options": ["The Sun", "The Sky and Kingship", "The Dead", "War"],
            "answer": "The Sky and Kingship"
        },
        {
            "id": 47,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Horus's mother?",
            "options": ["Hathor", "Isis", "Bastet", "Sekhmet"],
            "answer": "Isis"
        },
        {
            "id": 48,
            "uuid": str(uuid.uuid4()),
            "question": "What is Set the god of?",
            "options": ["The Sun", "Chaos and Storms", "The Dead", "Wisdom"],
            "answer": "Chaos and Storms"
        },
        {
            "id": 49,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Thoth in Egyptian mythology?",
            "options": ["God of War", "God of Wisdom and Writing", "God of the Sun", "God of the Dead"],
            "answer": "God of Wisdom and Writing"
        },
        {
            "id": 50,
            "uuid": str(uuid.uuid4()),
            "question": "What is Bastet the goddess of?",
            "options": ["War", "Cats and Protection", "The Sun", "Magic"],
            "answer": "Cats and Protection"
        },
        # Plus de questions mythologie grecque
        {
            "id": 51,
            "uuid": str(uuid.uuid4()),
            "question": "Who are the parents of Zeus?",
            "options": ["Uranus and Gaia", "Chronos and Rhea", "Oceanus and Tethys", "Atlas and Pleione"],
            "answer": "Chronos and Rhea"
        },
        {
            "id": 52,
            "uuid": str(uuid.uuid4()),
            "question": "What is Hecate the goddess of?",
            "options": ["Love", "Magic and Crossroads", "War", "The Hunt"],
            "answer": "Magic and Crossroads"
        },
        {
            "id": 53,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Persephone's husband?",
            "options": ["Zeus", "Poseidon", "Hades", "Apollo"],
            "answer": "Hades"
        },
        {
            "id": 54,
            "uuid": str(uuid.uuid4()),
            "question": "What is Pan the god of?",
            "options": ["War", "Nature and Shepherds", "The Sea", "Wine"],
            "answer": "Nature and Shepherds"
        },
        {
            "id": 55,
            "uuid": str(uuid.uuid4()),
            "question": "Who are the nine Muses daughters of?",
            "options": ["Zeus", "Apollo", "Zeus and Mnemosyne", "Poseidon"],
            "answer": "Zeus and Mnemosyne"
        },
        {
            "id": 56,
            "uuid": str(uuid.uuid4()),
            "question": "What is Hypnos the god of?",
            "options": ["War", "Sleep", "Death", "Dreams"],
            "answer": "Sleep"
        },
        {
            "id": 57,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Hypnos's twin brother?",
            "options": ["Ares", "Thanatos", "Hermes", "Apollo"],
            "answer": "Thanatos"
        },
        {
            "id": 58,
            "uuid": str(uuid.uuid4()),
            "question": "What is Thanatos the god of?",
            "options": ["Sleep", "Death", "War", "The Underworld"],
            "answer": "Death"
        },
        {
            "id": 59,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Eros in Greek mythology?",
            "options": ["God of War", "God of Love and Desire", "God of Sleep", "God of Wine"],
            "answer": "God of Love and Desire"
        },
        {
            "id": 60,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Eros's mother?",
            "options": ["Hera", "Athena", "Aphrodite", "Demeter"],
            "answer": "Aphrodite"
        },
        {
            "id": 61,
            "uuid": str(uuid.uuid4()),
            "question": "What are the three Fates called in Greek mythology?",
            "options": ["Furies", "Moirai", "Graces", "Muses"],
            "answer": "Moirai"
        },
        {
            "id": 62,
            "uuid": str(uuid.uuid4()),
            "question": "What is Nemesis the goddess of?",
            "options": ["Love", "Retribution and Vengeance", "War", "Wisdom"],
            "answer": "Retribution and Vengeance"
        },
        {
            "id": 63,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Gaia in Greek mythology?",
            "options": ["Goddess of Love", "Primordial Earth Goddess", "Goddess of War", "Goddess of Wisdom"],
            "answer": "Primordial Earth Goddess"
        },
        {
            "id": 64,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Uranus in Greek mythology?",
            "options": ["God of War", "Primordial Sky God", "God of the Sea", "God of the Underworld"],
            "answer": "Primordial Sky God"
        },
        {
            "id": 65,
            "uuid": str(uuid.uuid4()),
            "question": "Who are Gaia and Uranus's children?",
            "options": ["The Olympians", "The Titans", "The Muses", "The Furies"],
            "answer": "The Titans"
        },
        {
            "id": 66,
            "uuid": str(uuid.uuid4()),
            "question": "What is Nyx the goddess of?",
            "options": ["Day", "Night", "Dawn", "Dusk"],
            "answer": "Night"
        },
        {
            "id": 67,
            "uuid": str(uuid.uuid4()),
            "question": "What is Erebus the god of?",
            "options": ["Light", "Darkness", "The Sky", "The Sea"],
            "answer": "Darkness"
        },
        {
            "id": 68,
            "uuid": str(uuid.uuid4()),
            "question": "What is Eos the goddess of?",
            "options": ["Night", "Dawn", "Dusk", "Day"],
            "answer": "Dawn"
        },
        {
            "id": 69,
            "uuid": str(uuid.uuid4()),
            "question": "What is Helios the god of?",
            "options": ["The Moon", "The Sun", "The Stars", "Fire"],
            "answer": "The Sun"
        },
        {
            "id": 70,
            "uuid": str(uuid.uuid4()),
            "question": "What is Selene the goddess of?",
            "options": ["The Sun", "The Moon", "The Stars", "Dawn"],
            "answer": "The Moon"
        },
        {
            "id": 71,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Prometheus in Greek mythology?",
            "options": ["Titan who stole fire for humans", "God of War", "God of the Sea", "King of the gods"],
            "answer": "Titan who stole fire for humans"
        },
        {
            "id": 72,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Atlas in Greek mythology?",
            "options": ["God of War", "Titan who holds up the sky", "God of the Sea", "God of Fire"],
            "answer": "Titan who holds up the sky"
        },
        {
            "id": 73,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Rhea in Greek mythology?",
            "options": ["Mother of Zeus", "Goddess of Love", "Goddess of War", "Goddess of Wisdom"],
            "answer": "Mother of Zeus"
        },
        {
            "id": 74,
            "uuid": str(uuid.uuid4()),
            "question": "What is Iris the goddess of?",
            "options": ["War", "The Rainbow and Messenger", "Love", "Wisdom"],
            "answer": "The Rainbow and Messenger"
        },
        {
            "id": 75,
            "uuid": str(uuid.uuid4()),
            "question": "What are the three Graces called in Greek mythology?",
            "options": ["Moirai", "Charites", "Muses", "Furies"],
            "answer": "Charites"
        },
        # Mythologie hindoue
        {
            "id": 76,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Brahma in Hindu mythology?",
            "options": ["God of Destruction", "Creator God", "Preserver God", "God of War"],
            "answer": "Creator God"
        },
        {
            "id": 77,
            "uuid": str(uuid.uuid4()),
            "question": "What is Vishnu the god of?",
            "options": ["Destruction", "Preservation", "Creation", "War"],
            "answer": "Preservation"
        },
        {
            "id": 78,
            "uuid": str(uuid.uuid4()),
            "question": "What is Shiva the god of?",
            "options": ["Creation", "Preservation", "Destruction and Transformation", "War"],
            "answer": "Destruction and Transformation"
        },
        {
            "id": 79,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Lakshmi in Hindu mythology?",
            "options": ["Goddess of War", "Goddess of Wealth and Prosperity", "Goddess of Knowledge", "Goddess of Power"],
            "answer": "Goddess of Wealth and Prosperity"
        },
        {
            "id": 80,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Lakshmi's consort?",
            "options": ["Brahma", "Vishnu", "Shiva", "Ganesha"],
            "answer": "Vishnu"
        },
        {
            "id": 81,
            "uuid": str(uuid.uuid4()),
            "question": "What is Saraswati the goddess of?",
            "options": ["Wealth", "Knowledge and Arts", "War", "Power"],
            "answer": "Knowledge and Arts"
        },
        {
            "id": 82,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Saraswati's consort?",
            "options": ["Brahma", "Vishnu", "Shiva", "Indra"],
            "answer": "Brahma"
        },
        {
            "id": 83,
            "uuid": str(uuid.uuid4()),
            "question": "What is Parvati the goddess of?",
            "options": ["Wealth", "Knowledge", "Power and Devotion", "War"],
            "answer": "Power and Devotion"
        },
        {
            "id": 84,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Parvati's consort?",
            "options": ["Brahma", "Vishnu", "Shiva", "Krishna"],
            "answer": "Shiva"
        },
        {
            "id": 85,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Ganesha in Hindu mythology?",
            "options": ["God of War", "God of Wisdom and Remover of Obstacles", "God of Love", "God of Fire"],
            "answer": "God of Wisdom and Remover of Obstacles"
        },
        {
            "id": 86,
            "uuid": str(uuid.uuid4()),
            "question": "Who are Ganesha's parents?",
            "options": ["Brahma and Saraswati", "Vishnu and Lakshmi", "Shiva and Parvati", "Indra and Indrani"],
            "answer": "Shiva and Parvati"
        },
        {
            "id": 87,
            "uuid": str(uuid.uuid4()),
            "question": "What is Hanuman the god of?",
            "options": ["War", "Strength and Devotion", "Knowledge", "Wealth"],
            "answer": "Strength and Devotion"
        },
        {
            "id": 88,
            "uuid": str(uuid.uuid4()),
            "question": "What is Indra the god of?",
            "options": ["Fire", "Thunder and Rain", "Wind", "Earth"],
            "answer": "Thunder and Rain"
        },
        {
            "id": 89,
            "uuid": str(uuid.uuid4()),
            "question": "What is Agni the god of?",
            "options": ["Water", "Fire", "Wind", "Earth"],
            "answer": "Fire"
        },
        {
            "id": 90,
            "uuid": str(uuid.uuid4()),
            "question": "What is Vayu the god of?",
            "options": ["Fire", "Water", "Wind", "Earth"],
            "answer": "Wind"
        },
        {
            "id": 91,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Kali in Hindu mythology?",
            "options": ["Goddess of Wealth", "Goddess of Time and Death", "Goddess of Knowledge", "Goddess of Love"],
            "answer": "Goddess of Time and Death"
        },
        {
            "id": 92,
            "uuid": str(uuid.uuid4()),
            "question": "What is Durga the goddess of?",
            "options": ["Wealth", "Warrior Goddess", "Knowledge", "Love"],
            "answer": "Warrior Goddess"
        },
        {
            "id": 93,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Kartikeya in Hindu mythology?",
            "options": ["God of Love", "God of War", "God of Wisdom", "God of Fire"],
            "answer": "God of War"
        },
        {
            "id": 94,
            "uuid": str(uuid.uuid4()),
            "question": "Who is Kartikeya's brother?",
            "options": ["Krishna", "Rama", "Ganesha", "Hanuman"],
            "answer": "Ganesha"
        },
        {
            "id": 95,
            "uuid": str(uuid.uuid4()),
            "question": "What is Yama the god of?",
            "options": ["Life", "Death and Dharma", "War", "Knowledge"],
            "answer": "Death and Dharma"
        },
        {
            "id": 96,
            "uuid": str(uuid.uuid4()),
            "question": "What is Kamadeva the god of?",
            "options": ["War", "Love and Desire", "Knowledge", "Wealth"],
            "answer": "Love and Desire"
        },
        {
            "id": 97,
            "uuid": str(uuid.uuid4()),
            "question": "What is Surya the god of?",
            "options": ["The Moon", "The Sun", "The Stars", "Fire"],
            "answer": "The Sun"
        },
        {
            "id": 98,
            "uuid": str(uuid.uuid4()),
            "question": "What is Chandra the god of?",
            "options": ["The Sun", "The Moon", "The Stars", "Fire"],
            "answer": "The Moon"
        },
        {
            "id": 99,
            "uuid": str(uuid.uuid4()),
            "question": "What is Varuna the god of?",
            "options": ["Fire", "Water and Cosmic Order", "Wind", "Earth"],
            "answer": "Water and Cosmic Order"
        },
        {
            "id": 100,
            "uuid": str(uuid.uuid4()),
            "question": "What is the Trimurti in Hindu mythology?",
            "options": ["Three goddesses", "Brahma, Vishnu, and Shiva", "Three avatars of Vishnu", "Three sacred texts"],
            "answer": "Brahma, Vishnu, and Shiva"
        }
    ]
}

# Ajouter le quiz de mythologie
data['quizzes'].append(mythology_quiz)

# Sauvegarder le fichier JSON modifié
with open('C:/Users/athom/IdeaProjects/quizz1/src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Quiz de mythologie ajouté avec succès!")
print(f"Nombre total de quiz: {len(data['quizzes'])}")
print(f"Nombre de questions dans le quiz de mythologie: {len(mythology_quiz['questions'])}")

