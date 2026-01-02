import json
import uuid
from datetime import datetime

# Disney quiz data - 1000 questions
disney_questions = []

# Film release dates and basic info
disney_films = [
    ("Blanche-Neige et les Sept Nains", 1937, "Walt Disney", "David Hand"),
    ("Pinocchio", 1940, "Walt Disney", "Ben Sharpsteen, Hamilton Luske"),
    ("Fantasia", 1940, "Walt Disney", "Various"),
    ("Dumbo", 1941, "Walt Disney", "Ben Sharpsteen"),
    ("Bambi", 1942, "Walt Disney", "David Hand"),
    ("Saludos Amigos", 1942, "Walt Disney", "Various"),
    ("Les Trois Caballeros", 1944, "Walt Disney", "Norman Ferguson"),
    ("La Boîte à Musique", 1946, "Walt Disney", "Various"),
    ("Mélodie du Sud", 1946, "Walt Disney", "Harve Foster"),
    ("Coquin de Printemps", 1947, "Walt Disney", "Various"),
    ("Le Crapaud et le Maître d'École", 1949, "Walt Disney", "Various"),
    ("Cendrillon", 1950, "Walt Disney", "Clyde Geronimi, Wilfred Jackson"),
    ("Alice au Pays des Merveilles", 1951, "Walt Disney", "Clyde Geronimi"),
    ("Peter Pan", 1953, "Walt Disney", "Clyde Geronimi, Wilfred Jackson"),
    ("La Belle et le Clochard", 1955, "Walt Disney", "Clyde Geronimi"),
    ("La Belle au Bois Dormant", 1959, "Walt Disney", "Clyde Geronimi"),
    ("Les 101 Dalmatiens", 1961, "Walt Disney", "Clyde Geronimi"),
    ("Merlin l'Enchanteur", 1963, "Walt Disney", "Wolfgang Reitherman"),
    ("Le Livre de la Jungle", 1967, "Walt Disney", "Wolfgang Reitherman"),
    ("Les Aristochats", 1970, "Wolfgang Reitherman", "Wolfgang Reitherman"),
    ("Robin des Bois", 1973, "Wolfgang Reitherman", "Wolfgang Reitherman"),
    ("Les Aventures de Winnie l'Ourson", 1977, "Wolfgang Reitherman", "John Lounsbery"),
    ("Les Aventures de Bernard et Bianca", 1977, "Wolfgang Reitherman", "John Lounsbery"),
    ("Rox et Rouky", 1981, "Art Stevens", "Art Stevens"),
    ("Taram et le Chaudron Magique", 1985, "Ted Berman", "Ted Berman"),
    ("Basil, Détective Privé", 1986, "Ron Clements", "John Musker"),
    ("Oliver et Compagnie", 1988, "George Scribner", "George Scribner"),
    ("La Petite Sirène", 1989, "Ron Clements, John Musker", "Ron Clements, John Musker"),
    ("La Bande à Picsou, le film", 1990, "Bob Hathcock", "Bob Hathcock"),
    ("Bernard et Bianca au Pays des Kangourous", 1990, "Hendel Butoy", "Mike Gabriel"),
    ("La Belle et la Bête", 1991, "Gary Trousdale, Kirk Wise", "Gary Trousdale, Kirk Wise"),
    ("Aladdin", 1992, "Ron Clements, John Musker", "Ron Clements, John Musker"),
    ("Le Roi Lion", 1994, "Roger Allers, Rob Minkoff", "Roger Allers, Rob Minkoff"),
    ("Pocahontas", 1995, "Mike Gabriel, Eric Goldberg", "Mike Gabriel, Eric Goldberg"),
    ("Le Bossu de Notre-Dame", 1996, "Gary Trousdale, Kirk Wise", "Gary Trousdale, Kirk Wise"),
    ("Hercule", 1997, "Ron Clements, John Musker", "Ron Clements, John Musker"),
    ("Mulan", 1998, "Tony Bancroft, Barry Cook", "Tony Bancroft, Barry Cook"),
    ("Tarzan", 1999, "Kevin Lima, Chris Buck", "Kevin Lima, Chris Buck"),
    ("Fantasia 2000", 1999, "Various", "Various"),
    ("Dinosaure", 2000, "Eric Leighton, Ralph Zondag", "Eric Leighton, Ralph Zondag"),
    ("Kuzco, l'Empereur Mégalo", 2000, "Mark Dindal", "Mark Dindal"),
    ("Atlantide, l'Empire Perdu", 2001, "Gary Trousdale, Kirk Wise", "Gary Trousdale, Kirk Wise"),
    ("Lilo et Stitch", 2002, "Dean DeBlois, Chris Sanders", "Dean DeBlois, Chris Sanders"),
    ("La Planète au Trésor", 2002, "Ron Clements, John Musker", "Ron Clements, John Musker"),
    ("Frère des Ours", 2003, "Aaron Blaise, Robert Walker", "Aaron Blaise, Robert Walker"),
    ("La Ferme se Rebelle", 2004, "Will Finn, John Sanford", "Will Finn, John Sanford"),
    ("Chicken Little", 2005, "Mark Dindal", "Mark Dindal"),
    ("Bienvenue chez les Robinson", 2007, "Stephen J. Anderson", "Stephen J. Anderson"),
    ("Bolt", 2008, "Byron Howard, Chris Williams", "Byron Howard, Chris Williams"),
    ("La Princesse et la Grenouille", 2009, "Ron Clements, John Musker", "Ron Clements, John Musker"),
    ("Raiponce", 2010, "Nathan Greno, Byron Howard", "Nathan Greno, Byron Howard"),
    ("Winnie l'Ourson", 2011, "Stephen J. Anderson, Don Hall", "Stephen J. Anderson, Don Hall"),
    ("Les Mondes de Ralph", 2012, "Rich Moore", "Rich Moore"),
    ("La Reine des Neiges", 2013, "Chris Buck, Jennifer Lee", "Chris Buck, Jennifer Lee"),
    ("Les Nouveaux Héros", 2014, "Don Hall, Chris Williams", "Don Hall, Chris Williams"),
    ("Zootopie", 2016, "Byron Howard, Rich Moore", "Byron Howard, Rich Moore"),
    ("Vaiana", 2016, "Ron Clements, John Musker", "Ron Clements, John Musker"),
    ("Ralph 2.0", 2018, "Rich Moore, Phil Johnston", "Rich Moore, Phil Johnston"),
    ("La Reine des Neiges 2", 2019, "Chris Buck, Jennifer Lee", "Chris Buck, Jennifer Lee"),
    ("Raya et le Dernier Dragon", 2021, "Don Hall, Carlos López Estrada", "Don Hall, Carlos López Estrada"),
    ("Encanto", 2021, "Jared Bush, Byron Howard", "Jared Bush, Byron Howard"),
    ("Wish", 2023, "Chris Buck, Fawn Veerasunthorn", "Chris Buck, Fawn Veerasunthorn"),
]

