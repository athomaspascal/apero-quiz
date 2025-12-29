import json
import uuid

# Générer le quiz Game of Thrones
got_quiz = {
    "name": "Game of Thrones - Complete",
    "imageFileName": "game-of-thrones.svg",
    "questions": []
}

# Questions sur les personnages principaux
characters_questions = [
    {
        "question": "Qui est connu comme le 'Roi de la Nuit' ?",
        "options": ["Jon Snow", "Night King", "Bran Stark", "White Walker"],
        "answer": "Night King",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le nom de famille de Jon Snow ?",
        "options": ["Stark", "Lannister", "Targaryen", "Baratheon"],
        "answer": "Targaryen",
        "difficulty_level": 2
    },
    {
        "question": "Qui a tué le Roi Fou Aerys II Targaryen ?",
        "options": ["Robert Baratheon", "Jaime Lannister", "Ned Stark", "Tywin Lannister"],
        "answer": "Jaime Lannister",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le vrai nom de Jon Snow ?",
        "options": ["Aegon Targaryen", "Aemon Targaryen", "Rhaegar Targaryen", "Viserys Targaryen"],
        "answer": "Aegon Targaryen",
        "difficulty_level": 2
    },
    {
        "question": "Qui est la mère des dragons ?",
        "options": ["Cersei Lannister", "Daenerys Targaryen", "Sansa Stark", "Margaery Tyrell"],
        "answer": "Daenerys Targaryen",
        "difficulty_level": 1
    },
    {
        "question": "Quel personnage est surnommé 'Le Limier' ?",
        "options": ["Sandor Clegane", "Gregor Clegane", "Bronn", "Jorah Mormont"],
        "answer": "Sandor Clegane",
        "difficulty_level": 1
    },
    {
        "question": "Qui est surnommé 'La Montagne' ?",
        "options": ["Sandor Clegane", "Gregor Clegane", "Khal Drogo", "The Hound"],
        "answer": "Gregor Clegane",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le surnom de Tyrion Lannister ?",
        "options": ["Le Nain", "Le Lutin", "Le Petit Lion", "L'Imp"],
        "answer": "L'Imp",
        "difficulty_level": 1
    },
    {
        "question": "Qui a empoisonné le roi Joffrey ?",
        "options": ["Tyrion Lannister", "Olenna Tyrell", "Sansa Stark", "Littlefinger"],
        "answer": "Olenna Tyrell",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de l'épée de Jon Snow ?",
        "options": ["Ice", "Longclaw", "Oathkeeper", "Widow's Wail"],
        "answer": "Longclaw",
        "difficulty_level": 2
    },
    {
        "question": "Qui est le père biologique de Jon Snow ?",
        "options": ["Ned Stark", "Robert Baratheon", "Rhaegar Targaryen", "Aerys Targaryen"],
        "answer": "Rhaegar Targaryen",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de la louve de Arya Stark ?",
        "options": ["Ghost", "Nymeria", "Lady", "Summer"],
        "answer": "Nymeria",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom du loup de Jon Snow ?",
        "options": ["Ghost", "Grey Wind", "Shaggydog", "Summer"],
        "answer": "Ghost",
        "difficulty_level": 1
    },
    {
        "question": "Qui a tué Khal Drogo ?",
        "options": ["Daenerys", "Infection", "Jorah Mormont", "Les Dothraki"],
        "answer": "Infection",
        "difficulty_level": 2
    },
    {
        "question": "Quel personnage devient Roi à la fin de la série ?",
        "options": ["Jon Snow", "Tyrion Lannister", "Bran Stark", "Gendry Baratheon"],
        "answer": "Bran Stark",
        "difficulty_level": 1
    },
    {
        "question": "Qui a créé les Marcheurs Blancs ?",
        "options": ["Les Enfants de la Forêt", "Les Premiers Hommes", "Les Targaryen", "Les Anciens Dieux"],
        "answer": "Les Enfants de la Forêt",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de la Main du Roi sous Robert Baratheon ?",
        "options": ["Tywin Lannister", "Ned Stark", "Jon Arryn", "Tyrion Lannister"],
        "answer": "Jon Arryn",
        "difficulty_level": 2
    },
    {
        "question": "Qui a tué Ned Stark ?",
        "options": ["Joffrey Baratheon", "Cersei Lannister", "Ilyn Payne", "Littlefinger"],
        "answer": "Ilyn Payne",
        "difficulty_level": 1
    },
    {
        "question": "Quel dragon a été tué par le Night King ?",
        "options": ["Drogon", "Rhaegal", "Viserion", "Balerion"],
        "answer": "Viserion",
        "difficulty_level": 2
    },
    {
        "question": "Qui a tué le Night King ?",
        "options": ["Jon Snow", "Arya Stark", "Bran Stark", "Daenerys Targaryen"],
        "answer": "Arya Stark",
        "difficulty_level": 1
    },
    {
        "question": "Quel personnage peut changer de visage ?",
        "options": ["Arya Stark", "Jaqen H'ghar", "The Waif", "Tous les précédents"],
        "answer": "Tous les précédents",
        "difficulty_level": 2
    },
    {
        "question": "Où Arya a-t-elle appris à être une tueuse sans visage ?",
        "options": ["King's Landing", "Braavos", "Pentos", "Meereen"],
        "answer": "Braavos",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de la religion du Dieu Noyé ?",
        "options": ["Les Sept", "Le Dieu Noyé", "R'hllor", "Les Anciens Dieux"],
        "answer": "Le Dieu Noyé",
        "difficulty_level": 2
    },
    {
        "question": "Qui a brûlé King's Landing ?",
        "options": ["Cersei Lannister", "Daenerys Targaryen", "Jon Snow", "Night King"],
        "answer": "Daenerys Targaryen",
        "difficulty_level": 1
    },
    {
        "question": "Qui a tué Daenerys Targaryen ?",
        "options": ["Arya Stark", "Jon Snow", "Tyrion Lannister", "Grey Worm"],
        "answer": "Jon Snow",
        "difficulty_level": 1
    },
]

