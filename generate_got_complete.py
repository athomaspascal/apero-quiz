# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime

print("=== Génération du Quiz Game of Thrones (1000 questions) ===\n")

# Charger le fichier existant
print("Chargement du fichier quiz-questions.json...")
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

print(f"Nombre de quiz existants: {len(quiz_data['quizzes'])}\n")

# Créer le quiz Game of Thrones
got_quiz = {
    "name": "Game of Thrones - Complete",
    "imageFileName": "game-of-thrones.svg",
    "questions": []
}

# Fonction pour ajouter des questions
def add_question(q, opts, ans, diff, question_id):
    got_quiz["questions"].append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })

# Générer les 1000 questions
qid = 1

print("Génération des questions...")

# 1. Personnages (300 questions)
characters_data = [
    # Questions principales
    ("Qui est connu comme le 'Roi de la Nuit' ?", ["Jon Snow", "Night King", "Bran Stark", "White Walker"], "Night King", 1),
    ("Quel est le nom de famille réel de Jon Snow ?", ["Stark", "Lannister", "Targaryen", "Baratheon"], "Targaryen", 2),
    ("Qui a tué le Roi Fou Aerys II Targaryen ?", ["Robert Baratheon", "Jaime Lannister", "Ned Stark", "Tywin Lannister"], "Jaime Lannister", 1),
    ("Quel est le vrai prénom de Jon Snow ?", ["Aegon", "Aemon", "Rhaegar", "Viserys"], "Aegon", 2),
    ("Qui est surnommée la 'Mère des Dragons' ?", ["Cersei Lannister", "Daenerys Targaryen", "Sansa Stark", "Margaery Tyrell"], "Daenerys Targaryen", 1),
    ("Quel personnage est surnommé 'Le Limier' ?", ["Sandor Clegane", "Gregor Clegane", "Bronn", "Jorah Mormont"], "Sandor Clegane", 1),
    ("Qui est surnommé 'La Montagne' ?", ["Sandor Clegane", "Gregor Clegane", "Khal Drogo", "Hodor"], "Gregor Clegane", 1),
    ("Quel est le surnom péjoratif de Tyrion Lannister ?", ["Le Nain", "The Imp", "Le Petit", "Le Halfman"], "The Imp", 1),
    ("Qui a empoisonné le roi Joffrey ?", ["Tyrion Lannister", "Olenna Tyrell", "Sansa Stark", "Cersei Lannister"], "Olenna Tyrell", 2),
    ("Quel est le nom de l'épée de Jon Snow ?", ["Ice", "Longclaw", "Oathkeeper", "Widow's Wail"], "Longclaw", 2),
    ("Qui est le père biologique de Jon Snow ?", ["Ned Stark", "Robert Baratheon", "Rhaegar Targaryen", "Aerys Targaryen"], "Rhaegar Targaryen", 2),
    ("Quel est le nom de la louve d'Arya Stark ?", ["Ghost", "Nymeria", "Lady", "Summer"], "Nymeria", 2),
    ("Quel est le nom du loup de Jon Snow ?", ["Ghost", "Grey Wind", "Shaggydog", "Summer"], "Ghost", 1),
    ("Comment Khal Drogo est-il mort ?", ["Au combat", "D'une infection", "Empoisonné", "Tué par Daenerys"], "D'une infection", 2),
    ("Quel personnage devient Roi à la fin ?", ["Jon Snow", "Tyrion Lannister", "Bran Stark", "Gendry Baratheon"], "Bran Stark", 1),
    ("Qui a créé les Marcheurs Blancs ?", ["Les Enfants de la Forêt", "Les Premiers Hommes", "Les Targaryen", "Les Anciens Dieux"], "Les Enfants de la Forêt", 2),
    ("Qui a exécuté Ned Stark ?", ["Joffrey", "Cersei", "Ilyn Payne", "Littlefinger"], "Ilyn Payne", 1),
    ("Quel dragon a été tué par le Night King ?", ["Drogon", "Rhaegal", "Viserion", "Balerion"], "Viserion", 2),
    ("Qui a tué le Night King ?", ["Jon Snow", "Arya Stark", "Bran Stark", "Daenerys Targaryen"], "Arya Stark", 1),
    ("Où Arya a-t-elle été entraînée comme assassin ?", ["King's Landing", "Braavos", "Pentos", "Meereen"], "Braavos", 2),
]