# Main characters by film
main_characters = {
    "Blanche-Neige et les Sept Nains": ["Blanche-Neige", "Prince Charmant", "La Reine", "Simplet", "Grincheux"],
    "Pinocchio": ["Pinocchio", "Geppetto", "Jiminy Cricket", "La Fée Bleue", "Figaro"],
    "Dumbo": ["Dumbo", "Timothée", "Madame Jumbo", "Les Corbeaux"],
    "Bambi": ["Bambi", "Panpan", "Fleur", "Faline", "La Mère de Bambi"],
    "Cendrillon": ["Cendrillon", "Prince Charmant", "Marraine Fée", "Jaq", "Gus"],
    "Alice au Pays des Merveilles": ["Alice", "Le Chapelier Fou", "Le Chat de Chester", "La Reine de Cœur", "Le Lapin Blanc"],
    "Peter Pan": ["Peter Pan", "Wendy", "Capitaine Crochet", "Clochette", "Monsieur Mouche"],
    "La Belle et le Clochard": ["Lady", "Clochard", "Tony", "Joe", "Jock"],
    "La Belle au Bois Dormant": ["Aurore", "Prince Philippe", "Maléfique", "Pimprenelle", "Flora"],
    "Les 101 Dalmatiens": ["Pongo", "Perdita", "Cruella d'Enfer", "Roger", "Anita"],
    "Le Livre de la Jungle": ["Mowgli", "Baloo", "Bagheera", "Shere Khan", "Kaa"],
    "Les Aristochats": ["Duchesse", "Thomas O'Malley", "Marie", "Toulouse", "Berlioz"],
    "Robin des Bois": ["Robin des Bois", "Petit Jean", "Lady Marianne", "Prince Jean", "Shérif de Nottingham"],
    "La Petite Sirène": ["Ariel", "Prince Éric", "Ursula", "Sébastien", "Polochon"],
    "La Belle et la Bête": ["Belle", "La Bête", "Gaston", "Lumière", "Big Ben"],
    "Aladdin": ["Aladdin", "Jasmine", "Génie", "Jafar", "Abou"],
    "Le Roi Lion": ["Simba", "Mufasa", "Scar", "Nala", "Timon", "Pumbaa"],
    "Pocahontas": ["Pocahontas", "John Smith", "Meeko", "Flit", "Grand-Mère Feuillage"],
    "Le Bossu de Notre-Dame": ["Quasimodo", "Esmeralda", "Phoebus", "Frollo", "Clopin"],
    "Hercule": ["Hercule", "Mégara", "Hadès", "Philoctète", "Pégase"],
    "Mulan": ["Mulan", "Mushu", "Li Shang", "Shan Yu", "Cri-Kee"],
    "Tarzan": ["Tarzan", "Jane", "Kala", "Kerchak", "Terk"],
    "Kuzco, l'Empereur Mégalo": ["Kuzco", "Pacha", "Yzma", "Kronk"],
    "Lilo et Stitch": ["Lilo", "Stitch", "Nani", "Jumba", "Pleakley"],
    "La Princesse et la Grenouille": ["Tiana", "Prince Naveen", "Dr Facilier", "Louis", "Ray"],
    "Raiponce": ["Raiponce", "Flynn Rider", "Mère Gothel", "Pascal", "Maximus"],
    "Les Mondes de Ralph": ["Ralph", "Vanellope", "Felix", "Calhoun"],
    "La Reine des Neiges": ["Elsa", "Anna", "Kristoff", "Olaf", "Hans"],
    "Les Nouveaux Héros": ["Hiro", "Baymax", "Tadashi", "GoGo", "Wasabi"],
    "Zootopie": ["Judy Hopps", "Nick Wilde", "Chef Bogo", "Bellwether", "Flash"],
    "Vaiana": ["Vaiana", "Maui", "Te Fiti", "Hei Hei", "Pua"],
    "La Reine des Neiges 2": ["Elsa", "Anna", "Kristoff", "Olaf", "Nokk"],
    "Encanto": ["Mirabel", "Isabela", "Luisa", "Bruno", "Abuela Alma"],
}

