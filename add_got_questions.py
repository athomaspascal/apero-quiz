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

# Trouver le quiz Game of Thrones
got_quiz = None
if isinstance(data, dict) and 'quizzes' in data:
    quizzes = data['quizzes']
elif isinstance(data, list):
    quizzes = data
else:
    quizzes = []

for quiz in quizzes:
    if isinstance(quiz, dict) and 'Game of Thrones' in quiz.get('name', ''):
        got_quiz = quiz
        break

if not got_quiz:
    print("Quiz Game of Thrones non trouvé!")
    sys.exit(1)

# Obtenir les questions existantes
existing_questions = set()
current_max_id = 0
for q in got_quiz.get('questions', []):
    existing_questions.add(q.get('question', '').lower().strip())
    current_max_id = max(current_max_id, q.get('id', 0))

print(f"Questions existantes: {len(existing_questions)}")
print(f"ID maximum actuel: {current_max_id}")

# Nouvelles questions uniques sur Game of Thrones - EN FRANÇAIS
new_questions = [
    # Maisons et blasons
    {
        "question": "Quelle est la devise de la Maison Stark ?",
        "options": ["Winter is Coming", "Hear Me Roar", "Fire and Blood", "Ours is the Fury"],
        "answer": "Winter is Coming"
    },
    {
        "question": "Quelle est la devise de la Maison Lannister ?",
        "options": ["Hear Me Roar", "Winter is Coming", "Fire and Blood", "Growing Strong"],
        "answer": "Hear Me Roar"
    },
    {
        "question": "Quelle est la devise de la Maison Targaryen ?",
        "options": ["Fire and Blood", "Winter is Coming", "Ours is the Fury", "Unbowed, Unbent, Unbroken"],
        "answer": "Fire and Blood"
    },
    {
        "question": "Quelle est la devise de la Maison Baratheon ?",
        "options": ["Ours is the Fury", "Winter is Coming", "Fire and Blood", "We Do Not Sow"],
        "answer": "Ours is the Fury"
    },
    {
        "question": "Quelle est la devise de la Maison Greyjoy ?",
        "options": ["We Do Not Sow", "Winter is Coming", "What is Dead May Never Die", "Fire and Blood"],
        "answer": "We Do Not Sow"
    },
    {
        "question": "Quelle est la devise de la Maison Tyrell ?",
        "options": ["Growing Strong", "Winter is Coming", "Ours is the Fury", "Family, Duty, Honor"],
        "answer": "Growing Strong"
    },
    {
        "question": "Quelle est la devise de la Maison Tully ?",
        "options": ["Family, Duty, Honor", "Winter is Coming", "We Do Not Sow", "Ours is the Fury"],
        "answer": "Family, Duty, Honor"
    },
    {
        "question": "Quelle est la devise de la Maison Martell ?",
        "options": ["Unbowed, Unbent, Unbroken", "Fire and Blood", "Winter is Coming", "Ours is the Fury"],
        "answer": "Unbowed, Unbent, Unbroken"
    },
    {
        "question": "Quelle est la devise de la Maison Arryn ?",
        "options": ["As High as Honor", "Winter is Coming", "Growing Strong", "Fire and Blood"],
        "answer": "As High as Honor"
    },
    {
        "question": "Quel animal représente la Maison Stark ?",
        "options": ["Un loup-garou", "Un lion", "Un cerf", "Un dragon"],
        "answer": "Un loup-garou"
    },
    {
        "question": "Quel animal représente la Maison Lannister ?",
        "options": ["Un lion", "Un loup", "Un cerf", "Un aigle"],
        "answer": "Un lion"
    },
    {
        "question": "Quel animal représente la Maison Baratheon ?",
        "options": ["Un cerf", "Un lion", "Un loup", "Un kraken"],
        "answer": "Un cerf"
    },
    {
        "question": "Quel animal représente la Maison Targaryen ?",
        "options": ["Un dragon à trois têtes", "Un lion", "Un loup", "Un aigle"],
        "answer": "Un dragon à trois têtes"
    },
    {
        "question": "Quel animal représente la Maison Greyjoy ?",
        "options": ["Un kraken", "Un loup", "Un cerf", "Une rose"],
        "answer": "Un kraken"
    },
    {
        "question": "Quel animal représente la Maison Tyrell ?",
        "options": ["Une rose", "Un lion", "Un cerf", "Un aigle"],
        "answer": "Une rose"
    },

    # Les Dragons
    {
        "question": "Comment s'appelle le plus grand dragon de Daenerys ?",
        "options": ["Drogon", "Rhaegal", "Viserion", "Balerion"],
        "answer": "Drogon"
    },
    {
        "question": "Quel dragon a été transformé en dragon de glace ?",
        "options": ["Viserion", "Drogon", "Rhaegal", "Balerion"],
        "answer": "Viserion"
    },
    {
        "question": "Quel dragon porte le nom du frère de Daenerys ?",
        "options": ["Rhaegal", "Viserion", "Drogon", "Aegon"],
        "answer": "Rhaegal"
    },
    {
        "question": "Qui a tué Rhaegal ?",
        "options": ["Euron Greyjoy", "Le Roi de la Nuit", "Cersei Lannister", "Jon Snow"],
        "answer": "Euron Greyjoy"
    },

    # Lieux et châteaux
    {
        "question": "Quel est le nom du château des Stark ?",
        "options": ["Winterfell", "Casterly Rock", "King's Landing", "The Eyrie"],
        "answer": "Winterfell"
    },
    {
        "question": "Quel est le nom du château des Lannister ?",
        "options": ["Casterly Rock", "Winterfell", "Riverrun", "Highgarden"],
        "answer": "Casterly Rock"
    },
    {
        "question": "Quel est le nom du château des Arryn ?",
        "options": ["The Eyrie", "Winterfell", "Dragonstone", "Storm's End"],
        "answer": "The Eyrie"
    },
    {
        "question": "Quel est le nom du château ancestral des Targaryen ?",
        "options": ["Dragonstone", "King's Landing", "Winterfell", "Casterly Rock"],
        "answer": "Dragonstone"
    },
    {
        "question": "Où se trouve le Trône de Fer ?",
        "options": ["King's Landing", "Winterfell", "Dragonstone", "Casterly Rock"],
        "answer": "King's Landing"
    },
    {
        "question": "Comment s'appelle le grand mur de glace au nord ?",
        "options": ["The Wall", "The Ice Wall", "The Great Wall", "The Northern Wall"],
        "answer": "The Wall"
    },
    {
        "question": "Quel château appartient à la Maison Tyrell ?",
        "options": ["Highgarden", "Winterfell", "Riverrun", "The Twins"],
        "answer": "Highgarden"
    },
    {
        "question": "Quel château appartient à la Maison Tully ?",
        "options": ["Riverrun", "Winterfell", "The Twins", "Harrenhal"],
        "answer": "Riverrun"
    },
    {
        "question": "Quel château appartient à la Maison Frey ?",
        "options": ["The Twins", "Riverrun", "Winterfell", "Harrenhal"],
        "answer": "The Twins"
    },

    # Événements majeurs
    {
        "question": "Comment appelle-t-on le massacre lors du mariage de Robb Stark ?",
        "options": ["The Red Wedding", "The Purple Wedding", "The Black Wedding", "The Bloody Wedding"],
        "answer": "The Red Wedding"
    },
    {
        "question": "Comment appelle-t-on la mort de Joffrey lors de son mariage ?",
        "options": ["The Purple Wedding", "The Red Wedding", "The Green Wedding", "The Poisoned Wedding"],
        "answer": "The Purple Wedding"
    },
    {
        "question": "Qui a tué Joffrey Baratheon ?",
        "options": ["Olenna Tyrell", "Cersei Lannister", "Tyrion Lannister", "Sansa Stark"],
        "answer": "Olenna Tyrell"
    },
    {
        "question": "Qui a organisé le Red Wedding ?",
        "options": ["Walder Frey et Roose Bolton", "Cersei Lannister", "Tywin Lannister seul", "Littlefinger"],
        "answer": "Walder Frey et Roose Bolton"
    },
    {
        "question": "Qui a trahi Robb Stark lors du Red Wedding ?",
        "options": ["Roose Bolton", "Edmure Tully", "Brynden Tully", "Rickard Karstark"],
        "answer": "Roose Bolton"
    },
    {
        "question": "Quelle bataille est connue comme la plus grande bataille navale ?",
        "options": ["La Bataille de la Néra", "La Bataille des Bâtards", "La Bataille de Winterfell", "La Bataille de Castle Black"],
        "answer": "La Bataille de la Néra"
    },
    {
        "question": "Qui a gagné la Bataille des Bâtards ?",
        "options": ["Jon Snow", "Ramsay Bolton", "Stannis Baratheon", "Roose Bolton"],
        "answer": "Jon Snow"
    },

    # Personnages - Familles et relations
    {
        "question": "Qui sont les parents de Joffrey Baratheon ?",
        "options": ["Cersei et Jaime Lannister", "Cersei et Robert Baratheon", "Cersei et Tywin Lannister", "Cersei et Stannis Baratheon"],
        "answer": "Cersei et Jaime Lannister"
    },
    {
        "question": "Qui est le père biologique de Jon Snow ?",
        "options": ["Rhaegar Targaryen", "Ned Stark", "Robert Baratheon", "Brandon Stark"],
        "answer": "Rhaegar Targaryen"
    },
    {
        "question": "Qui est la mère biologique de Jon Snow ?",
        "options": ["Lyanna Stark", "Catelyn Stark", "Ashara Dayne", "Wylla"],
        "answer": "Lyanna Stark"
    },
    {
        "question": "Qui est le plus jeune fils de Ned Stark ?",
        "options": ["Rickon Stark", "Bran Stark", "Robb Stark", "Jon Snow"],
        "answer": "Rickon Stark"
    },
    {
        "question": "Comment s'appelle la sœur jumelle de Jaime Lannister ?",
        "options": ["Cersei", "Sansa", "Arya", "Daenerys"],
        "answer": "Cersei"
    },
    {
        "question": "Qui est le frère nain de Cersei et Jaime ?",
        "options": ["Tyrion", "Tywin", "Kevan", "Lancel"],
        "answer": "Tyrion"
    },
    {
        "question": "Comment s'appelle le père de Cersei, Jaime et Tyrion ?",
        "options": ["Tywin Lannister", "Kevan Lannister", "Tytos Lannister", "Tommen Lannister"],
        "answer": "Tywin Lannister"
    },
    {
        "question": "Qui a épousé Sansa Stark après Joffrey ?",
        "options": ["Tyrion Lannister", "Ramsay Bolton", "Les deux", "Petyr Baelish"],
        "answer": "Les deux"
    },
    {
        "question": "Qui a épousé Margaery Tyrell en dernier ?",
        "options": ["Tommen Baratheon", "Joffrey Baratheon", "Renly Baratheon", "Loras Tyrell"],
        "answer": "Tommen Baratheon"
    },
    {
        "question": "Qui est le père de Gendry ?",
        "options": ["Robert Baratheon", "Stannis Baratheon", "Renly Baratheon", "Tywin Lannister"],
        "answer": "Robert Baratheon"
    },

    # Armes et objets
    {
        "question": "Comment s'appelle l'épée de Jon Snow ?",
        "options": ["Longclaw", "Ice", "Oathkeeper", "Heartsbane"],
        "answer": "Longclaw"
    },
    {
        "question": "Comment s'appelle l'épée ancestrale de la Maison Stark ?",
        "options": ["Ice", "Longclaw", "Oathkeeper", "Widow's Wail"],
        "answer": "Ice"
    },
    {
        "question": "Qui a refondu l'épée Ice en deux épées ?",
        "options": ["Tywin Lannister", "Ned Stark", "Jon Snow", "Jaime Lannister"],
        "answer": "Tywin Lannister"
    },
    {
        "question": "Comment s'appelle l'épée que Jaime a donnée à Brienne ?",
        "options": ["Oathkeeper", "Widow's Wail", "Longclaw", "Ice"],
        "answer": "Oathkeeper"
    },
    {
        "question": "Quel matériau peut tuer les Marcheurs Blancs ?",
        "options": ["Verredragon et acier valyrien", "Fer ordinaire", "Bronze", "Argent"],
        "answer": "Verredragon et acier valyrien"
    },
    {
        "question": "Comment s'appelle le poison utilisé pour tuer Joffrey ?",
        "options": ["The Strangler", "The Tears of Lys", "Nightshade", "Greyscale"],
        "answer": "The Strangler"
    },

    # Titres et surnoms
    {
        "question": "Quel est le surnom de Sandor Clegane ?",
        "options": ["The Hound", "The Mountain", "The Viper", "The Spider"],
        "answer": "The Hound"
    },
    {
        "question": "Quel est le surnom de Gregor Clegane ?",
        "options": ["The Mountain", "The Hound", "The Giant", "The Beast"],
        "answer": "The Mountain"
    },
    {
        "question": "Quel est le surnom d'Oberyn Martell ?",
        "options": ["The Red Viper", "The Black Viper", "The Sand Snake", "The Dornish Prince"],
        "answer": "The Red Viper"
    },
    {
        "question": "Quel est le surnom de Varys ?",
        "options": ["The Spider", "The Master of Whispers", "The Eunuch", "Tous ces surnoms"],
        "answer": "Tous ces surnoms"
    },
    {
        "question": "Quel est le surnom de Petyr Baelish ?",
        "options": ["Littlefinger", "The Mockingbird", "The Schemer", "The Climber"],
        "answer": "Littlefinger"
    },
    {
        "question": "Quel titre porte le chef de la Garde de Nuit ?",
        "options": ["Lord Commander", "Night King", "First Ranger", "Lord of the Wall"],
        "answer": "Lord Commander"
    },
    {
        "question": "Quel titre porte Daenerys à la fin de la série ?",
        "options": ["Queen of the Ashes", "Queen of the Seven Kingdoms", "Mother of Dragons", "Breaker of Chains"],
        "answer": "Queen of the Ashes"
    },

    # La Garde de Nuit
    {
        "question": "Quel serment prononcent les membres de la Garde de Nuit ?",
        "options": ["Night gathers, and now my watch begins", "Winter is coming", "The night is dark and full of terrors", "What is dead may never die"],
        "answer": "Night gathers, and now my watch begins"
    },
    {
        "question": "Qui était Lord Commander avant Jon Snow ?",
        "options": ["Jeor Mormont", "Alliser Thorne", "Benjen Stark", "Mance Rayder"],
        "answer": "Jeor Mormont"
    },
    {
        "question": "Qui a tué Jon Snow la première fois ?",
        "options": ["Les frères de la Garde de Nuit", "Les Sauvageons", "Les Marcheurs Blancs", "Ramsay Bolton"],
        "answer": "Les frères de la Garde de Nuit"
    },
    {
        "question": "Qui a ressuscité Jon Snow ?",
        "options": ["Melisandre", "Thoros de Myr", "Beric Dondarrion", "Le Seigneur de Lumière"],
        "answer": "Melisandre"
    },
    {
        "question": "Comment s'appelle le château principal de la Garde de Nuit ?",
        "options": ["Castle Black", "The Shadow Tower", "Eastwatch-by-the-Sea", "The Nightfort"],
        "answer": "Castle Black"
    },
    {
        "question": "Qui était le Roi-d'au-delà-du-Mur ?",
        "options": ["Mance Rayder", "Tormund Giantsbane", "The Lord of Bones", "Craster"],
        "answer": "Mance Rayder"
    },
    {
        "question": "Comment s'appelle l'ami sauvageron de Jon Snow ?",
        "options": ["Tormund Giantsbane", "Mance Rayder", "Ygritte", "Orell"],
        "answer": "Tormund Giantsbane"
    },
    {
        "question": "Comment s'appelle la sauvageon que Jon Snow a aimée ?",
        "options": ["Ygritte", "Gilly", "Osha", "Val"],
        "answer": "Ygritte"
    },
    {
        "question": "Quelle est la phrase célèbre d'Ygritte ?",
        "options": ["You know nothing, Jon Snow", "Winter is coming", "The North remembers", "What is dead may never die"],
        "answer": "You know nothing, Jon Snow"
    },

    # Religion et magie
    {
        "question": "Qui est la prêtresse rouge au service de Stannis ?",
        "options": ["Melisandre", "Mirri Maz Duur", "Kinvara", "Quaithe"],
        "answer": "Melisandre"
    },
    {
        "question": "Quel dieu adore Melisandre ?",
        "options": ["Le Seigneur de Lumière", "Le Dieu Noyé", "Le dieu aux Sept Visages", "Les Anciens Dieux"],
        "answer": "Le Seigneur de Lumière"
    },
    {
        "question": "Quel dieu adorent les Fer-nés (Greyjoy) ?",
        "options": ["Le Dieu Noyé", "Le Seigneur de Lumière", "Les Anciens Dieux", "Les Sept"],
        "answer": "Le Dieu Noyé"
    },
    {
        "question": "Combien y a-t-il de visages dans la religion des Sept ?",
        "options": ["Sept", "Un", "Trois", "Neuf"],
        "answer": "Sept"
    },
    {
        "question": "Qui a entraîné Arya à Braavos ?",
        "options": ["Jaqen H'ghar", "Syrio Forel", "The Waif", "The Kindly Man"],
        "answer": "Jaqen H'ghar"
    },
    {
        "question": "Quelle organisation d'assassins appartient Jaqen H'ghar ?",
        "options": ["Les Sans-Visage", "Les Immaculés", "La Garde de Nuit", "Les Sangliers"],
        "answer": "Les Sans-Visage"
    },
    {
        "question": "Qui peut voir le passé et le futur grâce à ses visions ?",
        "options": ["Bran Stark", "Melisandre", "Jojen Reed", "The Three-Eyed Raven"],
        "answer": "Bran Stark"
    },
    {
        "question": "Quel titre porte Bran à la fin ?",
        "options": ["The Three-Eyed Raven et Roi des Six Royaumes", "Roi du Nord", "Lord de Winterfell", "Main du Roi"],
        "answer": "The Three-Eyed Raven et Roi des Six Royaumes"
    },

    # Batailles et guerres
    {
        "question": "Qui a brûlé Port-Réal avec du feu grégeois ?",
        "options": ["Daenerys et Drogon", "Cersei Lannister", "Le Roi Fou", "Tyrion Lannister"],
        "answer": "Daenerys et Drogon"
    },
    {
        "question": "Qui a détruit le Grand Septuaire de Baelor ?",
        "options": ["Cersei Lannister", "Daenerys Targaryen", "Le Roi Fou", "Jon Snow"],
        "answer": "Cersei Lannister"
    },
    {
        "question": "Qui a tué le Roi de la Nuit ?",
        "options": ["Arya Stark", "Jon Snow", "Daenerys Targaryen", "Bran Stark"],
        "answer": "Arya Stark"
    },
    {
        "question": "Où s'est déroulée la bataille contre le Roi de la Nuit ?",
        "options": ["Winterfell", "Castle Black", "King's Landing", "The Wall"],
        "answer": "Winterfell"
    },
    {
        "question": "Qui a mené l'attaque surprise sur Casterly Rock ?",
        "options": ["Les Immaculés", "Les Dothrakis", "Jon Snow", "Jaime Lannister"],
        "answer": "Les Immaculés"
    },

    # Fins et destins
    {
        "question": "Qui a tué Daenerys Targaryen ?",
        "options": ["Jon Snow", "Arya Stark", "Tyrion Lannister", "Grey Worm"],
        "answer": "Jon Snow"
    },
    {
        "question": "Où est parti Jon Snow à la fin ?",
        "options": ["Au-delà du Mur avec les Sauvageons", "À Winterfell", "À Dragonstone", "En exil à Essos"],
        "answer": "Au-delà du Mur avec les Sauvageons"
    },
    {
        "question": "Qui devient Main du Roi à la fin ?",
        "options": ["Tyrion Lannister", "Davos Seaworth", "Brienne de Torth", "Samwell Tarly"],
        "answer": "Tyrion Lannister"
    },
    {
        "question": "Qui devient Reine du Nord indépendant ?",
        "options": ["Sansa Stark", "Arya Stark", "Brienne de Torth", "Yara Greyjoy"],
        "answer": "Sansa Stark"
    },
    {
        "question": "Où va Arya Stark à la fin ?",
        "options": ["Explorer l'Ouest de Westeros", "Winterfell", "King's Landing", "Braavos"],
        "answer": "Explorer l'Ouest de Westeros"
    },
    {
        "question": "Qui a écrit l'histoire 'A Song of Ice and Fire' dans la série ?",
        "options": ["Samwell Tarly", "Tyrion Lannister", "Bran Stark", "Maester Aemon"],
        "answer": "Samwell Tarly"
    },

    # Personnages secondaires
    {
        "question": "Comment s'appelle le maître d'armes qui a entraîné Arya ?",
        "options": ["Syrio Forel", "Jaqen H'ghar", "Sandor Clegane", "Bronn"],
        "answer": "Syrio Forel"
    },
    {
        "question": "Qui est le mercenaire devenu ami de Tyrion et Jaime ?",
        "options": ["Bronn", "Daario Naharis", "Jorah Mormont", "Grey Worm"],
        "answer": "Bronn"
    },
    {
        "question": "Comment s'appelle le commandant des Immaculés ?",
        "options": ["Grey Worm", "Missandei", "Daario Naharis", "Strong Belwas"],
        "answer": "Grey Worm"
    },
    {
        "question": "Comment s'appelle la conseillère et amie de Daenerys ?",
        "options": ["Missandei", "Grey Worm", "Irri", "Jhiqui"],
        "answer": "Missandei"
    },
    {
        "question": "Qui était le conseiller exilé de Daenerys, amoureux d'elle ?",
        "options": ["Jorah Mormont", "Barristan Selmy", "Daario Naharis", "Tyrion Lannister"],
        "answer": "Jorah Mormont"
    },
    {
        "question": "Comment s'appelle le géant qui combat aux côtés de Jon Snow ?",
        "options": ["Wun Wun", "Mag the Mighty", "Dongo", "Hodor"],
        "answer": "Wun Wun"
    },
    {
        "question": "Quelle est la phrase répétée par Hodor ?",
        "options": ["Hodor", "Winter is coming", "Hold the door", "My lord"],
        "answer": "Hodor"
    },
    {
        "question": "Que signifie 'Hodor' ?",
        "options": ["Hold the door", "Hod door", "Honour", "Rien, c'est son nom"],
        "answer": "Hold the door"
    },
    {
        "question": "Comment est mort Hodor ?",
        "options": ["En tenant la porte contre les marcheurs blancs", "Tué par Ramsay Bolton", "Dans la bataille de Winterfell", "De vieillesse"],
        "answer": "En tenant la porte contre les marcheurs blancs"
    },
    {
        "question": "Qui a torturé Theon Greyjoy ?",
        "options": ["Ramsay Bolton", "Roose Bolton", "Joffrey Baratheon", "The Mountain"],
        "answer": "Ramsay Bolton"
    },
    {
        "question": "Quel surnom a donné Ramsay à Theon ?",
        "options": ["Reek", "The Broken", "The Coward", "The Traitor"],
        "answer": "Reek"
    },
    {
        "question": "Qui a tué Ramsay Bolton ?",
        "options": ["Sansa Stark (avec ses chiens)", "Jon Snow", "Theon Greyjoy", "Arya Stark"],
        "answer": "Sansa Stark (avec ses chiens)"
    },
    {
        "question": "Comment est mort Theon Greyjoy ?",
        "options": ["Tué par le Roi de la Nuit en protégeant Bran", "Tué par Ramsay Bolton", "Noyé", "Dans la bataille de Winterfell"],
        "answer": "Tué par le Roi de la Nuit en protégeant Bran"
    },
    {
        "question": "Qui a tué Tywin Lannister ?",
        "options": ["Tyrion Lannister", "Jaime Lannister", "Cersei Lannister", "Arya Stark"],
        "answer": "Tyrion Lannister"
    },
    {
        "question": "Où Tyrion a-t-il tué Tywin ?",
        "options": ["Aux toilettes", "Dans son lit", "Dans la salle du trône", "À Casterly Rock"],
        "answer": "Aux toilettes"
    },
    {
        "question": "Comment est morte Margaery Tyrell ?",
        "options": ["Dans l'explosion du Grand Septuaire", "Empoisonnée", "Décapitée", "Dans la bataille"],
        "answer": "Dans l'explosion du Grand Septuaire"
    },
    {
        "question": "Comment est mort Tommen Baratheon ?",
        "options": ["Il s'est jeté par la fenêtre", "Empoisonné", "Tué par Cersei", "Dans la bataille"],
        "answer": "Il s'est jeté par la fenêtre"
    },
    {
        "question": "Qui a tué Littlefinger ?",
        "options": ["Arya Stark", "Sansa Stark", "Jon Snow", "Brienne de Torth"],
        "answer": "Arya Stark"
    },
    {
        "question": "Comment est mort Viserys Targaryen ?",
        "options": ["Couronne d'or fondu versée sur sa tête", "Brûlé par un dragon", "Décapité", "Empoisonné"],
        "answer": "Couronne d'or fondu versée sur sa tête"
    },
    {
        "question": "Qui a tué Khal Drogo indirectement ?",
        "options": ["Mirri Maz Duur", "Daenerys", "Viserys", "Jorah Mormont"],
        "answer": "Mirri Maz Duur"
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

print(f"Questions en double trouvées: {duplicate_count}")
print(f"Nombre de nouvelles questions uniques: {len(filtered_questions)}")

# Ajouter les nouvelles questions avec ID et UUID
next_id = current_max_id + 1
for q in filtered_questions:
    q["id"] = next_id
    q["uuid"] = str(uuid.uuid4())
    q["difficulty_level"] = 1
    next_id += 1
    got_quiz["questions"].append(q)

print(f"\nNouvelles questions ajoutées au quiz Game of Thrones")
print(f"Nombre total de questions: {len(got_quiz['questions'])}")

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