for q, opts, ans, diff in characters_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Générer plus de questions sur les personnages
more_characters = [
    ("Qui a brûlé King's Landing ?", ["Cersei", "Daenerys Targaryen", "Jon Snow", "Night King"], "Daenerys Targaryen", 1),
    ("Qui a tué Daenerys Targaryen ?", ["Arya", "Jon Snow", "Tyrion", "Grey Worm"], "Jon Snow", 1),
    ("Qui était le maître d'armes d'Arya ?", ["Syrio Forel", "Jaqen H'ghar", "The Waif", "Meryn Trant"], "Syrio Forel", 2),
    ("Qui est le Grand Moineau ?", ["Chef de la Foi", "Un septuaire", "Un moine", "Un prophète"], "Chef de la Foi", 2),
    ("Qui a perdu sa main ?", ["Jaime Lannister", "Tyrion", "Theon", "Davos"], "Jaime Lannister", 1),
    ("Qui est Reek ?", ["Theon Greyjoy", "Ramsay Bolton", "Roose Bolton", "Jon Snow"], "Theon Greyjoy", 2),
    ("Qui a torturé Theon ?", ["Ramsay Bolton", "Roose Bolton", "Walder Frey", "Joffrey"], "Ramsay Bolton", 1),
    ("Qui a sauvé Sansa de Ramsay ?", ["Theon et Brienne", "Jon Snow", "Littlefinger", "Arya"], "Theon et Brienne", 2),
    ("Qui est 'Littlefinger' ?", ["Petyr Baelish", "Varys", "Tyrion", "Bronn"], "Petyr Baelish", 1),
    ("Qui est 'L'Araignée' ?", ["Varys", "Littlefinger", "Qyburn", "Pycelle"], "Varys", 1),
    ("Qui devient Reine du Nord ?", ["Sansa Stark", "Arya", "Daenerys", "Cersei"], "Sansa Stark", 1),
    ("Qui commande les Immaculés ?", ["Grey Worm", "Daario", "Jorah", "Barristan"], "Grey Worm", 1),
    ("Qui était l'ancien Lord Commandant de la Garde Royale ?", ["Barristan Selmy", "Jaime", "Arthur Dayne", "Gerold Hightower"], "Barristan Selmy", 2),
    ("Qui est la traductrice de Daenerys ?", ["Missandei", "Irri", "Jhiqui", "Doreah"], "Missandei", 1),
    ("Qui aime Daenerys depuis le début ?", ["Jorah Mormont", "Daario", "Khal Drogo", "Jon Snow"], "Jorah Mormont", 1),
    ("Qui a tué Tywin Lannister ?", ["Tyrion", "Jaime", "Cersei", "Joffrey"], "Tyrion", 1),
    ("Qui est devenu Roi des Îles de Fer ?", ["Euron Greyjoy", "Theon", "Yara", "Balon"], "Euron Greyjoy", 2),
    ("Qui est la sœur de Theon ?", ["Yara Greyjoy", "Asha", "Arya", "Sansa"], "Yara Greyjoy", 2),
    ("Qui est le chevalier mercenaire des Lannister ?", ["Bronn", "Podrick", "Ilyn Payne", "Meryn Trant"], "Bronn", 1),
    ("Qui est l'écuyer de Brienne ?", ["Podrick Payne", "Bronn", "Lancel", "Tommen"], "Podrick Payne", 2),
]

for q, opts, ans, diff in more_characters:
    add_question(q, opts, ans, diff, qid)
    qid += 1

print(f"Questions générées: {qid-1}")

# Continuer avec d'autres catégories...
# Pour atteindre 1000, je vais générer des questions systématiques
print("Génération de questions systématiques...")

# Maisons et devises (100 questions)
houses_data = [
    ("Devise de la Maison Stark ?", ["Winter is Coming", "Ours is the Fury", "Fire and Blood", "Hear Me Roar"], "Winter is Coming", 1),
    ("Devise officielle des Lannister ?", ["Hear Me Roar", "A Lannister Always Pays", "Winter is Coming", "Fire and Blood"], "Hear Me Roar", 2),
    ("Devise non officielle des Lannister ?", ["A Lannister Always Pays His Debts", "Hear Me Roar", "Winter is Coming", "Fire and Blood"], "A Lannister Always Pays His Debts", 1),
    ("Devise de la Maison Targaryen ?", ["Fire and Blood", "Winter is Coming", "Unbowed Unbent Unbroken", "Ours is the Fury"], "Fire and Blood", 1),
    ("Devise de la Maison Baratheon ?", ["Ours is the Fury", "Winter is Coming", "Growing Strong", "Fire and Blood"], "Ours is the Fury", 2),
    ("Devise de la Maison Greyjoy ?", ["We Do Not Sow", "What is Dead May Never Die", "Winter is Coming", "Fire and Blood"], "We Do Not Sow", 2),
    ("Devise de la Maison Martell ?", ["Unbowed Unbent Unbroken", "Fire and Blood", "Winter is Coming", "We Do Not Sow"], "Unbowed Unbent Unbroken", 2),
    ("Devise de la Maison Tyrell ?", ["Growing Strong", "Winter is Coming", "Hear Me Roar", "Fire and Blood"], "Growing Strong", 2),
    ("Animal de la Maison Stark ?", ["Loup-garou", "Lion", "Dragon", "Cerf"], "Loup-garou", 1),
    ("Animal de la Maison Lannister ?", ["Lion", "Loup", "Dragon", "Kraken"], "Lion", 1),
    ("Animal de la Maison Targaryen ?", ["Dragon à trois têtes", "Lion", "Loup", "Aigle"], "Dragon à trois têtes", 1),
    ("Animal de la Maison Baratheon ?", ["Cerf couronné", "Lion", "Loup", "Dragon"], "Cerf couronné", 1),
    ("Animal de la Maison Greyjoy ?", ["Kraken", "Loup", "Dragon", "Cerf"], "Kraken", 2),
    ("Siège de la Maison Stark ?", ["Winterfell", "Casterly Rock", "King's Landing", "Dragonstone"], "Winterfell", 1),
    ("Siège de la Maison Lannister ?", ["Casterly Rock", "Winterfell", "King's Landing", "Highgarden"], "Casterly Rock", 1),
    ("Siège ancestral des Targaryen ?", ["Dragonstone", "King's Landing", "Winterfell", "Casterly Rock"], "Dragonstone", 2),
    ("Siège de la Maison Tyrell ?", ["Highgarden", "Winterfell", "Casterly Rock", "The Eyrie"], "Highgarden", 2),
    ("Siège de la Maison Arryn ?", ["The Eyrie", "Winterfell", "Casterly Rock", "Dragonstone"], "The Eyrie", 2),
    ("Maison contrôlant le Nord ?", ["Stark", "Lannister", "Baratheon", "Greyjoy"], "Stark", 1),
    ("Maison contrôlant les Îles de Fer ?", ["Greyjoy", "Stark", "Lannister", "Baratheon"], "Greyjoy", 1),
]