# Songs by film
famous_songs = {
    "Blanche-Neige et les Sept Nains": ["Heigh-Ho", "Un Jour Mon Prince Viendra"],
    "Pinocchio": ["Quand On Prie la Bonne Étoile"],
    "Cendrillon": ["Bibbidi-Bobbidi-Boo", "Un Rêve est un Souhait"],
    "Alice au Pays des Merveilles": ["Dans Un Monde Qui n'Existe Pas"],
    "Peter Pan": ["Tu T'Envoles", "La Deuxième Étoile"],
    "La Belle au Bois Dormant": ["J'en ai Rêvé"],
    "Le Livre de la Jungle": ["Il en Faut Peu Pour Être Heureux", "Être un Homme Comme Vous"],
    "Les Aristochats": ["Tout le Monde Veut Devenir un Cat"],
    "La Petite Sirène": ["Partir Là-Bas", "Sous l'Océan", "Embrasse-La"],
    "La Belle et la Bête": ["Histoire Éternelle", "C'est la Fête", "Belle"],
    "Aladdin": ["Ce Rêve Bleu", "Je Suis Ton Meilleur Ami", "Prince Ali"],
    "Le Roi Lion": ["L'Histoire de la Vie", "Je Voudrais Déjà Être Roi", "Hakuna Matata", "L'Amour Brille Sous les Étoiles"],
    "Pocahontas": ["L'Air du Vent", "Au Détour de la Rivière"],
    "Le Bossu de Notre-Dame": ["Le Temps des Cathédrales", "Vivre"],
    "Hercule": ["De Zéro en Héros", "Je Vais Tout Droit"],
    "Mulan": ["Comme un Homme", "Réflexion"],
    "Tarzan": ["De l'Autre Côté", "Toujours dans Mon Cœur"],
    "La Princesse et la Grenouille": ["Je Vais Tout Donner", "Je Vois Là-Bas"],
    "Raiponce": ["Moi J'ai un Rêve", "Je Veux y Croire"],
    "La Reine des Neiges": ["Libérée, Délivrée", "L'Amour est un Cadeau", "Viens Faire un Bonhomme de Neige"],
    "Vaiana": ["Là où je Vais", "Je Suis Vaiana"],
    "La Reine des Neiges 2": ["Show Yourself", "Into the Unknown"],
    "Encanto": ["Ne Parlons Pas de Bruno", "Quelles Sont Ces Familles", "Dos Oruguitas"],
}

# Villains
villains = {
    "Blanche-Neige et les Sept Nains": "La Reine Grimhilde",
    "Pinocchio": "Stromboli",
    "Cendrillon": "Dame Tremaine",
    "Alice au Pays des Merveilles": "La Reine de Cœur",
    "Peter Pan": "Capitaine Crochet",
    "La Belle au Bois Dormant": "Maléfique",
    "Les 101 Dalmatiens": "Cruella d'Enfer",
    "Le Livre de la Jungle": "Shere Khan",
    "La Petite Sirène": "Ursula",
    "La Belle et la Bête": "Gaston",
    "Aladdin": "Jafar",
    "Le Roi Lion": "Scar",
    "Pocahontas": "Gouverneur Ratcliffe",
    "Le Bossu de Notre-Dame": "Juge Claude Frollo",
    "Hercule": "Hadès",
    "Mulan": "Shan Yu",
    "Tarzan": "Clayton",
    "Kuzco, l'Empereur Mégalo": "Yzma",
    "Lilo et Stitch": "Capitaine Gantu",
    "La Princesse et la Grenouille": "Dr Facilier",
    "Raiponce": "Mère Gothel",
    "Les Mondes de Ralph": "King Candy/Turbo",
    "La Reine des Neiges": "Prince Hans",
    "Les Nouveaux Héros": "Yokai",
    "Zootopie": "Bellwether",
    "Vaiana": "Tamatoa",
    "La Reine des Neiges 2": "Aucun vrai méchant",
    "Encanto": "Aucun vrai méchant",
}

question_id = 1

# Questions about release years
for film, year, producer, director in disney_films[:50]:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"En quelle année le film '{film}' est-il sorti ?",
        "difficulty_level": 2,
        "options": [str(year), str(year-3), str(year+2), str(year+5)],
        "answer": str(year)
    })
    question_id += 1

# Questions about directors
for film, year, producer, director in disney_films[:50]:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Qui a réalisé le film '{film}' ?",
        "difficulty_level": 3,
        "options": [director, "John Lasseter", "Brad Bird", "Pete Docter"],
        "answer": director
    })
    question_id += 1

# Questions about main characters
for film, characters in list(main_characters.items())[:30]:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Quel est le personnage principal du film '{film}' ?",
        "difficulty_level": 1,
        "options": [characters[0], "Mickey Mouse", "Donald Duck", "Dingo"],
        "answer": characters[0]
    })
    question_id += 1

# Questions about sidekick characters
for film, characters in list(main_characters.items())[:30]:
    if len(characters) >= 3:
        disney_questions.append({
            "id": question_id,
            "uuid": str(uuid.uuid4()),
            "question": f"Parmi ces personnages, lequel fait partie du film '{film}' ?",
            "difficulty_level": 2,
            "options": [characters[2], "Simba", "Ariel", "Belle"],
            "answer": characters[2]
        })
        question_id += 1

# Questions about songs
for film, songs in list(famous_songs.items())[:25]:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Quelle chanson emblématique provient du film '{film}' ?",
        "difficulty_level": 2,
        "options": [songs[0], "Libérée, Délivrée", "Ce Rêve Bleu", "Hakuna Matata"],
        "answer": songs[0]
    })
    question_id += 1

# Questions about villains
for film, villain in list(villains.items())[:28]:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Qui est le méchant principal dans le film '{film}' ?",
        "difficulty_level": 2,
        "options": [villain, "Maléfique", "Ursula", "Jafar"],
        "answer": villain
    })
    question_id += 1