# Questions sur les maisons
houses_questions = [
    {
        "question": "Quelle est la devise de la Maison Stark ?",
        "options": ["Winter is Coming", "Ours is the Fury", "Fire and Blood", "Hear Me Roar"],
        "answer": "Winter is Coming",
        "difficulty_level": 1
    },
    {
        "question": "Quelle est la devise de la Maison Lannister ?",
        "options": ["A Lannister Always Pays His Debts", "Hear Me Roar", "Winter is Coming", "Ours is the Fury"],
        "answer": "Hear Me Roar",
        "difficulty_level": 2
    },
    {
        "question": "Quelle est la devise non officielle des Lannister ?",
        "options": ["Hear Me Roar", "A Lannister Always Pays His Debts", "Winter is Coming", "Fire and Blood"],
        "answer": "A Lannister Always Pays His Debts",
        "difficulty_level": 1
    },
    {
        "question": "Quelle est la devise de la Maison Targaryen ?",
        "options": ["Fire and Blood", "Winter is Coming", "Unbowed, Unbent, Unbroken", "Ours is the Fury"],
        "answer": "Fire and Blood",
        "difficulty_level": 1
    },
    {
        "question": "Quelle est la devise de la Maison Baratheon ?",
        "options": ["Ours is the Fury", "Winter is Coming", "Growing Strong", "Fire and Blood"],
        "answer": "Ours is the Fury",
        "difficulty_level": 2
    },
    {
        "question": "Quelle est la devise de la Maison Greyjoy ?",
        "options": ["We Do Not Sow", "What is Dead May Never Die", "Winter is Coming", "Fire and Blood"],
        "answer": "We Do Not Sow",
        "difficulty_level": 2
    },
    {
        "question": "Quelle est la devise de la Maison Martell ?",
        "options": ["Unbowed, Unbent, Unbroken", "Fire and Blood", "Winter is Coming", "We Do Not Sow"],
        "answer": "Unbowed, Unbent, Unbroken",
        "difficulty_level": 2
    },
    {
        "question": "Quelle est la devise de la Maison Tyrell ?",
        "options": ["Growing Strong", "Winter is Coming", "Hear Me Roar", "Fire and Blood"],
        "answer": "Growing Strong",
        "difficulty_level": 2
    },
    {
        "question": "Quel animal symbolise la Maison Stark ?",
        "options": ["Loup", "Lion", "Dragon", "Cerf"],
        "answer": "Loup",
        "difficulty_level": 1
    },
    {
        "question": "Quel animal symbolise la Maison Lannister ?",
        "options": ["Lion", "Loup", "Dragon", "Kraken"],
        "answer": "Lion",
        "difficulty_level": 1
    },
    {
        "question": "Quel animal symbolise la Maison Targaryen ?",
        "options": ["Dragon", "Lion", "Loup", "Aigle"],
        "answer": "Dragon",
        "difficulty_level": 1
    },
    {
        "question": "Quel animal symbolise la Maison Baratheon ?",
        "options": ["Cerf", "Lion", "Loup", "Dragon"],
        "answer": "Cerf",
        "difficulty_level": 1
    },
    {
        "question": "Quel animal symbolise la Maison Greyjoy ?",
        "options": ["Kraken", "Loup", "Dragon", "Cerf"],
        "answer": "Kraken",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le siège de la Maison Stark ?",
        "options": ["Winterfell", "Casterly Rock", "King's Landing", "Dragonstone"],
        "answer": "Winterfell",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le siège de la Maison Lannister ?",
        "options": ["Casterly Rock", "Winterfell", "King's Landing", "Highgarden"],
        "answer": "Casterly Rock",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le siège de la Maison Targaryen ?",
        "options": ["Dragonstone", "King's Landing", "Winterfell", "Casterly Rock"],
        "answer": "Dragonstone",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le siège de la Maison Tyrell ?",
        "options": ["Highgarden", "Winterfell", "Casterly Rock", "The Eyrie"],
        "answer": "Highgarden",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le siège de la Maison Arryn ?",
        "options": ["The Eyrie", "Winterfell", "Casterly Rock", "Dragonstone"],
        "answer": "The Eyrie",
        "difficulty_level": 2
    },
    {
        "question": "Quelle maison contrôle le Nord ?",
        "options": ["Stark", "Lannister", "Baratheon", "Greyjoy"],
        "answer": "Stark",
        "difficulty_level": 1
    },
    {
        "question": "Quelle maison contrôle les Îles de Fer ?",
        "options": ["Greyjoy", "Stark", "Lannister", "Baratheon"],
        "answer": "Greyjoy",
        "difficulty_level": 1
    },
]