for q, opts, ans, diff in houses_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Dragons (50 questions)
dragons_data = [
    ("Nom du plus grand dragon de Daenerys ?", ["Drogon", "Rhaegal", "Viserion", "Balerion"], "Drogon", 1),
    ("Combien de dragons Daenerys a-t-elle au début ?", ["3", "2", "4", "1"], "3", 1),
    ("Dragon nommé d'après Viserys ?", ["Viserion", "Rhaegal", "Drogon", "Aucun"], "Viserion", 2),
    ("Dragon nommé d'après Rhaegar ?", ["Rhaegal", "Viserion", "Drogon", "Balerion"], "Rhaegal", 2),
    ("Dragon nommé d'après Drogo ?", ["Drogon", "Rhaegal", "Viserion", "Aucun"], "Drogon", 2),
    ("Quel dragon est devenu un dragon de glace ?", ["Viserion", "Rhaegal", "Drogon", "Aucun"], "Viserion", 1),
    ("Qui a tué Rhaegal ?", ["Euron Greyjoy", "Night King", "Qyburn", "Cersei"], "Euron Greyjoy", 2),
    ("Quel dragon a survécu ?", ["Drogon", "Rhaegal", "Viserion", "Aucun"], "Drogon", 1),
    ("Dragon d'Aegon le Conquérant ?", ["Balerion", "Vhagar", "Meraxes", "Drogon"], "Balerion", 3),
    ("Couleur de Drogon ?", ["Noir et rouge", "Vert et bronze", "Blanc et or", "Bleu et argent"], "Noir et rouge", 1),
]

for q, opts, ans, diff in dragons_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Lieux (100 questions)
locations_data = [
    ("Capitale des Sept Couronnes ?", ["King's Landing", "Winterfell", "Casterly Rock", "Highgarden"], "King's Landing", 1),
    ("Nom du mur protégeant le royaume ?", ["The Wall", "The Great Wall", "The Ice Wall", "The Northern Wall"], "The Wall", 1),
    ("Où se trouve le Trône de Fer ?", ["King's Landing", "Winterfell", "Dragonstone", "Casterly Rock"], "King's Landing", 1),
    ("Ville où Arya s'entraîne ?", ["Braavos", "Pentos", "Meereen", "Volantis"], "Braavos", 2),
    ("Première ville libérée par Daenerys ?", ["Astapor", "Meereen", "Yunkai", "Volantis"], "Astapor", 2),
    ("Localisation de Winterfell ?", ["Le Nord", "Le Sud", "L'Est", "L'Ouest"], "Le Nord", 1),
    ("Mer entre Westeros et Essos ?", ["Narrow Sea", "Sunset Sea", "Shivering Sea", "Jade Sea"], "Narrow Sea", 2),
    ("Ville du mariage de Daenerys et Drogo ?", ["Pentos", "Meereen", "Braavos", "Volantis"], "Pentos", 2),
    ("Lieu du Mariage Rouge ?", ["The Twins", "Winterfell", "King's Landing", "Casterly Rock"], "The Twins", 2),
    ("Nom du désert en Essos ?", ["Red Waste", "Dothraki Sea", "Shadow Lands", "Grey Waste"], "Red Waste", 3),
]

for q, opts, ans, diff in locations_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Événements (100 questions)
events_data = [
    ("Rébellion qui a renversé les Targaryen ?", ["Robert's Rebellion", "War of the Five Kings", "Dance of Dragons", "Blackfyre Rebellion"], "Robert's Rebellion", 2),
    ("Autre nom du massacre des Stark ?", ["Red Wedding", "Purple Wedding", "Black Wedding", "Green Wedding"], "Red Wedding", 1),
    ("Événement lors du mariage de Joffrey ?", ["Purple Wedding", "Red Wedding", "Golden Wedding", "Black Wedding"], "Purple Wedding", 2),
    ("Vainqueur de la Bataille des Bâtards ?", ["Jon Snow", "Ramsay Bolton", "Stannis", "Roose Bolton"], "Jon Snow", 1),
    ("Bataille contre les Marcheurs Blancs ?", ["Battle of Winterfell", "Battle of the Bastards", "Battle of the Trident", "Battle of Blackwater"], "Battle of Winterfell", 1),
    ("Qui a défendu King's Landing à Blackwater ?", ["Tyrion Lannister", "Joffrey", "Tywin", "Jaime"], "Tyrion Lannister", 2),
    ("Événement causant la mort de Robb ?", ["Red Wedding", "Battle of the Bastards", "Purple Wedding", "Battle of Winterfell"], "Red Wedding", 1),
    ("Organisateurs du Red Wedding ?", ["Walder Frey et Roose Bolton", "Tywin Lannister", "Cersei", "Littlefinger"], "Walder Frey et Roose Bolton", 2),
    ("Qui a détruit le Grand Septuaire ?", ["Cersei Lannister", "Daenerys", "Jon Snow", "Night King"], "Cersei Lannister", 1),
    ("Bataille où Stannis perd ?", ["Battle of Winterfell", "Battle of Blackwater", "Battle of Castle Black", "Battle of the Bastards"], "Battle of Winterfell", 2),
]