# Additional variety questions
variety_questions = [
    ("Quel est le premier long métrage d'animation de Disney ?", ["Blanche-Neige et les Sept Nains", "Pinocchio", "Fantasia", "Dumbo"], "Blanche-Neige et les Sept Nains", 1),
    ("Combien de nains accompagnent Blanche-Neige ?", ["7", "5", "9", "6"], "7", 1),
    ("Quel est le nom du chat dans 'Cendrillon' ?", ["Lucifer", "Figaro", "Duchesse", "Thomas"], "Lucifer", 2),
    ("Dans 'La Belle et la Bête', quel objet est Lumière ?", ["Un chandelier", "Une horloge", "Une théière", "Une armoire"], "Un chandelier", 1),
    ("Dans 'Aladdin', comment s'appelle le singe d'Aladdin ?", ["Abou", "Iago", "Rajah", "Pascal"], "Abou", 1),
    ("Quel est le nom du lion dans 'Le Roi Lion' ?", ["Simba", "Mufasa", "Scar", "Nala"], "Simba", 1),
    ("Dans 'La Petite Sirène', combien de sœurs a Ariel ?", ["6", "4", "5", "7"], "6", 2),
    ("Quel animal est Dumbo ?", ["Un éléphant", "Un lion", "Un singe", "Un ours"], "Un éléphant", 1),
    ("Dans 'La Reine des Neiges', quel est le nom du bonhomme de neige ?", ["Olaf", "Sven", "Kristoff", "Hans"], "Olaf", 1),
    ("Quelle princesse a de très longs cheveux magiques ?", ["Raiponce", "Aurore", "Ariel", "Belle"], "Raiponce", 1),
]

for q, opts, ans, diff in variety_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# More detailed questions about specific films
detailed_questions = [
    ("Dans 'Le Roi Lion', comment s'appelle le père de Simba ?", ["Mufasa", "Scar", "Rafiki", "Zazu"], "Mufasa", 1),
    ("Dans 'Le Roi Lion', qui est l'oncle de Simba ?", ["Scar", "Mufasa", "Timon", "Pumbaa"], "Scar", 1),
    ("Dans 'Le Roi Lion', quels sont les deux compagnons de Simba ?", ["Timon et Pumbaa", "Zazu et Rafiki", "Scar et Nala", "Timon et Zazu"], "Timon et Pumbaa", 1),
    ("Dans 'Aladdin', quel est le nom du perroquet de Jafar ?", ["Iago", "Abou", "Rajah", "Zazu"], "Iago", 2),
    ("Dans 'Aladdin', quel est le nom du tigre de Jasmine ?", ["Rajah", "Shere Khan", "Bagheera", "Tigrou"], "Rajah", 2),
    ("Dans 'La Belle et la Bête', qui est transformé en horloge ?", ["Big Ben", "Lumière", "Zip", "Plumette"], "Big Ben", 2),
    ("Dans 'La Belle et la Bête', qui est transformée en théière ?", ["Mrs Samovar", "Plumette", "Armoire", "Zip"], "Mrs Samovar", 2),
    ("Dans 'La Petite Sirène', quel est le nom du crabe musicien ?", ["Sébastien", "Polochon", "Eurêka", "Louis"], "Sébastien", 1),
    ("Dans 'La Petite Sirène', quel est le nom du poisson ami d'Ariel ?", ["Polochon", "Sébastien", "Eurêka", "Nemo"], "Polochon", 1),
    ("Dans 'Mulan', quel est le nom du dragon ?", ["Mushu", "Cri-Kee", "Khan", "Shan Yu"], "Mushu", 1),
    ("Dans 'Hercule', qui entraîne Hercule ?", ["Philoctète", "Zeus", "Hadès", "Mégara"], "Philoctète", 2),
    ("Dans 'Tarzan', quel est le nom de la mère adoptive de Tarzan ?", ["Kala", "Jane", "Terk", "Tantor"], "Kala", 2),
    ("Dans 'Raiponce', quel est le vrai nom de Flynn Rider ?", ["Eugene Fitzherbert", "John Smith", "Prince Éric", "Prince Naveen"], "Eugene Fitzherbert", 3),
    ("Dans 'La Reine des Neiges', quel est le nom du renne de Kristoff ?", ["Sven", "Olaf", "Hans", "Oaken"], "Sven", 1),
    ("Dans 'Zootopie', quelle est la profession de Judy Hopps ?", ["Policière", "Détective", "Avocate", "Maire"], "Policière", 1),
    ("Dans 'Vaiana', quel demi-dieu accompagne Vaiana ?", ["Maui", "Tamatoa", "Te Fiti", "Heihei"], "Maui", 1),
    ("Dans 'Les 101 Dalmatiens', qui sont les deux dalmatiens parents ?", ["Pongo et Perdita", "Roger et Anita", "Lucky et Patch", "Rolly et Penny"], "Pongo et Perdita", 1),
    ("Dans 'Peter Pan', où habite Peter Pan ?", ["Le Pays Imaginaire", "Londres", "L'Île au Trésor", "Wonderland"], "Le Pays Imaginaire", 1),
    ("Dans 'Alice au Pays des Merveilles', quelle couleur Alice doit-elle peindre les roses ?", ["Rouge", "Blanche", "Jaune", "Rose"], "Rouge", 2),
    ("Dans 'Cendrillon', à quelle heure se termine le sortilège ?", ["Minuit", "23h", "Minuit et demi", "1h du matin"], "Minuit", 1),
]