# Questions sur les lieux
locations_questions = [
    {
        "question": "Quelle ville est la capitale des Sept Couronnes ?",
        "options": ["King's Landing", "Winterfell", "Casterly Rock", "Highgarden"],
        "answer": "King's Landing",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le nom du mur qui protège le royaume des Marcheurs Blancs ?",
        "options": ["The Wall", "The Great Wall", "The Ice Wall", "The Northern Wall"],
        "answer": "The Wall",
        "difficulty_level": 1
    },
    {
        "question": "Où se trouve le Trône de Fer ?",
        "options": ["King's Landing", "Winterfell", "Dragonstone", "Casterly Rock"],
        "answer": "King's Landing",
        "difficulty_level": 1
    },
    {
        "question": "Dans quelle ville Arya apprend-elle à être une tueuse sans visage ?",
        "options": ["Braavos", "Pentos", "Meereen", "Volantis"],
        "answer": "Braavos",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom du port libre où Daenerys libère les esclaves ?",
        "options": ["Meereen", "Astapor", "Yunkai", "Tous les précédents"],
        "answer": "Tous les précédents",
        "difficulty_level": 2
    },
    {
        "question": "Où se trouve le château de Winterfell ?",
        "options": ["Le Nord", "Le Sud", "L'Est", "L'Ouest"],
        "answer": "Le Nord",
        "difficulty_level": 1
    },
    {
        "question": "Quel est le nom de la mer entre Westeros et Essos ?",
        "options": ["Narrow Sea", "Sunset Sea", "Shivering Sea", "Jade Sea"],
        "answer": "Narrow Sea",
        "difficulty_level": 2
    },
    {
        "question": "Dans quelle ville Daenerys épouse-t-elle Khal Drogo ?",
        "options": ["Pentos", "Meereen", "Braavos", "Volantis"],
        "answer": "Pentos",
        "difficulty_level": 2
    },
    {
        "question": "Où se déroule le mariage rouge ?",
        "options": ["The Twins", "Winterfell", "King's Landing", "Casterly Rock"],
        "answer": "The Twins",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom du désert en Essos ?",
        "options": ["Red Waste", "Dothraki Sea", "Shadow Lands", "Grey Waste"],
        "answer": "Red Waste",
        "difficulty_level": 3
    },
]