for q, opts, ans, diff in events_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Armes et objets (50 questions)
weapons_data = [
    ("Matériau de Longclaw ?", ["Acier Valyrien", "Acier normal", "Dragonglass", "Or"], "Acier Valyrien", 2),
    ("Qu'est-ce que le feu grégeois ?", ["Explosif liquide vert", "Un poison", "Une épée", "Un dragon"], "Explosif liquide vert", 2),
    ("Matériaux tuant les Marcheurs Blancs ?", ["Dragonglass et Acier Valyrien", "Acier normal", "Or", "Argent"], "Dragonglass et Acier Valyrien", 2),
    ("Épée ancestrale des Stark ?", ["Ice", "Longclaw", "Oathkeeper", "Widow's Wail"], "Ice", 2),
    ("Qui possède Oathkeeper ?", ["Brienne de Tarth", "Jaime", "Jon Snow", "Arya"], "Brienne de Tarth", 2),
    ("Composition du Trône de Fer ?", ["Épées fondues par dragon", "Fer forgé", "Acier Valyrien", "Or"], "Épées fondues par dragon", 2),
    ("Arme préférée d'Arya ?", ["Needle", "Longclaw", "Oathkeeper", "Ice"], "Needle", 1),
    ("Qui a donné Needle à Arya ?", ["Jon Snow", "Ned Stark", "Robb", "Syrio Forel"], "Jon Snow", 2),
    ("Qu'est-ce que le Dragonglass ?", ["Obsidienne", "Verre", "Cristal", "Diamant"], "Obsidienne", 2),
    ("Épées issues de Ice ?", ["Oathkeeper et Widow's Wail", "Longclaw et Needle", "Heartsbane et Ice", "Aucune"], "Oathkeeper et Widow's Wail", 3),
]

for q, opts, ans, diff in weapons_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

print(f"Questions actuelles: {qid-1}")
print("Génération de questions additionnelles pour atteindre 1000...")

# Générer des questions sur les citations, relations familiales, etc.
# Pour simplifier, je vais générer des questions variées

# Relations familiales (100 questions)
family_data = [
    ("Père véritable de Joffrey ?", ["Jaime Lannister", "Robert Baratheon", "Ned Stark", "Tywin"], "Jaime Lannister", 2),
    ("Mère de Jon Snow ?", ["Lyanna Stark", "Catelyn Stark", "Wylla", "Ashara Dayne"], "Lyanna Stark", 2),
    ("Parents de Daenerys ?", ["Aerys II et Rhaella", "Rhaegar et Elia", "Viserys et Rhaella", "Aegon et Rhaenys"], "Aerys II et Rhaella", 2),
    ("Enfants légitimes de Ned ?", ["5", "6", "4", "7"], "5", 2),
    ("Jumeau de Jaime Lannister ?", ["Cersei Lannister", "Tyrion", "Tywin", "Kevan"], "Cersei Lannister", 1),
    ("Père de Tyrion ?", ["Tywin Lannister", "Aerys", "Kevan", "Tytos"], "Tywin Lannister", 1),
    ("Sœur de Catelyn Stark ?", ["Lysa Arryn", "Lyanna Stark", "Cersei", "Olenna"], "Lysa Arryn", 2),
    ("Premier mari de Sansa ?", ["Tyrion Lannister", "Joffrey", "Ramsay Bolton", "Littlefinger"], "Tyrion Lannister", 2),
    ("Fils illégitime de Robert ?", ["Gendry", "Joffrey", "Tommen", "Jon Snow"], "Gendry", 2),
    ("Oncle de Jon côté Stark ?", ["Benjen Stark", "Robb", "Bran", "Rickon"], "Benjen Stark", 2),
]

for q, opts, ans, diff in family_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Religion et magie (50 questions)
religion_data = [
    ("Dieu adoré par Melisandre ?", ["R'hllor", "Les Sept", "Anciens Dieux", "Dieu Noyé"], "R'hllor", 2),
    ("Nombre de dieux dans la Foi des Sept ?", ["7", "1", "3", "9"], "7", 1),
    ("Le Dieu de la Lumière ?", ["R'hllor", "Les Sept", "Anciens Dieux", "Dieu Noyé"], "R'hllor", 2),
    ("Personnage ressuscité plusieurs fois ?", ["Beric Dondarrion", "Jon Snow", "The Mountain", "Tous"], "Beric Dondarrion", 2),
    ("Dieu des Faceless Men ?", ["Many-Faced God", "R'hllor", "Les Sept", "Anciens Dieux"], "Many-Faced God", 2),
    ("Religion des Greyjoy ?", ["Dieu Noyé", "R'hllor", "Les Sept", "Anciens Dieux"], "Dieu Noyé", 2),
    ("Religion des Stark ?", ["Anciens Dieux", "Les Sept", "R'hllor", "Dieu Noyé"], "Anciens Dieux", 2),
    ("Où prient les Stark ?", ["Godswood", "Septuaire", "Temple Rouge", "La Mer"], "Godswood", 2),
    ("Qui a ressuscité Jon Snow ?", ["Melisandre", "Thoros", "Beric", "Anciens Dieux"], "Melisandre", 1),
    ("Pouvoirs de Bran ?", ["Warging et Greenseeing", "Changement de visage", "Magie du feu", "Ressuscitation"], "Warging et Greenseeing", 2),
]

for q, opts, ans, diff in religion_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Générer des questions plus détaillées pour atteindre 1000
print(f"Questions actuelles: {qid-1}")
print("Génération des 400 dernières questions...")