for q, opts, ans, diff in detailed_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about Disney princesses
princess_questions = [
    ("Quelle princesse a perdu sa pantoufle de verre ?", ["Cendrillon", "Aurore", "Belle", "Ariel"], "Cendrillon", 1),
    ("Quelle princesse vit sous l'océan ?", ["Ariel", "Vaiana", "Pocahontas", "Jasmine"], "Ariel", 1),
    ("Quelle princesse aime lire des livres ?", ["Belle", "Ariel", "Cendrillon", "Jasmine"], "Belle", 1),
    ("Quelle princesse a des pouvoirs de glace ?", ["Elsa", "Anna", "Aurore", "Mulan"], "Elsa", 1),
    ("Quelle princesse se transforme en grenouille ?", ["Tiana", "Ariel", "Belle", "Cendrillon"], "Tiana", 2),
    ("Quelle princesse a été endormie par une pomme empoisonnée ?", ["Blanche-Neige", "Aurore", "Cendrillon", "Belle"], "Blanche-Neige", 1),
    ("Quelle princesse a été endormie pendant 100 ans ?", ["Aurore", "Blanche-Neige", "Cendrillon", "Ariel"], "Aurore", 1),
    ("Quelle princesse vole sur un tapis magique ?", ["Jasmine", "Ariel", "Belle", "Pocahontas"], "Jasmine", 1),
    ("Quelle princesse se déguise en homme pour sauver son père ?", ["Mulan", "Pocahontas", "Tiana", "Mérida"], "Mulan", 1),
    ("Quelle princesse a un caméléon comme animal de compagnie ?", ["Raiponce", "Tiana", "Jasmine", "Ariel"], "Raiponce", 2),
    ("Combien de princesses Disney officielles existe-t-il ?", ["Plus de 10", "5", "7", "15"], "Plus de 10", 2),
    ("Quelle princesse n'est pas d'origine royale au début de son histoire ?", ["Cendrillon", "Aurore", "Jasmine", "Ariel"], "Cendrillon", 2),
    ("Quelle princesse a une sœur qui s'appelle Anna ?", ["Elsa", "Aurore", "Ariel", "Tiana"], "Elsa", 1),
    ("Quelle est la couleur de la robe de Belle dans 'La Belle et la Bête' ?", ["Jaune", "Bleue", "Rose", "Verte"], "Jaune", 1),
    ("Quelle princesse voyage sur un bateau pour découvrir de nouvelles terres ?", ["Pocahontas", "Vaiana", "Ariel", "Jasmine"], "Pocahontas", 2),
]

for q, opts, ans, diff in princess_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about sidekicks and animals
sidekick_questions = [
    ("Quel est le nom du cheval de Raiponce ?", ["Maximus", "Philippe", "Khan", "Samson"], "Maximus", 2),
    ("Quel est le nom du cheval de Mulan ?", ["Khan", "Maximus", "Philippe", "Angus"], "Khan", 2),
    ("Quel est le nom de la souris dans 'Cendrillon' ?", ["Jaq et Gus", "Timothée", "Bernard", "Basil"], "Jaq et Gus", 2),
    ("Quel est le nom du grillon dans 'Pinocchio' ?", ["Jiminy Cricket", "Cri-Kee", "Gus", "Timothée"], "Jiminy Cricket", 1),
    ("Quel est le nom du cochon dans 'Vaiana' ?", ["Pua", "Heihei", "Pumbaa", "Timon"], "Pua", 2),
    ("Quel est le nom du coq dans 'Vaiana' ?", ["Heihei", "Pua", "Alan-a-Dale", "Zazu"], "Heihei", 2),
    ("Quel oiseau parle dans 'Le Roi Lion' ?", ["Zazu", "Iago", "Flit", "Archimède"], "Zazu", 2),
    ("Quel est le nom du mandrill sage dans 'Le Roi Lion' ?", ["Rafiki", "Zazu", "Pumbaa", "Timon"], "Rafiki", 2),
    ("Dans 'Pocahontas', quel est le nom du raton laveur ?", ["Meeko", "Flit", "Percy", "Redfeather"], "Meeko", 2),
    ("Dans 'Pocahontas', quel est le nom du colibri ?", ["Flit", "Meeko", "Percy", "Redfeather"], "Flit", 3),
    ("Quel est le nom du cheval du Prince dans 'La Belle au Bois Dormant' ?", ["Samson", "Philippe", "Maximus", "Khan"], "Samson", 3),
    ("Dans 'Les Aristochats', quels sont les chatons de Duchesse ?", ["Marie, Toulouse et Berlioz", "Figaro, Cléo et Gidéon", "Jaq, Gus et Lucifer", "Patch, Lucky et Rolly"], "Marie, Toulouse et Berlioz", 2),
    ("Quel est l'animal de compagnie de la Reine dans 'Blanche-Neige' ?", ["Un corbeau", "Un chat", "Un serpent", "Un loup"], "Un corbeau", 3),
    ("Dans 'Aladdin', quel type de tapis accompagne Aladdin ?", ["Un tapis volant", "Un tapis persan", "Un tapis rouge", "Un tapis magique"], "Un tapis volant", 1),
    ("Quel est le nom du caméléon dans 'Raiponce' ?", ["Pascal", "Rajah", "Abou", "Meeko"], "Pascal", 1),
]