# Questions sur les événements
events_questions = [
    {
        "question": "Quel événement a déclenché la chute de la dynastie Targaryen ?",
        "options": ["Robert's Rebellion", "War of the Five Kings", "Dance of Dragons", "Blackfyre Rebellion"],
        "answer": "Robert's Rebellion",
        "difficulty_level": 2
    },
    {
        "question": "Quel événement est connu sous le nom de 'Red Wedding' ?",
        "options": ["Le massacre de la famille Stark aux Twins", "Le mariage de Joffrey", "Le mariage de Sansa", "La mort de Ned Stark"],
        "answer": "Le massacre de la famille Stark aux Twins",
        "difficulty_level": 1
    },
    {
        "question": "Quel événement est connu sous le nom de 'Purple Wedding' ?",
        "options": ["Le mariage et la mort de Joffrey", "Le Red Wedding", "Le mariage de Sansa", "Le mariage de Margaery"],
        "answer": "Le mariage et la mort de Joffrey",
        "difficulty_level": 2
    },
    {
        "question": "Qui a gagné la Bataille des Bâtards ?",
        "options": ["Jon Snow", "Ramsay Bolton", "Stannis Baratheon", "Roose Bolton"],
        "answer": "Jon Snow",
        "difficulty_level": 1
    },
    {
        "question": "Quelle bataille a eu lieu à Winterfell contre les Marcheurs Blancs ?",
        "options": ["Battle of Winterfell", "Battle of the Bastards", "Battle of the Trident", "Battle of Blackwater"],
        "answer": "Battle of Winterfell",
        "difficulty_level": 1
    },
    {
        "question": "Qui a défendu King's Landing lors de la Bataille de Blackwater ?",
        "options": ["Tyrion Lannister", "Joffrey Baratheon", "Tywin Lannister", "Jaime Lannister"],
        "answer": "Tyrion Lannister",
        "difficulty_level": 2
    },
    {
        "question": "Quel événement a causé la mort de Robb Stark ?",
        "options": ["Red Wedding", "Battle of the Bastards", "Purple Wedding", "Battle of Winterfell"],
        "answer": "Red Wedding",
        "difficulty_level": 1
    },
    {
        "question": "Qui a organisé le Red Wedding ?",
        "options": ["Walder Frey et Roose Bolton", "Tywin Lannister", "Cersei Lannister", "Littlefinger"],
        "answer": "Walder Frey et Roose Bolton",
        "difficulty_level": 2
    },
    {
        "question": "Quelle bataille a vu la défaite de Stannis Baratheon ?",
        "options": ["Battle of Winterfell (contre Bolton)", "Battle of Blackwater", "Battle of Castle Black", "Battle of the Bastards"],
        "answer": "Battle of Winterfell (contre Bolton)",
        "difficulty_level": 2
    },
    {
        "question": "Qui a détruit le Grand Septuaire de Baelor ?",
        "options": ["Cersei Lannister", "Daenerys Targaryen", "Jon Snow", "Night King"],
        "answer": "Cersei Lannister",
        "difficulty_level": 1
    },
]

