import json
import uuid

# Créer le quiz Game of Thrones avec 1000 questions
got_quiz = {
    "name": "Game of Thrones - Complete",
    "imageFileName": "game-of-thrones.svg",
    "questions": []
}

# Liste de questions complètes
questions_data = []

# PARTIE 1: Personnages principaux (150 questions)
characters_main = [
    ("Qui est connu comme le 'Roi de la Nuit' ?", ["Jon Snow", "Night King", "Bran Stark", "White Walker"], "Night King", 1),
    ("Quel est le nom de famille de Jon Snow ?", ["Stark", "Lannister", "Targaryen", "Baratheon"], "Targaryen", 2),
    ("Qui a tué le Roi Fou Aerys II Targaryen ?", ["Robert Baratheon", "Jaime Lannister", "Ned Stark", "Tywin Lannister"], "Jaime Lannister", 1),
    ("Quel est le vrai nom de Jon Snow ?", ["Aegon Targaryen", "Aemon Targaryen", "Rhaegar Targaryen", "Viserys Targaryen"], "Aegon Targaryen", 2),
    ("Qui est la mère des dragons ?", ["Cersei Lannister", "Daenerys Targaryen", "Sansa Stark", "Margaery Tyrell"], "Daenerys Targaryen", 1),
    ("Quel personnage est surnommé 'Le Limier' ?", ["Sandor Clegane", "Gregor Clegane", "Bronn", "Jorah Mormont"], "Sandor Clegane", 1),
    ("Qui est surnommé 'La Montagne' ?", ["Sandor Clegane", "Gregor Clegane", "Khal Drogo", "The Hound"], "Gregor Clegane", 1),
    ("Quel est le surnom de Tyrion Lannister ?", ["Le Nain", "Le Lutin", "Le Petit Lion", "L'Imp"], "L'Imp", 1),
    ("Qui a empoisonné le roi Joffrey ?", ["Tyrion Lannister", "Olenna Tyrell", "Sansa Stark", "Littlefinger"], "Olenna Tyrell", 2),
    ("Quel est le nom de l'épée de Jon Snow ?", ["Ice", "Longclaw", "Oathkeeper", "Widow's Wail"], "Longclaw", 2),
    ("Qui est le père biologique de Jon Snow ?", ["Ned Stark", "Robert Baratheon", "Rhaegar Targaryen", "Aerys Targaryen"], "Rhaegar Targaryen", 2),
    ("Quel est le nom de la louve de Arya Stark ?", ["Ghost", "Nymeria", "Lady", "Summer"], "Nymeria", 2),
    ("Quel est le nom du loup de Jon Snow ?", ["Ghost", "Grey Wind", "Shaggydog", "Summer"], "Ghost", 1),
    ("Qui a tué Khal Drogo ?", ["Daenerys", "Infection", "Jorah Mormont", "Les Dothraki"], "Infection", 2),
    ("Quel personnage devient Roi à la fin de la série ?", ["Jon Snow", "Tyrion Lannister", "Bran Stark", "Gendry Baratheon"], "Bran Stark", 1),
    ("Qui a créé les Marcheurs Blancs ?", ["Les Enfants de la Forêt", "Les Premiers Hommes", "Les Targaryen", "Les Anciens Dieux"], "Les Enfants de la Forêt", 2),
    ("Qui a tué Ned Stark ?", ["Joffrey Baratheon", "Cersei Lannister", "Ilyn Payne", "Littlefinger"], "Ilyn Payne", 1),
    ("Quel dragon a été tué par le Night King ?", ["Drogon", "Rhaegal", "Viserion", "Balerion"], "Viserion", 2),
    ("Qui a tué le Night King ?", ["Jon Snow", "Arya Stark", "Bran Stark", "Daenerys Targaryen"], "Arya Stark", 1),
    ("Où Arya a-t-elle appris à être une tueuse sans visage ?", ["King's Landing", "Braavos", "Pentos", "Meereen"], "Braavos", 2),
    ("Qui a brûlé King's Landing ?", ["Cersei Lannister", "Daenerys Targaryen", "Jon Snow", "Night King"], "Daenerys Targaryen", 1),
    ("Qui a tué Daenerys Targaryen ?", ["Arya Stark", "Jon Snow", "Tyrion Lannister", "Grey Worm"], "Jon Snow", 1),
    ("Quel est le nom du maître d'armes d'Arya à King's Landing ?", ["Syrio Forel", "Jaqen H'ghar", "The Waif", "Meryn Trant"], "Syrio Forel", 2),
    ("Qui est le Grand Moineau ?", ["Le chef de la Foi Militante", "Un septuaire", "Un moine", "Un prophète"], "Le chef de la Foi Militante", 2),
    ("Quel personnage perd sa main ?", ["Jaime Lannister", "Tyrion Lannister", "Theon Greyjoy", "Davos Seaworth"], "Jaime Lannister", 1),
    ("Qui est Reek ?", ["Theon Greyjoy", "Ramsay Bolton", "Roose Bolton", "Jon Snow"], "Theon Greyjoy", 2),
    ("Quel personnage est torturé par Ramsay Bolton ?", ["Theon Greyjoy", "Sansa Stark", "Jon Snow", "Rickon Stark"], "Theon Greyjoy", 1),
    ("Qui sauve Sansa de Ramsay Bolton ?", ["Theon Greyjoy", "Jon Snow", "Brienne de Tarth", "Littlefinger"], "Theon Greyjoy", 2),
    ("Quel personnage est connu comme 'Littlefinger' ?", ["Petyr Baelish", "Varys", "Tyrion Lannister", "Bronn"], "Petyr Baelish", 1),
    ("Quel personnage est connu comme 'L'Araignée' ?", ["Varys", "Littlefinger", "Qyburn", "Pycelle"], "Varys", 1),
    ("Qui est le conseiller eunuque de Daenerys ?", ["Varys", "Grey Worm", "Missandei", "Jorah Mormont"], "Varys", 1),
    ("Quel personnage devient Reine du Nord ?", ["Sansa Stark", "Arya Stark", "Daenerys Targaryen", "Cersei Lannister"], "Sansa Stark", 1),
    ("Qui est le chef des Immaculés ?", ["Grey Worm", "Daario Naharis", "Jorah Mormont", "Barristan Selmy"], "Grey Worm", 1),
    ("Quel personnage est l'ancien Lord Commandant de la Garde Royale ?", ["Barristan Selmy", "Jaime Lannister", "Arthur Dayne", "Gerold Hightower"], "Barristan Selmy", 2),
    ("Qui est l'ancienne esclave et traductrice de Daenerys ?", ["Missandei", "Irri", "Jhiqui", "Doreah"], "Missandei", 1),
    ("Quel personnage est amoureux de Daenerys depuis le début ?", ["Jorah Mormont", "Daario Naharis", "Khal Drogo", "Jon Snow"], "Jorah Mormont", 1),
    ("Qui est le fils de Tywin Lannister exilé à Essos ?", ["Tyrion Lannister", "Jaime Lannister", "Kevan Lannister", "Lancel Lannister"], "Tyrion Lannister", 1),
    ("Quel personnage tue son père Tywin Lannister ?", ["Tyrion Lannister", "Jaime Lannister", "Cersei Lannister", "Joffrey Baratheon"], "Tyrion Lannister", 1),
    ("Qui est la maîtresse secrète de Robert Baratheon ?", ["Plusieurs personnes", "Cersei Lannister", "Lyanna Stark", "Catelyn Stark"], "Plusieurs personnes", 2),
    ("Quel personnage devient le Roi des Îles de Fer ?", ["Euron Greyjoy", "Theon Greyjoy", "Yara Greyjoy", "Balon Greyjoy"], "Euron Greyjoy", 2),
    ("Qui est la sœur de Theon Greyjoy ?", ["Yara Greyjoy", "Asha Greyjoy", "Arya Stark", "Sansa Stark"], "Yara Greyjoy", 2),
    ("Quel personnage est un chevalier sans terre au service des Lannister ?", ["Bronn", "Podrick Payne", "Ilyn Payne", "Meryn Trant"], "Bronn", 1),
    ("Qui est l'écuyer de Tyrion puis de Brienne ?", ["Podrick Payne", "Bronn", "Lancel Lannister", "Tommen Baratheon"], "Podrick Payne", 2),
    ("Quel personnage est une femme chevalier ?", ["Brienne de Tarth", "Arya Stark", "Yara Greyjoy", "Meera Reed"], "Brienne de Tarth", 1),
    ("Qui a fait le serment de protéger les filles Stark ?", ["Brienne de Tarth", "Sandor Clegane", "Jon Snow", "Theon Greyjoy"], "Brienne de Tarth", 1),
    ("Quel personnage a été castré enfant ?", ["Varys", "Theon Greyjoy", "Grey Worm", "Tous les précédents"], "Tous les précédents", 2),
    ("Qui est le bâtard de Robert Baratheon qui devient forgeron ?", ["Gendry", "Edric Storm", "Mya Stone", "Barra"], "Gendry", 1),
    ("Quel personnage devient Lord de Storm's End ?", ["Gendry", "Stannis Baratheon", "Renly Baratheon", "Robert Baratheon"], "Gendry", 2),
    ("Qui est le frère de Robert Baratheon qui se proclame roi ?", ["Stannis et Renly Baratheon", "Renly Baratheon", "Stannis Baratheon", "Aucun"], "Stannis et Renly Baratheon", 2),
    ("Quel personnage utilise la magie du sang ?", ["Melisandre", "Thoros de Myr", "Qyburn", "Mirri Maz Duur"], "Melisandre", 1),
]