for q, opts, ans, diff in sidekick_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about music and songs
music_questions = [
    ("Quelle chanson Elsa chante-t-elle dans 'La Reine des Neiges' ?", ["Libérée, Délivrée", "L'Amour est un Cadeau", "Veux-tu Faire un Bonhomme de Neige", "En Été"], "Libérée, Délivrée", 1),
    ("Dans 'Le Roi Lion', que signifie 'Hakuna Matata' ?", ["Pas de soucis", "Roi Lion", "Cercle de la Vie", "Amitié"], "Pas de soucis", 1),
    ("Quelle chanson célèbre provient du film 'La Belle et la Bête' ?", ["Histoire Éternelle", "Ce Rêve Bleu", "Hakuna Matata", "Partir Là-Bas"], "Histoire Éternelle", 1),
    ("Dans 'Aladdin', sur quoi Aladdin et Jasmine volent-ils pendant 'Ce Rêve Bleu' ?", ["Un tapis volant", "Un éléphant", "Un chameau", "Un cheval"], "Un tapis volant", 1),
    ("Quelle chanson les sept nains chantent-ils en allant au travail ?", ["Heigh-Ho", "Hakuna Matata", "Il en Faut Peu", "Siffler en Travaillant"], "Heigh-Ho", 1),
    ("Dans 'Le Livre de la Jungle', quelle chanson Baloo chante-t-il ?", ["Il en Faut Peu Pour Être Heureux", "Être un Homme Comme Vous", "Le Livre de la Jungle", "Hakuna Matata"], "Il en Faut Peu Pour Être Heureux", 1),
    ("Quelle chanson célèbre est associée à Mulan ?", ["Comme un Homme", "Réflexion", "Je Vais Tout Droit", "Histoire Éternelle"], "Comme un Homme", 1),
    ("Dans 'Pocahontas', quelle est la chanson principale ?", ["L'Air du Vent", "Au Détour de la Rivière", "Histoire Éternelle", "Partir Là-Bas"], "L'Air du Vent", 1),
    ("Quelle chanson Ariel chante-t-elle sur son rocher ?", ["Partir Là-Bas", "Sous l'Océan", "Embrasse-La", "Histoire Éternelle"], "Partir Là-Bas", 1),
    ("Dans 'Tarzan', quelle chanson Phil Collins a-t-il écrite ?", ["De l'Autre Côté", "Toujours dans Mon Cœur", "Histoire Éternelle", "Ce Rêve Bleu"], "De l'Autre Côté", 2),
    ("Quelle chanson du 'Roi Lion' parle du cycle de la vie ?", ["L'Histoire de la Vie", "Hakuna Matata", "Je Voudrais Déjà Être Roi", "L'Amour Brille"], "L'Histoire de la Vie", 1),
    ("Dans 'Vaiana', quelle chanson parle de voyager sur l'océan ?", ["Là où je Vais", "Je Suis Vaiana", "Shiny", "We Know the Way"], "Là où je Vais", 2),
    ("Dans 'Encanto', quelle chanson parle de Bruno ?", ["Ne Parlons Pas de Bruno", "Quelles Sont Ces Familles", "Dos Oruguitas", "Colombia, Mi Encanto"], "Ne Parlons Pas de Bruno", 1),
    ("Quelle est la berceuse de 'La Belle au Bois Dormant' ?", ["J'en ai Rêvé", "Un Jour Mon Prince Viendra", "Un Rêve est un Souhait", "Histoire Éternelle"], "J'en ai Rêvé", 2),
    ("Dans 'Raiponce', quelle chanson chante-t-elle sur les lanternes ?", ["Je Veux y Croire", "Moi J'ai un Rêve", "Libre", "Partir Là-Bas"], "Je Veux y Croire", 2),
]

for q, opts, ans, diff in music_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Continue generating more questions to reach 1000
# Questions about settings and locations
location_questions = [
    ("Dans quelle ville se déroule 'Raiponce' ?", ["Royaume de Corona", "Royaume d'Arendelle", "Agrabah", "Atlantica"], "Royaume de Corona", 2),
    ("Dans quel pays se déroule 'Mulan' ?", ["Chine", "Japon", "Corée", "Mongolie"], "Chine", 1),
    ("Dans quelle ville se déroule 'Aladdin' ?", ["Agrabah", "Bagdad", "Damas", "Le Caire"], "Agrabah", 1),
    ("Dans quel pays se déroule 'La Reine des Neiges' ?", ["Norvège/Arendelle", "Islande", "Suède", "Danemark"], "Norvège/Arendelle", 2),
    ("Sur quelle île se déroule 'Vaiana' ?", ["Motunui", "Hawaï", "Tahiti", "Bora Bora"], "Motunui", 2),
    ("Dans quelle ville se déroule 'Les Aristochats' ?", ["Paris", "Londres", "Rome", "Vienne"], "Paris", 1),
    ("Dans quelle ville se déroule 'Le Bossu de Notre-Dame' ?", ["Paris", "Londres", "Rome", "Madrid"], "Paris", 1),
    ("Dans quel pays africain se déroule 'Le Roi Lion' ?", ["Savane africaine", "Kenya", "Tanzanie", "Afrique du Sud"], "Savane africaine", 2),
    ("Où se déroule 'Lilo et Stitch' ?", ["Hawaï", "Californie", "Floride", "Polynésie"], "Hawaï", 1),
    ("Dans quelle jungle se déroule 'Tarzan' ?", ["Afrique", "Amazonie", "Asie", "Australie"], "Afrique", 2),
    ("Où habite Belle dans 'La Belle et la Bête' ?", ["Un petit village français", "Paris", "Londres", "Un château"], "Un petit village français", 1),
    ("Dans quel pays se déroule 'Pocahontas' ?", ["Virginie, Amérique", "Canada", "Mexique", "Brésil"], "Virginie, Amérique", 2),
    ("Où se trouve le château de la Bête ?", ["Dans une forêt enchantée", "À Paris", "Dans les Alpes", "En Bavière"], "Dans une forêt enchantée", 2),
    ("Dans quelle ville futuriste se déroule 'Les Nouveaux Héros' ?", ["San Fransokyo", "Tokyo", "San Francisco", "New York"], "San Fransokyo", 2),
    ("Où se déroule 'Zootopie' ?", ["Zootopie", "New York", "Los Angeles", "Animal City"], "Zootopie", 1),
]

for q, opts, ans, diff in location_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