# Questions sur les dragons
dragons_questions = [
    {
        "question": "Quel est le nom du plus grand dragon de Daenerys ?",
        "options": ["Drogon", "Rhaegal", "Viserion", "Balerion"],
        "answer": "Drogon",
        "difficulty_level": 1
    },
    {
        "question": "Combien de dragons Daenerys a-t-elle au début ?",
        "options": ["3", "2", "4", "1"],
        "answer": "3",
        "difficulty_level": 1
    },
    {
        "question": "Quel dragon a été nommé d'après le frère de Daenerys ?",
        "options": ["Viserion", "Rhaegal", "Drogon", "Aucun"],
        "answer": "Viserion",
        "difficulty_level": 2
    },
    {
        "question": "Quel dragon a été nommé d'après Rhaegar Targaryen ?",
        "options": ["Rhaegal", "Viserion", "Drogon", "Balerion"],
        "answer": "Rhaegal",
        "difficulty_level": 2
    },
    {
        "question": "Quel dragon a été nommé d'après Khal Drogo ?",
        "options": ["Drogon", "Rhaegal", "Viserion", "Aucun"],
        "answer": "Drogon",
        "difficulty_level": 2
    },
    {
        "question": "Quel dragon est devenu un dragon de glace ?",
        "options": ["Viserion", "Rhaegal", "Drogon", "Aucun"],
        "answer": "Viserion",
        "difficulty_level": 1
    },
    {
        "question": "Qui a tué Rhaegal ?",
        "options": ["Euron Greyjoy", "Night King", "Qyburn", "Cersei Lannister"],
        "answer": "Euron Greyjoy",
        "difficulty_level": 2
    },
    {
        "question": "Quel dragon a survécu jusqu'à la fin de la série ?",
        "options": ["Drogon", "Rhaegal", "Viserion", "Aucun"],
        "answer": "Drogon",
        "difficulty_level": 1
    },
    {
        "question": "Quel était le nom du dragon d'Aegon le Conquérant ?",
        "options": ["Balerion", "Vhagar", "Meraxes", "Drogon"],
        "answer": "Balerion",
        "difficulty_level": 3
    },
    {
        "question": "De quelle couleur est Drogon ?",
        "options": ["Noir et rouge", "Vert et bronze", "Blanc et or", "Bleu et argent"],
        "answer": "Noir et rouge",
        "difficulty_level": 1
    },
]

# Combiner toutes les questions de base
all_base_questions = (
    characters_questions +
    houses_questions +
    locations_questions +
    events_questions +
    dragons_questions
)

print(f"Questions de base générées: {len(all_base_questions)}")

# Ajouter plus de questions pour atteindre 1000
additional_questions = []