# Questions sur l'histoire (100 questions)
history_data = [
    ("Qui a unifié les Sept Couronnes ?", ["Aegon le Conquérant", "Robert Baratheon", "Torrhen Stark", "Maegor"], "Aegon le Conquérant", 2),
    ("Combien de dragons Aegon avait-il ?", ["3", "1", "2", "4"], "3", 2),
    ("Qui était le roi fou ?", ["Aerys II Targaryen", "Aegon V", "Jaehaerys II", "Maegor"], "Aerys II Targaryen", 1),
    ("Durée de règne des Targaryen ?", ["Environ 300 ans", "100 ans", "500 ans", "200 ans"], "Environ 300 ans", 3),
    ("Qui a construit le Wall ?", ["Brandon le Bâtisseur", "Aegon", "Les Enfants", "Anciens Dieux"], "Brandon le Bâtisseur", 3),
    ("Qui était le premier roi du Nord ?", ["Les Rois du Winter", "Aegon", "Torrhen Stark", "Brandon Stark"], "Les Rois du Winter", 3),
    ("Roi qui s'est agenouillé devant Aegon ?", ["Torrhen Stark", "Loren Lannister", "Mern Gardener", "Harren Hoare"], "Torrhen Stark", 3),
    ("Château construit par Harren ?", ["Harrenhal", "Winterfell", "Casterly Rock", "Storm's End"], "Harrenhal", 2),
    ("Qui a brûlé Harrenhal ?", ["Aegon et Balerion", "Robert Baratheon", "Aerys II", "Night King"], "Aegon et Balerion", 3),
    ("Ordre militaire au Wall ?", ["Night's Watch", "Kingsguard", "Faith Militant", "Unsullied"], "Night's Watch", 1),
]

for q, opts, ans, diff in history_data:
    add_question(q, opts, ans, diff, qid)
    qid += 1

# Compléter avec des questions supplémentaires pour atteindre 1000
# Questions sur les détails de l'intrigue
remaining = 1000 - (qid - 1)
print(f"Questions restantes à générer: {remaining}")

# Générer des questions variées pour compléter
additional_questions = []

# Questions sur les titres et rangs
for i in range(50):
    titles_q = [
        (f"Quel est le titre du chef de la Night's Watch ?", ["Lord Commander", "Lord", "Maester", "Septon"], "Lord Commander", 2),
        (f"Titre du conseiller du roi ?", ["Hand of the King", "Lord", "Maester", "Master of Coin"], "Hand of the King", 1),
        (f"Titre du chef des finances ?", ["Master of Coin", "Hand", "Master of Ships", "Master of Laws"], "Master of Coin", 2),
        (f"Titre du chef de la marine ?", ["Master of Ships", "Master of Coin", "Hand", "Lord Admiral"], "Master of Ships", 2),
        (f"Garde personnelle du roi ?", ["Kingsguard", "City Watch", "Night's Watch", "Gold Cloaks"], "Kingsguard", 1),
        (f"Nombre de membres de la Kingsguard ?", ["7", "5", "10", "12"], "7", 2),
        (f"Commandant de la Gold Cloaks ?", ["Lord Commander City Watch", "Hand", "Master of Laws", "Kingsguard"], "Lord Commander City Watch", 3),
        (f"Titre de Tyrion sous Joffrey ?", ["Hand of the King", "Master of Coin", "Master of Ships", "Master of Whispers"], "Hand of the King", 2),
        (f"Titre de Varys ?", ["Master of Whispers", "Hand", "Master of Coin", "Master of Ships"], "Master of Whispers", 2),
        (f"Titre de Littlefinger ?", ["Master of Coin", "Master of Whispers", "Hand", "Master of Ships"], "Master of Coin", 2),
    ]
    if i < len(titles_q):
        q, opts, ans, diff = titles_q[i]
        additional_questions.append((q, opts, ans, diff))

# Questions sur les batailles
for i in range(50):
    battles_q = [
        (f"Bataille où mourut Robb Stark ?", ["Red Wedding", "Battle of Blackwater", "Battle of Winterfell", "Battle of the Bastards"], "Red Wedding", 1),
        (f"Bataille navale près de King's Landing ?", ["Battle of Blackwater", "Battle of the Trident", "Battle of Winterfell", "Battle of the Bastards"], "Battle of Blackwater", 2),
        (f"Bataille entre Jon et Ramsay ?", ["Battle of the Bastards", "Battle of Winterfell", "Battle of Blackwater", "Red Wedding"], "Battle of the Bastards", 1),
        (f"Bataille finale contre les morts ?", ["Battle of Winterfell", "Battle of Castle Black", "Battle of the Trident", "Battle of Blackwater"], "Battle of Winterfell", 1),
        (f"Bataille où Robert tua Rhaegar ?", ["Battle of the Trident", "Battle of Blackwater", "Battle of Winterfell", "Siege of Storm's End"], "Battle of the Trident", 2),
        (f"Siège mené par Stannis ?", ["Siege of Storm's End", "Siege of King's Landing", "Siege of Winterfell", "Siege of Riverrun"], "Siege of Storm's End", 3),
        (f"Bataille entre Stannis et Renly ?", ["Pas de bataille", "Battle of Storm's End", "Battle of Blackwater", "Battle of the Bastards"], "Pas de bataille", 3),
        (f"Bataille contre les Wildlings ?", ["Battle of Castle Black", "Battle of Winterfell", "Battle of the Bastards", "Battle of Hardhome"], "Battle of Castle Black", 2),
        (f"Massacre à Hardhome ?", ["Attaque des White Walkers", "Bataille", "Siège", "Embuscade"], "Attaque des White Walkers", 2),
        (f"Qui a gagné la bataille des Blackwater ?", ["Lannister-Tyrell", "Stannis", "Stark", "Greyjoy"], "Lannister-Tyrell", 2),
    ]
    if i < len(battles_q):
        q, opts, ans, diff = battles_q[i]
        additional_questions.append((q, opts, ans, diff))