print(f"Generated {len(disney_questions)} questions so far...")

# More questions about specific plot points
plot_questions = [
    ("Que perd Cendrillon au bal ?", ["Une pantoufle de verre", "Un collier", "Un gant", "Un diadème"], "Une pantoufle de verre", 1),
    ("Comment Blanche-Neige est-elle empoisonnée ?", ["Avec une pomme", "Avec du vin", "Avec une rose", "Avec un gâteau"], "Avec une pomme", 1),
    ("Que veut Ariel plus que tout ?", ["Devenir humaine", "Être une sirène", "Voyager", "Chanter"], "Devenir humaine", 1),
    ("Quel objet la Bête offre-t-il à Belle ?", ["Une bibliothèque", "Une rose", "Un miroir magique", "Une robe"], "Une bibliothèque", 2),
    ("Combien de souhaits le Génie peut-il exaucer ?", ["3", "5", "Illimités", "1"], "3", 1),
    ("Que recherche Aladdin dans la Caverne aux Merveilles ?", ["Une lampe magique", "Un trésor", "Une couronne", "Une épée"], "Une lampe magique", 1),
    ("Pourquoi Elsa s'enfuit-elle du royaume ?", ["Elle a peur de ses pouvoirs", "Elle est en colère", "Elle veut voyager", "Elle fuit un méchant"], "Elle a peur de ses pouvoirs", 1),
    ("Quel est le rêve de Raiponce ?", ["Voir les lanternes", "Sortir de sa tour", "Se marier", "Devenir princesse"], "Voir les lanternes", 1),
    ("Pourquoi Mulan s'engage-t-elle dans l'armée ?", ["Pour sauver son père", "Pour l'honneur", "Pour voyager", "Pour devenir guerrière"], "Pour sauver son père", 1),
    ("Que cherche Moana ?", ["À sauver son île", "À devenir chef", "À naviguer", "À trouver un trésor"], "À sauver son île", 1),
    ("Pourquoi Aurore s'endort-elle ?", ["Elle se pique le doigt", "Elle mange une pomme", "Un sort", "Elle est fatiguée"], "Elle se pique le doigt", 1),
    ("Que doit faire Tiana pour redevenir humaine ?", ["Embrasser un prince", "Trouver l'étoile", "Faire un vœu", "Attendre minuit"], "Embrasser un prince", 2),
    ("Quel est le secret de Mirabel dans 'Encanto' ?", ["Elle n'a pas de pouvoir magique", "Elle a un pouvoir caché", "Elle est adoptée", "Elle est malade"], "Elle n'a pas de pouvoir magique", 2),
    ("Que veut Hercule ?", ["Devenir un vrai héros", "Être un dieu", "Être fort", "Être riche"], "Devenir un vrai héros", 1),
    ("Pourquoi Judy Hopps va-t-elle à Zootopie ?", ["Pour devenir policière", "Pour étudier", "Pour voir sa famille", "Pour fuir"], "Pour devenir policière", 1),
]

for q, opts, ans, diff in plot_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about magic items
magic_items_questions = [
    ("Quel objet magique possède la Reine dans 'Blanche-Neige' ?", ["Un miroir magique", "Une baguette", "Une pomme", "Une couronne"], "Un miroir magique", 1),
    ("Que contient la lampe dans 'Aladdin' ?", ["Un génie", "Un trésor", "Un sort", "Un souhait"], "Un génie", 1),
    ("Quel objet identifie Cendrillon ?", ["Une pantoufle de verre", "Un collier", "Une robe", "Un carrosse"], "Une pantoufle de verre", 1),
    ("Qu'utilise la marraine fée dans 'Cendrillon' ?", ["Une baguette magique", "Un livre de sorts", "Une potion", "Un miroir"], "Une baguette magique", 1),
    ("Quel objet la Bête garde-t-il précieusement ?", ["Une rose enchantée", "Un miroir", "Une couronne", "Un livre"], "Une rose enchantée", 1),
    ("Que garde Ursula en échange de la voix d'Ariel ?", ["Sa voix dans un coquillage", "Son âme", "Ses cheveux", "Son trident"], "Sa voix dans un coquillage", 2),
    ("Quel objet permet à Maléfique de maudire Aurore ?", ["Un rouet", "Une rose", "Une pomme", "Un miroir"], "Un rouet", 2),
    ("Dans 'Raiponce', qu'est-ce qui donne à Raiponce ses pouvoirs ?", ["Une fleur magique", "Une potion", "Un sort", "La lune"], "Une fleur magique", 2),
    ("Quel tapis aide Aladdin ?", ["Un tapis volant", "Un tapis magique", "Un tapis persan", "Un tapis royal"], "Un tapis volant", 1),
    ("Que possède Jafar pour contrôler le Sultan ?", ["Un bâton serpent", "Une lampe", "Un anneau", "Un livre"], "Un bâton serpent", 3),
]