# Questions sur les relations familiales
family_questions = [
    {
        "question": "Qui est le père de Joffrey Baratheon ?",
        "options": ["Robert Baratheon", "Jaime Lannister", "Ned Stark", "Tywin Lannister"],
        "answer": "Jaime Lannister",
        "difficulty_level": 2
    },
    {
        "question": "Qui est la mère de Jon Snow ?",
        "options": ["Lyanna Stark", "Catelyn Stark", "Wylla", "Ashara Dayne"],
        "answer": "Lyanna Stark",
        "difficulty_level": 2
    },
    {
        "question": "Qui sont les parents de Daenerys Targaryen ?",
        "options": ["Aerys II et Rhaella Targaryen", "Rhaegar et Elia", "Viserys et Rhaella", "Aegon et Rhaenys"],
        "answer": "Aerys II et Rhaella Targaryen",
        "difficulty_level": 2
    },
    {
        "question": "Combien d'enfants Ned Stark a-t-il ?",
        "options": ["5 (plus Jon Snow)", "6", "4", "7"],
        "answer": "5 (plus Jon Snow)",
        "difficulty_level": 2
    },
    {
        "question": "Qui est le frère jumeau de Jaime Lannister ?",
        "options": ["Cersei Lannister", "Tyrion Lannister", "Tywin Lannister", "Kevan Lannister"],
        "answer": "Cersei Lannister",
        "difficulty_level": 1
    },
    {
        "question": "Qui est le père de Tyrion Lannister ?",
        "options": ["Tywin Lannister", "Aerys Targaryen", "Kevan Lannister", "Tytos Lannister"],
        "answer": "Tywin Lannister",
        "difficulty_level": 1
    },
    {
        "question": "Qui est la sœur de Catelyn Stark ?",
        "options": ["Lysa Arryn", "Lyanna Stark", "Cersei Lannister", "Olenna Tyrell"],
        "answer": "Lysa Arryn",
        "difficulty_level": 2
    },
    {
        "question": "Qui a épousé Sansa Stark en premier ?",
        "options": ["Tyrion Lannister", "Joffrey Baratheon", "Ramsay Bolton", "Littlefinger"],
        "answer": "Tyrion Lannister",
        "difficulty_level": 2
    },
    {
        "question": "Qui est le fils illégitime de Robert Baratheon ?",
        "options": ["Gendry", "Joffrey", "Tommen", "Jon Snow"],
        "answer": "Gendry",
        "difficulty_level": 2
    },
    {
        "question": "Qui est l'oncle de Jon Snow du côté Stark ?",
        "options": ["Benjen Stark", "Robb Stark", "Bran Stark", "Rickon Stark"],
        "answer": "Benjen Stark",
        "difficulty_level": 2
    },
]

additional_questions.extend(family_questions)

# Questions sur les armes et objets
weapons_questions = [
    {
        "question": "De quel matériau est faite l'épée Longclaw ?",
        "options": ["Acier Valyrien", "Acier normal", "Dragonglass", "Or"],
        "answer": "Acier Valyrien",
        "difficulty_level": 2
    },
    {
        "question": "Qu'est-ce que le feu grégeois ?",
        "options": ["Un explosif liquide vert", "Un poison", "Une épée", "Un dragon"],
        "answer": "Un explosif liquide vert",
        "difficulty_level": 2
    },
    {
        "question": "Quel matériau peut tuer les Marcheurs Blancs ?",
        "options": ["Dragonglass et Acier Valyrien", "Acier normal", "Or", "Argent"],
        "answer": "Dragonglass et Acier Valyrien",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de l'épée ancestrale des Stark ?",
        "options": ["Ice", "Longclaw", "Oathkeeper", "Widow's Wail"],
        "answer": "Ice",
        "difficulty_level": 2
    },
    {
        "question": "Qui possède l'épée Oathkeeper ?",
        "options": ["Brienne de Tarth", "Jaime Lannister", "Jon Snow", "Arya Stark"],
        "answer": "Brienne de Tarth",
        "difficulty_level": 2
    },
    {
        "question": "De quoi est fait le Trône de Fer ?",
        "options": ["Épées fondues par le feu de dragon", "Fer forgé", "Acier Valyrien", "Or"],
        "answer": "Épées fondues par le feu de dragon",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de l'épée de Brienne de Tarth ?",
        "options": ["Oathkeeper", "Ice", "Longclaw", "Widow's Wail"],
        "answer": "Oathkeeper",
        "difficulty_level": 2
    },
    {
        "question": "Quel est le nom de l'arme préférée d'Arya ?",
        "options": ["Needle", "Longclaw", "Oathkeeper", "Ice"],
        "answer": "Needle",
        "difficulty_level": 1
    },
    {
        "question": "Qui a donné Needle à Arya ?",
        "options": ["Jon Snow", "Ned Stark", "Robb Stark", "Syrio Forel"],
        "answer": "Jon Snow",
        "difficulty_level": 2
    },
    {
        "question": "Qu'est-ce que le Dragonglass ?",
        "options": ["Obsidienne", "Verre", "Cristal", "Diamant"],
        "answer": "Obsidienne",
        "difficulty_level": 2
    },
]