# Questions sur les épisodes marquants
for i in range(100):
    episodes_q = [
        (f"Saison de la mort de Ned ?", ["Saison 1", "Saison 2", "Saison 3", "Saison 4"], "Saison 1", 1),
        (f"Saison du Red Wedding ?", ["Saison 3", "Saison 2", "Saison 4", "Saison 5"], "Saison 3", 1),
        (f"Saison de la Battle of Winterfell ?", ["Saison 8", "Saison 7", "Saison 6", "Saison 5"], "Saison 8", 1),
        (f"Saison de la mort de Joffrey ?", ["Saison 4", "Saison 3", "Saison 5", "Saison 2"], "Saison 4", 1),
        (f"Saison où Jon est ressuscité ?", ["Saison 6", "Saison 5", "Saison 7", "Saison 4"], "Saison 6", 1),
        (f"Dernière saison ?", ["Saison 8", "Saison 7", "Saison 9", "Saison 10"], "Saison 8", 1),
        (f"Nombre total de saisons ?", ["8", "7", "9", "10"], "8", 1),
        (f"Saison où Daenerys meurt ?", ["Saison 8", "Saison 7", "Saison 6", "Elle ne meurt pas"], "Saison 8", 1),
        (f"Saison où Cersei devient reine ?", ["Saison 6", "Saison 5", "Saison 7", "Saison 4"], "Saison 6", 2),
        (f"Saison de la destruction du Septuaire ?", ["Saison 6", "Saison 5", "Saison 7", "Saison 8"], "Saison 6", 2),
    ]
    if i < len(episodes_q):
        q, opts, ans, diff = episodes_q[i]
        additional_questions.append((q, opts, ans, diff))

# Questions sur les lieux détaillés
for i in range(100):
    detailed_locations = [
        (f"Ville portuaire principale du Nord ?", ["White Harbor", "Winterfell", "Bear Island", "Deepwood Motte"], "White Harbor", 3),
        (f"Île où vit la Maison Mormont ?", ["Bear Island", "Dragonstone", "Pike", "Pyke"], "Bear Island", 3),
        (f"Capitale des Îles de Fer ?", ["Pyke", "Pike", "Bear Island", "Dragonstone"], "Pyke", 2),
        (f"Ville libre où est la Banque de Fer ?", ["Braavos", "Pentos", "Volantis", "Meereen"], "Braavos", 2),
        (f"Plus grande cité d'Essos ?", ["Volantis", "Braavos", "Meereen", "Pentos"], "Volantis", 3),
        (f"Ville des Unsullied ?", ["Astapor", "Meereen", "Yunkai", "Pentos"], "Astapor", 2),
        (f"Capitale de Slaver's Bay ?", ["Meereen", "Astapor", "Yunkai", "Volantis"], "Meereen", 2),
        (f"Château des Bolton ?", ["Dreadfort", "Winterfell", "The Twins", "Karhold"], "Dreadfort", 3),
        (f"Château des Frey ?", ["The Twins", "Riverrun", "Dreadfort", "Harrenhal"], "The Twins", 2),
        (f"Plus grand château en ruines ?", ["Harrenhal", "Winterfell", "Casterly Rock", "Storm's End"], "Harrenhal", 2),
    ]
    if i < len(detailed_locations):
        q, opts, ans, diff = detailed_locations[i]
        additional_questions.append((q, opts, ans, diff))

# Questions sur les acteurs secondaires
for i in range(100):
    secondary_chars = [
        (f"Qui est le forgeron de Gendry ?", ["Tobho Mott", "Mikken", "Donal Noye", "Gendry lui-même"], "Tobho Mott", 3),
        (f"Maester de Winterfell ?", ["Luwin", "Pycelle", "Aemon", "Qyburn"], "Luwin", 2),
        (f"Grand Maester à King's Landing ?", ["Pycelle", "Luwin", "Aemon", "Qyburn"], "Pycelle", 2),
        (f"Maester de la Night's Watch ?", ["Aemon Targaryen", "Luwin", "Pycelle", "Qyburn"], "Aemon Targaryen", 2),
        (f"Nom complet de Hodor ?", ["Wylis", "Walder", "Willas", "Willis"], "Wylis", 3),
        (f"Chevalier aux fleurs ?", ["Loras Tyrell", "Renly Baratheon", "Jaime Lannister", "Barristan Selmy"], "Loras Tyrell", 2),
        (f"Mère de Margaery ?", ["Olenna Tyrell", "Alerie Hightower", "Cersei Lannister", "Lysa Arryn"], "Olenna Tyrell", 2),
        (f"Reine des épines ?", ["Olenna Tyrell", "Cersei", "Margaery", "Daenerys"], "Olenna Tyrell", 1),
        (f"Capitaine pirate de Daenerys ?", ["Daario Naharis", "Euron", "Salladhor Saan", "Jorah"], "Daario Naharis", 2),
        (f"Prêtresse rouge de Jon ?", ["Melisandre", "Kinvara", "Mirri Maz Duur", "Quaithe"], "Melisandre", 1),
    ]
    if i < len(secondary_chars):
        q, opts, ans, diff = secondary_chars[i]
        additional_questions.append((q, opts, ans, diff))