for q, opts, ans, diff in magic_items_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about transformations
transformation_questions = [
    ("En quoi la citrouille se transforme-t-elle dans 'Cendrillon' ?", ["En carrosse", "En château", "En robe", "En cheval"], "En carrosse", 1),
    ("En quoi la Bête était-elle transformée avant ?", ["Un prince", "Un roi", "Un chevalier", "Un paysan"], "Un prince", 1),
    ("En quoi Tiana se transforme-t-elle ?", ["En grenouille", "En princesse", "En oiseau", "En chat"], "En grenouille", 1),
    ("En quoi Kuzco est-il transformé ?", ["En lama", "En âne", "En cochon", "En singe"], "En lama", 1),
    ("Que devient Pinocchio quand il ment ?", ["Son nez s'allonge", "Il devient âne", "Il rétrécit", "Il disparaît"], "Son nez s'allonge", 1),
    ("En quel animal Merlin transforme-t-il Arthur ?", ["Plusieurs animaux", "Un oiseau", "Un poisson", "Un écureuil"], "Plusieurs animaux", 2),
    ("Que se passe-t-il quand Ariel obtient des jambes ?", ["Elle perd sa voix", "Elle perd ses cheveux", "Elle devient mortelle", "Elle oublie tout"], "Elle perd sa voix", 1),
    ("En quoi les serviteurs du château sont-ils transformés dans 'La Belle et la Bête' ?", ["En objets", "En animaux", "En statues", "En plantes"], "En objets", 1),
    ("Quel garçon devient un âne dans 'Pinocchio' ?", ["Lumignon", "Geppetto", "Jiminy", "Stromboli"], "Lumignon", 3),
    ("Que devient Stitch quand il est gentil ?", ["Il devient bon", "Il grandit", "Il change de couleur", "Il parle"], "Il devient bon", 2),
]

for q, opts, ans, diff in transformation_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Continuing to generate more questions...
print(f"Current count: {len(disney_questions)} questions")

# We need to generate many more questions to reach 1000
# Let's create a function to generate similar questions with variations

def generate_character_questions(film, character, char_type, difficulty):
    questions = []
    global question_id

    questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Dans '{film}', qui est {character} ?",
        "difficulty_level": difficulty,
        "options": [char_type, "Un méchant", "Un sidekick", "Un animal"],
        "answer": char_type
    })
    question_id += 1

    return questions

# Generate more varied questions
films_extended = [
    ("Blanche-Neige et les Sept Nains", "Snow White and the Seven Dwarfs", "Blanche-Neige", "princesse"),
    ("Pinocchio", "Pinocchio", "Pinocchio", "pantin de bois"),
    ("Fantasia", "Fantasia", "Mickey Mouse", "sorcier"),
    ("Dumbo", "Dumbo", "Dumbo", "éléphanteau"),
    ("Bambi", "Bambi", "Bambi", "faon"),
    ("Cendrillon", "Cinderella", "Cendrillon", "princesse"),
    ("Alice au Pays des Merveilles", "Alice in Wonderland", "Alice", "petite fille"),
    ("Peter Pan", "Peter Pan", "Peter Pan", "garçon volant"),
    ("La Belle et le Clochard", "Lady and the Tramp", "Lady", "chienne"),
    ("La Belle au Bois Dormant", "Sleeping Beauty", "Aurore", "princesse"),
    ("Les 101 Dalmatiens", "101 Dalmatians", "Pongo", "dalmatien"),
    ("Merlin l'Enchanteur", "The Sword in the Stone", "Arthur", "jeune garçon"),
    ("Le Livre de la Jungle", "The Jungle Book", "Mowgli", "petit d'homme"),
    ("Les Aristochats", "The Aristocats", "Duchesse", "chatte"),
    ("Robin des Bois", "Robin Hood", "Robin", "renard"),
    ("Bernard et Bianca", "The Rescuers", "Bernard", "souris"),
    ("Rox et Rouky", "The Fox and the Hound", "Rox", "renard"),
    ("Basil, Détective Privé", "The Great Mouse Detective", "Basil", "souris détective"),
    ("Oliver et Compagnie", "Oliver & Company", "Oliver", "chaton"),
    ("La Petite Sirène", "The Little Mermaid", "Ariel", "sirène"),
]

for film_fr, film_en, character, char_type in films_extended:
    disney_questions.extend(generate_character_questions(film_fr, character, char_type, 2))

print(f"Current count: {len(disney_questions)} questions")

# Generate questions about voice actors and production
production_questions = [
    ("Qui a fondé les studios Disney ?", ["Walt Disney", "Roy Disney", "Bob Iger", "Michael Eisner"], "Walt Disney", 1),
    ("En quelle année Walt Disney a-t-il créé Mickey Mouse ?", ["1928", "1930", "1925", "1932"], "1928", 2),
    ("Quel était le premier film d'animation Disney en couleur ?", ["Blanche-Neige", "Steamboat Willie", "Fantasia", "Pinocchio"], "Blanche-Neige", 2),
    ("Quel compositeur a travaillé sur 'La Petite Sirène' et 'Aladdin' ?", ["Alan Menken", "Phil Collins", "Elton John", "Hans Zimmer"], "Alan Menken", 3),
    ("Qui a composé la musique du 'Roi Lion' ?", ["Elton John et Hans Zimmer", "Alan Menken", "Phil Collins", "Randy Newman"], "Elton John et Hans Zimmer", 2),
    ("Quel compositeur a créé la musique de 'Tarzan' ?", ["Phil Collins", "Elton John", "Alan Menken", "Hans Zimmer"], "Phil Collins", 2),
    ("Qui a doublé le Génie dans la version originale d''Aladdin' ?", ["Robin Williams", "Jim Carrey", "Eddie Murphy", "Will Smith"], "Robin Williams", 2),
    ("Dans quel parc se trouve le château de la Belle au Bois Dormant ?", ["Disneyland Paris", "Walt Disney World", "Tokyo Disney", "Hong Kong Disney"], "Disneyland Paris", 2),
    ("Quel est le surnom de l'âge d'or de Disney (1989-1999) ?", ["Renaissance Disney", "Âge d'or", "Nouvelle ère", "Époque classique"], "Renaissance Disney", 3),
    ("Combien de films font partie des 'Classiques d'animation Disney' ?", ["Plus de 60", "30", "50", "100"], "Plus de 60", 2),
]

for q, opts, ans, diff in production_questions:
    disney_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Save progress and continue
print(f"Generated {len(disney_questions)} questions. Continuing...")