additional_questions.extend(weapons_questions)

# Questions sur la religion et la magie
religion_magic_questions = [
    {
        "question": "Quel dieu adore Melisandre ?",
        "options": ["R'hllor", "Les Sept", "Les Anciens Dieux", "Le Dieu Noyé"],
        "answer": "R'hllor",
        "difficulty_level": 2
    },
    {
        "question": "Combien de dieux y a-t-il dans la Foi des Sept ?",
        "options": ["7", "1", "3", "9"],
        "answer": "7",
        "difficulty_level": 1
    },
    {
        "question": "Qui est le Dieu de la Lumière ?",
        "options": ["R'hllor", "Les Sept", "Les Anciens Dieux", "Le Dieu Noyé"],
        "answer": "R'hllor",
        "difficulty_level": 2
    },
    {
        "question": "Quel personnage est ressuscité plusieurs fois ?",
        "options": ["Beric Dondarrion", "Jon Snow", "The Mountain", "Tous les précédents"],
        "answer": "Beric Dondarrion",
        "difficulty_level": 2
    },
    {
        "question": "Qui est le dieu de la mort des Faceless Men ?",
        "options": ["The Many-Faced God", "R'hllor", "Les Sept", "Les Anciens Dieux"],
        "answer": "The Many-Faced God",
        "difficulty_level": 2
    },
    {
        "question": "Quelle religion les Greyjoy pratiquent-ils ?",
        "options": ["Le Dieu Noyé", "R'hllor", "Les Sept", "Les Anciens Dieux"],
        "answer": "Le Dieu Noyé",
        "difficulty_level": 2
    },
    {
        "question": "Quelle religion les Stark pratiquent-ils ?",
        "options": ["Les Anciens Dieux", "Les Sept", "R'hllor", "Le Dieu Noyé"],
        "answer": "Les Anciens Dieux",
        "difficulty_level": 2
    },
    {
        "question": "Où les Stark prient-ils ?",
        "options": ["Le Godswood", "Le Septuaire", "Le Temple Rouge", "La Mer"],
        "answer": "Le Godswood",
        "difficulty_level": 2
    },
    {
        "question": "Qui a ressuscité Jon Snow ?",
        "options": ["Melisandre", "Thoros de Myr", "Beric Dondarrion", "Les Anciens Dieux"],
        "answer": "Melisandre",
        "difficulty_level": 1
    },
    {
        "question": "Quel pouvoir Bran possède-t-il ?",
        "options": ["Warging et Greenseeing", "Changement de visage", "Magie du feu", "Ressuscitation"],
        "answer": "Warging et Greenseeing",
        "difficulty_level": 2
    },
]

additional_questions.extend(religion_magic_questions)

print(f"Questions additionnelles générées: {len(additional_questions)}")
print(f"Total actuel: {len(all_base_questions) + len(additional_questions)}")

# Sauvegarder dans un fichier temporaire
with open('C:/Users/athom/IdeaProjects/quizz1/got_quiz_part1.json', 'w', encoding='utf-8') as f:
    json.dump({
        "base_questions": all_base_questions,
        "additional_questions": additional_questions
    }, f, ensure_ascii=False, indent=2)

print("Partie 1 générée avec succès!")