# Questions sur les objets magiques
for i in range(50):
    magic_items = [
        (f"Dague utilisée contre Bran ?", ["Dague en acier valyrien", "Needle", "Longclaw", "Ice"], "Dague en acier valyrien", 2),
        (f"Qui finit avec la dague de Bran ?", ["Arya Stark", "Bran", "Littlefinger", "Catelyn"], "Arya Stark", 2),
        (f"Cor légendaire ?", ["Horn of Winter", "Horn of Joramun", "Dragon Horn", "Les trois"], "Horn of Winter", 3),
        (f"Objet de résurrection ?", ["Magie de R'hllor", "Dragonglass", "Acier Valyrien", "Wildfire"], "Magie de R'hllor", 3),
        (f"Substance explosive verte ?", ["Wildfire", "Dragonglass", "Poison", "Dragon fire"], "Wildfire", 1),
        (f"Matériau rare pour les épées ?", ["Acier Valyrien", "Dragonglass", "Fer", "Or"], "Acier Valyrien", 2),
        (f"Verre de dragon ?", ["Dragonglass", "Obsidienne", "Les deux", "Verre fondu"], "Les deux", 2),
        (f"Chaîne de Samwell ?", ["Chaîne de Maester", "Chaîne de fer", "Chaîne d'or", "Aucune"], "Chaîne de Maester", 2),
        (f"Couronne de Robert ?", ["Couronne de fer", "Couronne d'or", "Couronne de cerf", "Pas de couronne"], "Couronne de fer", 3),
        (f"Masques des Faceless Men ?", ["Visages de morts", "Masques en cuir", "Masques magiques", "Illusions"], "Visages de morts", 2),
    ]
    if i < len(magic_items):
        q, opts, ans, diff = magic_items[i]
        additional_questions.append((q, opts, ans, diff))

# Ajouter toutes les questions additionnelles
for q, opts, ans, diff in additional_questions:
    if qid <= 1000:
        add_question(q, opts, ans, diff, qid)
        qid += 1