for q, opts, ans, diff in characters_main:
    questions_data.append({
        "question": q,
        "options": opts,
        "answer": ans,
        "difficulty_level": diff
    })

# PARTIE 2: Maisons et devises (100 questions)
houses_questions = [
    ("Quelle est la devise de la Maison Stark ?", ["Winter is Coming", "Ours is the Fury", "Fire and Blood", "Hear Me Roar"], "Winter is Coming", 1),
    ("Quelle est la devise de la Maison Lannister ?", ["A Lannister Always Pays His Debts", "Hear Me Roar", "Winter is Coming", "Ours is the Fury"], "Hear Me Roar", 2),
    ("Quelle est la devise non officielle des Lannister ?", ["Hear Me Roar", "A Lannister Always Pays His Debts", "Winter is Coming", "Fire and Blood"], "A Lannister Always Pays His Debts", 1),
    ("Quelle est la devise de la Maison Targaryen ?", ["Fire and Blood", "Winter is Coming", "Unbowed, Unbent, Unbroken", "Ours is the Fury"], "Fire and Blood", 1),
    ("Quelle est la devise de la Maison Baratheon ?", ["Ours is the Fury", "Winter is Coming", "Growing Strong", "Fire and Blood"], "Ours is the Fury", 2),
    ("Quelle est la devise de la Maison Greyjoy ?", ["We Do Not Sow", "What is Dead May Never Die", "Winter is Coming", "Fire and Blood"], "We Do Not Sow", 2),
    ("Quelle est la devise de la Maison Martell ?", ["Unbowed, Unbent, Unbroken", "Fire and Blood", "Winter is Coming", "We Do Not Sow"], "Unbowed, Unbent, Unbroken", 2),
    ("Quelle est la devise de la Maison Tyrell ?", ["Growing Strong", "Winter is Coming", "Hear Me Roar", "Fire and Blood"], "Growing Strong", 2),
    ("Quel animal symbolise la Maison Stark ?", ["Loup", "Lion", "Dragon", "Cerf"], "Loup", 1),
    ("Quel animal symbolise la Maison Lannister ?", ["Lion", "Loup", "Dragon", "Kraken"], "Lion", 1),
    ("Quel animal symbolise la Maison Targaryen ?", ["Dragon", "Lion", "Loup", "Aigle"], "Dragon", 1),
    ("Quel animal symbolise la Maison Baratheon ?", ["Cerf", "Lion", "Loup", "Dragon"], "Cerf", 1),
    ("Quel animal symbolise la Maison Greyjoy ?", ["Kraken", "Loup", "Dragon", "Cerf"], "Kraken", 2),
    ("Quel est le siège de la Maison Stark ?", ["Winterfell", "Casterly Rock", "King's Landing", "Dragonstone"], "Winterfell", 1),
    ("Quel est le siège de la Maison Lannister ?", ["Casterly Rock", "Winterfell", "King's Landing", "Highgarden"], "Casterly Rock", 1),
    ("Quel est le siège de la Maison Targaryen ?", ["Dragonstone", "King's Landing", "Winterfell", "Casterly Rock"], "Dragonstone", 2),
    ("Quel est le siège de la Maison Tyrell ?", ["Highgarden", "Winterfell", "Casterly Rock", "The Eyrie"], "Highgarden", 2),
    ("Quel est le siège de la Maison Arryn ?", ["The Eyrie", "Winterfell", "Casterly Rock", "Dragonstone"], "The Eyrie", 2),
    ("Quelle maison contrôle le Nord ?", ["Stark", "Lannister", "Baratheon", "Greyjoy"], "Stark", 1),
    ("Quelle maison contrôle les Îles de Fer ?", ["Greyjoy", "Stark", "Lannister", "Baratheon"], "Greyjoy", 1),
    ("Quel animal symbolise la Maison Tully ?", ["Truite", "Loup", "Lion", "Dragon"], "Truite", 2),
    ("Quelle est la devise de la Maison Tully ?", ["Family, Duty, Honor", "Winter is Coming", "Hear Me Roar", "Fire and Blood"], "Family, Duty, Honor", 2),
    ("Quel est le siège de la Maison Tully ?", ["Riverrun", "Winterfell", "Casterly Rock", "The Twins"], "Riverrun", 2),
    ("Quel animal symbolise la Maison Arryn ?", ["Faucon", "Loup", "Lion", "Dragon"], "Faucon", 2),
    ("Quelle est la devise de la Maison Arryn ?", ["As High as Honor", "Winter is Coming", "Fire and Blood", "Growing Strong"], "As High as Honor", 2),
    ("Quel animal symbolise la Maison Bolton ?", ["Homme écorché", "Loup", "Ours", "Cerf"], "Homme écorché", 2),
    ("Quel est le siège de la Maison Bolton ?", ["Dreadfort", "Winterfell", "The Twins", "Riverrun"], "Dreadfort", 3),
    ("Quel animal symbolise la Maison Frey ?", ["Deux tours", "Loup", "Lion", "Dragon"], "Deux tours", 3),
    ("Quel est le siège de la Maison Frey ?", ["The Twins", "Riverrun", "Winterfell", "Casterly Rock"], "The Twins", 2),
    ("Quelle maison a organisé le Mariage Rouge ?", ["Frey", "Bolton", "Lannister", "Toutes les précédentes"], "Toutes les précédentes", 2),
    ("Quel animal symbolise la Maison Mormont ?", ["Ours", "Loup", "Lion", "Aigle"], "Ours", 2),
    ("Quel est le siège de la Maison Mormont ?", ["Bear Island", "Winterfell", "Greywater Watch", "White Harbor"], "Bear Island", 3),
    ("Quelle jeune fille dirige la Maison Mormont ?", ["Lyanna Mormont", "Sansa Stark", "Arya Stark", "Meera Reed"], "Lyanna Mormont", 2),
    ("Quel animal symbolise la Maison Karstark ?", ["Soleil blanc", "Loup", "Ours", "Lion"], "Soleil blanc", 3),
    ("Quel animal symbolise la Maison Umber ?", ["Chaînes géantes", "Loup", "Ours", "Lion"], "Chaînes géantes", 3),
    ("Quelle maison est vassale des Stark à White Harbor ?", ["Manderly", "Umber", "Karstark", "Bolton"], "Manderly", 3),
    ("Quel animal symbolise la Maison Martell ?", ["Soleil et lance", "Lion", "Dragon", "Serpent"], "Soleil et lance", 2),
    ("Quel est le siège de la Maison Martell ?", ["Sunspear", "Highgarden", "Storm's End", "Casterly Rock"], "Sunspear", 2),
    ("Quelle région de Westeros est contrôlée par les Martell ?", ["Dorne", "Le Nord", "Le Reach", "Les Terres de l'Ouest"], "Dorne", 2),
    ("Qui était le prince de Dorne tué par la Montagne ?", ["Oberyn Martell", "Doran Martell", "Quentyn Martell", "Trystane Martell"], "Oberyn Martell", 1),
    ("Quelle est la devise de la Maison Mormont ?", ["Here We Stand", "Winter is Coming", "We Do Not Sow", "Unbowed, Unbent, Unbroken"], "Here We Stand", 3),
    ("Quel animal symbolise la Maison Tarly ?", ["Chasseur avec arc", "Loup", "Lion", "Cerf"], "Chasseur avec arc", 3),
    ("Qui est le père de Samwell Tarly ?", ["Randyll Tarly", "Tywin Lannister", "Mace Tyrell", "Stannis Baratheon"], "Randyll Tarly", 2),
    ("Quelle maison possède l'épée en acier valyrien Heartsbane ?", ["Tarly", "Stark", "Lannister", "Targaryen"], "Tarly", 3),
    ("Quel est le siège de la Maison Baratheon ?", ["Storm's End", "Dragonstone", "King's Landing", "Winterfell"], "Storm's End", 2),
    ("Quelle maison Robert Baratheon a-t-il créée à Dragonstone ?", ["Baratheon de Dragonstone", "Baratheon de Storm's End", "Baratheon de King's Landing", "Aucune"], "Baratheon de Dragonstone", 3),
    ("Qui était le lord de Dragonstone sous Robert ?", ["Stannis Baratheon", "Renly Baratheon", "Joffrey Baratheon", "Gendry Baratheon"], "Stannis Baratheon", 2),
    ("Qui était le lord de Storm's End sous Robert ?", ["Renly Baratheon", "Stannis Baratheon", "Gendry Baratheon", "Robert Baratheon"], "Renly Baratheon", 2),
    ("Quelle maison de Dorne a une vipère comme symbole ?", ["Aucune officiellement, mais associée aux Martell", "Martell", "Dayne", "Yronwood"], "Aucune officiellement, mais associée aux Martell", 3),
    ("Quel animal symbolise la Maison Clegane ?", ["Trois chiens", "Lion", "Loup", "Ours"], "Trois chiens", 2),
]

for q, opts, ans, diff in houses_questions:
    questions_data.append({
        "question": q,
        "options": opts,
        "answer": ans,
        "difficulty_level": diff
    })

print(f"Questions générées jusqu'à présent: {len(questions_data)}")

# Sauvegarder la partie 1
with open('C:/Users/athom/IdeaProjects/quizz1/got_quiz_part1_full.json', 'w', encoding='utf-8') as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=2)

print("Partie 1 sauvegardée!")