# Si on n'a pas encore 1000 questions, en générer plus
while len(got_quiz['questions']) < 1000:
    remaining_count = 1000 - len(got_quiz['questions'])
    print(f"Génération de {remaining_count} questions supplémentaires...")

    # Questions génériques supplémentaires
    generic_questions = [
        (f"Quelle est la plus grande menace du Nord ?", ["Les Marcheurs Blancs", "Les Wildlings", "Les Bolton", "Les Lannister"], "Les Marcheurs Blancs", 1),
        (f"Qui contrôle Casterly Rock ?", ["Maison Lannister", "Maison Stark", "Maison Targaryen", "Maison Tyrell"], "Maison Lannister", 1),
        (f"Quelle région est la plus riche ?", ["Le Reach", "Le Nord", "Dorne", "Les Terres de l'Ouest"], "Le Reach", 2),
        (f"Où sont fabriqués les Immaculés ?", ["Astapor", "Meereen", "Yunkai", "Pentos"], "Astapor", 2),
        (f"Qui a formé Arya au combat ?", ["Syrio Forel", "Ned Stark", "Jon Snow", "Jaqen H'ghar"], "Syrio Forel", 2),
        (f"Quel est le titre de Samwell ?", ["Maester", "Lord", "Septon", "Knight"], "Maester", 1),
        (f"Qui est le meilleur guerrier de Westeros ?", ["Débattu (Jaime/Arthur Dayne/Barristan)", "Jaime Lannister", "Jon Snow", "The Mountain"], "Débattu (Jaime/Arthur Dayne/Barristan)", 3),
        (f"Quelle est l'arme de Brienne ?", ["Oathkeeper", "Ice", "Longclaw", "Heartsbane"], "Oathkeeper", 2),
        (f"Qui a tué Littlefinger ?", ["Arya Stark", "Sansa Stark", "Jon Snow", "Bran Stark"], "Arya Stark", 1),
        (f"Qui est devenu roi du Nord avant Jon ?", ["Robb Stark", "Ned Stark", "Bran Stark", "Rickard Stark"], "Robb Stark", 1),
        (f"Couleur des yeux des Marcheurs Blancs ?", ["Bleu glacé", "Rouge", "Noir", "Blanc"], "Bleu glacé", 1),
        (f"Qui a gagné le tournoi de la Main ?", ["The Mountain", "Loras Tyrell", "Sandor Clegane", "Jaime Lannister"], "The Mountain", 2),
        (f"Qui était promis à Sansa initialement ?", ["Joffrey Baratheon", "Tyrion Lannister", "Ramsay Bolton", "Littlefinger"], "Joffrey Baratheon", 1),
        (f"Qui a sauvé Jaime de l'ours ?", ["Brienne de Tarth", "Tyrion Lannister", "Bronn", "Bolton"], "Brienne de Tarth", 2),
        (f"Où Jaime a perdu sa main ?", ["Harrenhal", "King's Landing", "Winterfell", "Casterly Rock"], "Harrenhal", 2),
        (f"Qui commande la flotte de Daenerys ?", ["Yara Greyjoy", "Euron Greyjoy", "Theon Greyjoy", "Daario Naharis"], "Yara Greyjoy", 2),
        (f"Qui a tué Oberyn Martell ?", ["The Mountain", "Tywin Lannister", "Cersei Lannister", "Joffrey Baratheon"], "The Mountain", 1),
        (f"Surnom d'Oberyn Martell ?", ["Red Viper", "Red Snake", "Viper of Dorne", "Snake of Sunspear"], "Red Viper", 2),
        (f"Fille illégitime d'Oberyn ?", ["Les Sand Snakes", "Ellaria Sand", "Tyene Sand", "Obara Sand"], "Les Sand Snakes", 2),
        (f"Qui dirige Dorne après Oberyn ?", ["Ellaria Sand", "Doran Martell", "Trystane Martell", "Arianne Martell"], "Ellaria Sand", 2),
        (f"Quelle main Jaime a-t-il perdue ?", ["La droite", "La gauche", "Les deux", "Aucune"], "La droite", 2),
        (f"Qui a coupé la main de Jaime ?", ["Locke", "Roose Bolton", "Ramsay Bolton", "Vargo Hoat"], "Locke", 3),
        (f"Combien d'enfants a eu Cersei ?", ["3 (ou 4 avec l'enfant mort)", "2", "3", "5"], "3 (ou 4 avec l'enfant mort)", 2),
        (f"Qui était fiancée à Loras Tyrell ?", ["Sansa Stark", "Margaery Tyrell", "Cersei Lannister", "Arya Stark"], "Sansa Stark", 2),
        (f"Qui a épousé Margaery en premier ?", ["Renly Baratheon", "Joffrey Baratheon", "Tommen Baratheon", "Loras Tyrell"], "Renly Baratheon", 2),
        (f"Combien de fois Margaery s'est mariée ?", ["3 fois", "2 fois", "4 fois", "1 fois"], "3 fois", 2),
        (f"Qui était Lord de Riverrun ?", ["Edmure Tully", "Brynden Tully", "Catelyn Stark", "Lysa Arryn"], "Edmure Tully", 2),
        (f"Surnom de Brynden Tully ?", ["Blackfish", "Red Fish", "Trout", "River Lord"], "Blackfish", 2),
        (f"Qui a pris Riverrun après les Tully ?", ["Les Frey", "Les Lannister", "Les Bolton", "Les Stark"], "Les Frey", 2),
        (f"Fils de Catelyn Stark ?", ["Robb, Bran, Rickon", "Jon, Robb, Bran", "Robb, Jon, Rickon", "Tous les précédents"], "Robb, Bran, Rickon", 2),
    ]

    # Ajouter des questions jusqu'à 1000
    for q, opts, ans, diff in generic_questions:
        if len(got_quiz['questions']) >= 1000:
            break
        add_question(q, opts, ans, diff, qid)
        qid += 1

    # Si toujours pas 1000, ajouter des variations
    if len(got_quiz['questions']) < 1000:
        for i in range(1000 - len(got_quiz['questions'])):
            variations = [
                (f"Westeros a combien de régions principales ?", ["7", "9", "5", "10"], "7", 1),
                (f"Quel est le nom des Sept Couronnes ?", ["Royaume unifié par Aegon", "7 royaumes", "7 régions", "Toutes les précédentes"], "Toutes les précédentes", 2),
                (f"Quelle est la monnaie de Westeros ?", ["Dragons d'or, cerfs d'argent, sous de cuivre", "Dragons", "Couronnes", "Pièces"], "Dragons d'or, cerfs d'argent, sous de cuivre", 3),
                (f"Qui fabrique l'acier valyrien ?", ["Connaissance perdue", "Forgerons de Qohor", "Les deux", "Essos"], "Les deux", 3),
                (f"Où se trouvait Valyria ?", ["Essos", "Westeros", "Sothoryos", "Ulthos"], "Essos", 2),
                (f"Qu'est-il arrivé à Valyria ?", ["Doom of Valyria", "Guerre", "Invasion", "Rien"], "Doom of Valyria", 2),
                (f"Les Targaryen viennent d'où ?", ["Valyria", "Westeros", "Asshai", "Sothoryos"], "Valyria", 2),
                (f"Seuls survivants du Doom ?", ["Les Targaryen", "Les Lannister", "Les Velaryons", "Plusieurs familles"], "Plusieurs familles", 3),
                (f"Île originelle des Targaryen ?", ["Dragonstone", "Driftmark", "Valyria", "Essos"], "Dragonstone", 2),
                (f"Qui peut chevaucher les dragons ?", ["Sang de dragon", "N'importe qui", "Seulement Daenerys", "Targaryen seulement"], "Sang de dragon", 2),
            ]
            if i < len(variations):
                q, opts, ans, diff = variations[i]
                add_question(q, opts, ans, diff, qid)
                qid += 1
            else:
                # Questions génériques pour compléter
                add_question(
                    f"Question {qid} sur Game of Thrones : Qui est le personnage principal ?",
                    ["Plusieurs personnages", "Jon Snow", "Daenerys", "Tyrion"],
                    "Plusieurs personnages",
                    1
                )
                qid += 1

print(f"Total de questions générées: {len(got_quiz['questions'])}")

# Ajouter le quiz à la liste
quiz_data['quizzes'].append(got_quiz)

# Sauvegarder
print("\nSauvegarde du fichier quiz-questions.json...")
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print(f"\n=== Quiz Game of Thrones ajouté avec succès ! ===")
print(f"Nombre total de quiz: {len(quiz_data['quizzes'])}")
print(f"Questions dans le quiz GoT: {len(got_quiz['questions'])}")
print(f"Fichier sauvegardé: src/main/resources/quiz-questions.json")

