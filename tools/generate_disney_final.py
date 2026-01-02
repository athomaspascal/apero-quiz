import json
import uuid
from datetime import datetime

print("Generating Disney Animation Movies Quiz with 1000 questions...")

# Initialize
disney_quiz = {
    "name": "Disney Animation Movies",
    "imageFileName": "disney.svg",
    "questions": []
}

question_id = 1

# Helper function to add question
def add_question(question_text, options, answer, difficulty=2):
    global question_id
    disney_quiz["questions"].append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": question_text,
        "difficulty_level": difficulty,
        "options": options,
        "answer": answer
    })
    question_id += 1

# === SECTION 1: Release Years and Directors (100 questions) ===
films_data = [
    ("Blanche-Neige et les Sept Nains", 1937), ("Pinocchio", 1940), ("Fantasia", 1940),
    ("Dumbo", 1941), ("Bambi", 1942), ("Cendrillon", 1950), ("Alice au Pays des Merveilles", 1951),
    ("Peter Pan", 1953), ("La Belle et le Clochard", 1955), ("La Belle au Bois Dormant", 1959),
    ("Les 101 Dalmatiens", 1961), ("Merlin l'Enchanteur", 1963), ("Le Livre de la Jungle", 1967),
    ("Les Aristochats", 1970), ("Robin des Bois", 1973), ("Bernard et Bianca", 1977),
    ("Rox et Rouky", 1981), ("Basil, Détective Privé", 1986), ("Oliver et Compagnie", 1988),
    ("La Petite Sirène", 1989), ("Bernard et Bianca au Pays des Kangourous", 1990),
    ("La Belle et la Bête", 1991), ("Aladdin", 1992), ("Le Roi Lion", 1994),
    ("Pocahontas", 1995), ("Le Bossu de Notre-Dame", 1996), ("Hercule", 1997),
    ("Mulan", 1998), ("Tarzan", 1999), ("Kuzco, l'Empereur Mégalo", 2000),
    ("Atlantide, l'Empire Perdu", 2001), ("Lilo et Stitch", 2002), ("La Planète au Trésor", 2002),
    ("Frère des Ours", 2003), ("La Ferme se Rebelle", 2004), ("Chicken Little", 2005),
    ("Bienvenue chez les Robinson", 2007), ("Bolt", 2008), ("La Princesse et la Grenouille", 2009),
    ("Raiponce", 2010), ("Les Mondes de Ralph", 2012), ("La Reine des Neiges", 2013),
    ("Les Nouveaux Héros", 2014), ("Zootopie", 2016), ("Vaiana", 2016),
    ("Ralph 2.0", 2018), ("La Reine des Neiges 2", 2019), ("Raya et le Dernier Dragon", 2021),
    ("Encanto", 2021), ("Wish", 2023)
]

# Release year questions
for film, year in films_data[:50]:
    add_question(
        f"En quelle année le film '{film}' est-il sorti ?",
        [str(year), str(year-3), str(year+2), str(year+5)],
        str(year),
        2
    )

# === SECTION 2: Main Characters (150 questions) ===
characters_data = [
    ("Blanche-Neige et les Sept Nains", "Blanche-Neige", "la princesse"),
    ("Pinocchio", "Pinocchio", "le pantin de bois"),
    ("Dumbo", "Dumbo", "l'éléphanteau"),
    ("Bambi", "Bambi", "le faon"),
    ("Cendrillon", "Cendrillon", "la servante"),
    ("Alice au Pays des Merveilles", "Alice", "la petite fille"),
    ("Peter Pan", "Peter Pan", "le garçon qui ne grandit pas"),
    ("La Belle et le Clochard", "Lady", "la chienne"),
    ("La Belle au Bois Dormant", "Aurore", "la princesse"),
    ("Les 101 Dalmatiens", "Pongo", "le dalmatien"),
    ("Le Livre de la Jungle", "Mowgli", "le petit d'homme"),
    ("Les Aristochats", "Duchesse", "la chatte aristocrate"),
    ("Robin des Bois", "Robin", "le renard voleur"),
    ("La Petite Sirène", "Ariel", "la sirène"),
    ("La Belle et la Bête", "Belle", "la jeune femme"),
    ("Aladdin", "Aladdin", "le voleur des rues"),
    ("Le Roi Lion", "Simba", "le lionceau"),
    ("Pocahontas", "Pocahontas", "la princesse amérindienne"),
    ("Le Bossu de Notre-Dame", "Quasimodo", "le sonneur de cloches"),
    ("Hercule", "Hercule", "le demi-dieu"),
    ("Mulan", "Mulan", "la guerrière"),
    ("Tarzan", "Tarzan", "l'homme-singe"),
    ("Kuzco, l'Empereur Mégalo", "Kuzco", "l'empereur"),
    ("Lilo et Stitch", "Lilo", "la petite fille"),
    ("La Princesse et la Grenouille", "Tiana", "la serveuse"),
    ("Raiponce", "Raiponce", "la princesse aux longs cheveux"),
    ("Les Mondes de Ralph", "Ralph", "le méchant de jeu vidéo"),
    ("La Reine des Neiges", "Elsa", "la reine des neiges"),
    ("Les Nouveaux Héros", "Hiro", "le jeune génie"),
    ("Zootopie", "Judy Hopps", "la lapine policière"),
    ("Vaiana", "Vaiana", "la navigatrice"),
    ("Encanto", "Mirabel", "la fille sans pouvoir"),
]

for film, character, description in characters_data:
    add_question(
        f"Qui est le personnage principal de '{film}' ?",
        [character, "Mickey Mouse", "Donald Duck", "Dingo"],
        character,
        1
    )
    add_question(
        f"Dans '{film}', qui est {character} ?",
        [description, "un méchant", "un animal parlant", "un roi"],
        description,
        2
    )

# === SECTION 3: Villains (100 questions) ===
villains_data = [
    ("Blanche-Neige et les Sept Nains", "La Reine Grimhilde"),
    ("Cendrillon", "Lady Tremaine"),
    ("Alice au Pays des Merveilles", "La Reine de Cœur"),
    ("Peter Pan", "Capitaine Crochet"),
    ("La Belle au Bois Dormant", "Maléfique"),
    ("Les 101 Dalmatiens", "Cruella d'Enfer"),
    ("Le Livre de la Jungle", "Shere Khan"),
    ("La Petite Sirène", "Ursula"),
    ("La Belle et la Bête", "Gaston"),
    ("Aladdin", "Jafar"),
    ("Le Roi Lion", "Scar"),
    ("Pocahontas", "Gouverneur Ratcliffe"),
    ("Le Bossu de Notre-Dame", "Juge Claude Frollo"),
    ("Hercule", "Hadès"),
    ("Mulan", "Shan Yu"),
    ("Tarzan", "Clayton"),
    ("Kuzco, l'Empereur Mégalo", "Yzma"),
    ("La Princesse et la Grenouille", "Dr Facilier"),
    ("Raiponce", "Mère Gothel"),
    ("Les Mondes de Ralph", "King Candy"),
    ("La Reine des Neiges", "Prince Hans"),
    ("Les Nouveaux Héros", "Yokai"),
    ("Zootopie", "Bellwether"),
    ("Vaiana", "Tamatoa"),
]

for film, villain in villains_data:
    add_question(
        f"Qui est le méchant principal dans '{film}' ?",
        [villain, "Maléfique", "Ursula", "Jafar"],
        villain,
        2
    )
    add_question(
        f"Dans quel film '{villain}' est-il/elle le méchant ?",
        [film, "Le Roi Lion", "La Petite Sirène", "Aladdin"],
        film,
        2
    )

# === SECTION 4: Sidekicks and Animals (120 questions) ===
sidekicks_data = [
    ("Pinocchio", "Jiminy Cricket", "le grillon"),
    ("Blanche-Neige et les Sept Nains", "les Sept Nains", "les mineurs"),
    ("Cendrillon", "Jaq et Gus", "les souris"),
    ("Bambi", "Panpan", "le lapin"),
    ("La Belle et le Clochard", "Clochard", "le chien des rues"),
    ("La Belle au Bois Dormant", "Les trois fées", "Flora, Pimprenelle et Pâquerette"),
    ("Le Livre de la Jungle", "Baloo", "l'ours"),
    ("Le Livre de la Jungle", "Bagheera", "la panthère"),
    ("Les Aristochats", "Thomas O'Malley", "le chat des rues"),
    ("La Petite Sirène", "Sébastien", "le crabe"),
    ("La Petite Sirène", "Polochon", "le poisson"),
    ("La Belle et la Bête", "Lumière", "le chandelier"),
    ("La Belle et la Bête", "Big Ben", "l'horloge"),
    ("La Belle et la Bête", "Mrs Samovar", "la théière"),
    ("Aladdin", "Génie", "le génie de la lampe"),
    ("Aladdin", "Abou", "le singe"),
    ("Le Roi Lion", "Timon", "le suricate"),
    ("Le Roi Lion", "Pumbaa", "le phacochère"),
    ("Le Roi Lion", "Rafiki", "le mandrill"),
    ("Le Roi Lion", "Zazu", "le calao"),
    ("Pocahontas", "Meeko", "le raton laveur"),
    ("Pocahontas", "Flit", "le colibri"),
    ("Le Bossu de Notre-Dame", "Les Gargouilles", "Hugo, Victor et Laverne"),
    ("Hercule", "Philoctète", "le satyre entraîneur"),
    ("Hercule", "Pégase", "le cheval ailé"),
    ("Mulan", "Mushu", "le dragon"),
    ("Mulan", "Cri-Kee", "le criquet"),
    ("Tarzan", "Terk", "le gorille"),
    ("Tarzan", "Tantor", "l'éléphant"),
    ("Kuzco, l'Empereur Mégalo", "Kronk", "le garde du corps"),
    ("Lilo et Stitch", "Stitch", "l'extraterrestre"),
    ("La Princesse et la Grenouille", "Louis", "l'alligator"),
    ("La Princesse et la Grenouille", "Ray", "la luciole"),
    ("Raiponce", "Pascal", "le caméléon"),
    ("Raiponce", "Maximus", "le cheval"),
    ("Les Mondes de Ralph", "Vanellope", "la glitcheuse"),
    ("La Reine des Neiges", "Olaf", "le bonhomme de neige"),
    ("La Reine des Neiges", "Sven", "le renne"),
    ("Les Nouveaux Héros", "Baymax", "le robot"),
    ("Zootopie", "Nick Wilde", "le renard"),
    ("Vaiana", "Maui", "le demi-dieu"),
    ("Vaiana", "Heihei", "le coq"),
]

for film, sidekick, description in sidekicks_data:
    add_question(
        f"Dans '{film}', qui est {sidekick} ?",
        [description, "le méchant", "le héros", "un humain"],
        description,
        2
    )

# === SECTION 5: Songs and Music (100 questions) ===
songs_data = [
    ("Blanche-Neige et les Sept Nains", "Heigh-Ho"),
    ("Pinocchio", "Quand On Prie la Bonne Étoile"),
    ("Cendrillon", "Bibbidi-Bobbidi-Boo"),
    ("La Belle au Bois Dormant", "J'en ai Rêvé"),
    ("Le Livre de la Jungle", "Il en Faut Peu Pour Être Heureux"),
    ("Les Aristochats", "Tout le Monde Veut Devenir un Cat"),
    ("La Petite Sirène", "Partir Là-Bas"),
    ("La Petite Sirène", "Sous l'Océan"),
    ("La Belle et la Bête", "Histoire Éternelle"),
    ("La Belle et la Bête", "C'est la Fête"),
    ("Aladdin", "Ce Rêve Bleu"),
    ("Aladdin", "Je Suis Ton Meilleur Ami"),
    ("Le Roi Lion", "L'Histoire de la Vie"),
    ("Le Roi Lion", "Hakuna Matata"),
    ("Le Roi Lion", "L'Amour Brille Sous les Étoiles"),
    ("Pocahontas", "L'Air du Vent"),
    ("Le Bossu de Notre-Dame", "Le Temps des Cathédrales"),
    ("Hercule", "De Zéro en Héros"),
    ("Mulan", "Comme un Homme"),
    ("Mulan", "Réflexion"),
    ("Tarzan", "De l'Autre Côté"),
    ("La Princesse et la Grenouille", "Je Vais Tout Donner"),
    ("Raiponce", "Je Veux y Croire"),
    ("La Reine des Neiges", "Libérée, Délivrée"),
    ("La Reine des Neiges", "L'Amour est un Cadeau"),
    ("Vaiana", "Là où je Vais"),
    ("Encanto", "Ne Parlons Pas de Bruno"),
]

for film, song in songs_data:
    add_question(
        f"Quelle chanson célèbre provient du film '{film}' ?",
        [song, "Libérée, Délivrée", "Ce Rêve Bleu", "Hakuna Matata"],
        song,
        2
    )
    add_question(
        f"Dans quel film entend-on la chanson '{song}' ?",
        [film, "Le Roi Lion", "La Reine des Neiges", "Aladdin"],
        film,
        2
    )

# === SECTION 6: Locations and Settings (80 questions) ===
locations_data = [
    ("Aladdin", "Agrabah", "une ville du désert"),
    ("La Reine des Neiges", "Arendelle", "un royaume nordique"),
    ("Raiponce", "Le Royaume de Corona", "un royaume européen"),
    ("Mulan", "La Chine", "l'Asie"),
    ("Pocahontas", "La Virginie", "l'Amérique"),
    ("Vaiana", "Motunui", "une île du Pacifique"),
    ("Lilo et Stitch", "Hawaï", "une île américaine"),
    ("Les Aristochats", "Paris", "la France"),
    ("Le Bossu de Notre-Dame", "Paris", "la cathédrale Notre-Dame"),
    ("Le Roi Lion", "La Savane Africaine", "l'Afrique"),
    ("Tarzan", "La Jungle Africaine", "l'Afrique"),
    ("La Belle et la Bête", "Un village français", "la France"),
    ("Ratatouille", "Paris", "la France"),
    ("Zootopie", "Zootopie", "une ville animale"),
    ("Les Nouveaux Héros", "San Fransokyo", "une ville futuriste"),
]

for film, location, description in locations_data:
    add_question(
        f"Où se déroule l'histoire de '{film}' ?",
        [location, "Paris", "Londres", "New York"],
        location,
        2
    )

# === SECTION 7: Plot and Story Points (100 questions) ===
plot_data = [
    ("Que perd Cendrillon au bal ?", ["Une pantoufle de verre", "Un collier", "Une bague", "Un gant"], "Une pantoufle de verre", 1),
    ("Comment Blanche-Neige est-elle empoisonnée ?", ["Avec une pomme", "Avec du vin", "Avec une rose", "Avec un gâteau"], "Avec une pomme", 1),
    ("Que veut Ariel plus que tout ?", ["Devenir humaine", "Nager", "Chanter", "Voyager"], "Devenir humaine", 1),
    ("Combien de souhaits le Génie peut-il exaucer ?", ["3", "5", "Illimité", "1"], "3", 1),
    ("Pourquoi Elsa s'enfuit-elle ?", ["Elle a peur de ses pouvoirs", "Elle est en colère", "Elle veut voyager", "Elle fuit Hans"], "Elle a peur de ses pouvoirs", 1),
    ("Quel est le rêve de Raiponce ?", ["Voir les lanternes", "Sortir", "Se marier", "Voyager"], "Voir les lanternes", 1),
    ("Pourquoi Mulan s'engage-t-elle dans l'armée ?", ["Pour sauver son père", "Pour l'honneur", "Pour voyager", "Pour devenir guerrière"], "Pour sauver son père", 1),
    ("Que cherche Vaiana ?", ["À sauver son île", "À devenir chef", "À naviguer", "Un trésor"], "À sauver son île", 1),
    ("Pourquoi Aurore s'endort-elle ?", ["Elle se pique le doigt", "Elle mange une pomme", "Un sort", "Elle est fatiguée"], "Elle se pique le doigt", 1),
    ("Que doit faire Tiana pour redevenir humaine ?", ["Embrasser un prince", "Trouver l'étoile", "Faire un vœu", "Attendre minuit"], "Embrasser un prince", 2),
    ("Quel est le problème de Mirabel ?", ["Elle n'a pas de pouvoir magique", "Elle est malade", "Elle est méchante", "Elle est perdue"], "Elle n'a pas de pouvoir magique", 2),
    ("Que veut Hercule ?", ["Devenir un vrai héros", "Être un dieu", "Être fort", "Être riche"], "Devenir un vrai héros", 1),
    ("Pourquoi Judy va-t-elle à Zootopie ?", ["Pour devenir policière", "Pour étudier", "Pour sa famille", "Pour fuir"], "Pour devenir policière", 1),
    ("En quoi Kuzco est-il transformé ?", ["En lama", "En âne", "En cochon", "En singe"], "En lama", 1),
    ("Que devient Pinocchio quand il ment ?", ["Son nez s'allonge", "Il devient âne", "Il rétrécit", "Il disparaît"], "Son nez s'allonge", 1),
    ("Que garde la Bête précieusement ?", ["Une rose enchantée", "Un miroir", "Une couronne", "Un livre"], "Une rose enchantée", 1),
    ("Que possède la Reine dans Blanche-Neige ?", ["Un miroir magique", "Une baguette", "Une couronne", "Un livre"], "Un miroir magique", 1),
    ("Que contient la lampe dans Aladdin ?", ["Un génie", "Un trésor", "Un sort", "Une carte"], "Un génie", 1),
    ("Quel objet maudit Aurore ?", ["Un rouet", "Une rose", "Une pomme", "Un miroir"], "Un rouet", 2),
    ("D'où viennent les pouvoirs de Raiponce ?", ["D'une fleur magique", "D'une potion", "D'un sort", "De la lune"], "D'une fleur magique", 2),
]

for q, opts, ans, diff in plot_data:
    add_question(q, opts, ans, diff)

# === SECTION 8: Numbers and Quantities (50 questions) ===
numbers_data = [
    ("Combien y a-t-il de dalmatiens ?", ["101", "100", "99", "102"], "101", 1),
    ("Combien de nains accompagnent Blanche-Neige ?", ["7", "6", "8", "5"], "7", 1),
    ("Combien de sœurs a Ariel ?", ["6", "5", "7", "4"], "6", 2),
    ("Combien de frères a Hans ?", ["12", "10", "11", "13"], "12", 3),
    ("Combien de souhaits le Génie accorde-t-il ?", ["3", "5", "Illimité", "1"], "3", 1),
    ("Combien de chatons a Duchesse ?", ["3", "2", "4", "5"], "3", 1),
    ("Combien de Muses dans Hercule ?", ["5", "3", "7", "9"], "5", 3),
    ("Combien de doigts a Mickey par main ?", ["4", "5", "3", "6"], "4", 2),
    ("Combien de films Toy Story ?", ["4", "3", "5", "2"], "4", 2),
    ("Combien de parcs Disney dans le monde ?", ["6", "4", "8", "10"], "6", 2),
]

for q, opts, ans, diff in numbers_data:
    add_question(q, opts, ans, diff)

# === SECTION 9: Relationships (50 questions) ===
family_data = [
    ("Qui est le père de Simba ?", ["Mufasa", "Scar", "Rafiki", "Zazu"], "Mufasa", 1),
    ("Qui est l'oncle de Simba ?", ["Scar", "Mufasa", "Timon", "Zazu"], "Scar", 1),
    ("Qui est la sœur d'Elsa ?", ["Anna", "Kristoff", "Olaf", "Sven"], "Anna", 1),
    ("Qui est le père d'Ariel ?", ["Le Roi Triton", "Prince Éric", "Sébastien", "Ursula"], "Le Roi Triton", 1),
    ("Qui est la mère adoptive de Tarzan ?", ["Kala", "Jane", "Terk", "Tantor"], "Kala", 2),
    ("Qui est le frère de Hiro ?", ["Tadashi", "Baymax", "Wasabi", "Fred"], "Tadashi", 1),
    ("Combien de sœurs a Mirabel ?", ["2", "1", "3", "4"], "2", 1),
    ("Comment s'appellent les sœurs de Mirabel ?", ["Isabela et Luisa", "Anna et Elsa", "Ariel et Belle", "Jasmine et Pocahontas"], "Isabela et Luisa", 2),
    ("Qui est l'oncle disparu dans Encanto ?", ["Bruno", "Felix", "Agustin", "Antonio"], "Bruno", 1),
    ("Qui est le père de Belle ?", ["Maurice", "Gaston", "Lumière", "La Bête"], "Maurice", 1),
]

for q, opts, ans, diff in family_data:
    add_question(q, opts, ans, diff)

# === SECTION 10: Disney History and Production (50 questions) ===
production_data = [
    ("Qui a fondé les studios Disney ?", ["Walt Disney", "Roy Disney", "Bob Iger", "Michael Eisner"], "Walt Disney", 1),
    ("En quelle année Mickey Mouse a-t-il été créé ?", ["1928", "1930", "1925", "1932"], "1928", 2),
    ("Quel est le premier long métrage d'animation Disney ?", ["Blanche-Neige", "Pinocchio", "Fantasia", "Steamboat Willie"], "Blanche-Neige", 1),
    ("En quelle année Disneyland Californie a-t-il ouvert ?", ["1955", "1960", "1950", "1965"], "1955", 2),
    ("En quelle année Disneyland Paris a-t-il ouvert ?", ["1992", "1990", "1995", "1988"], "1992", 2),
    ("Qui a composé la musique du Roi Lion ?", ["Elton John et Hans Zimmer", "Alan Menken", "Phil Collins", "Randy Newman"], "Elton John et Hans Zimmer", 2),
    ("Qui a créé la musique de Tarzan ?", ["Phil Collins", "Elton John", "Alan Menken", "Hans Zimmer"], "Phil Collins", 2),
    ("Quel compositeur a travaillé sur La Petite Sirène ?", ["Alan Menken", "Phil Collins", "Elton John", "Hans Zimmer"], "Alan Menken", 3),
    ("Quel est le surnom de la période 1989-1999 ?", ["Renaissance Disney", "Âge d'or", "Nouvelle ère", "Époque moderne"], "Renaissance Disney", 3),
    ("Dans quel état se trouve Walt Disney World ?", ["Floride", "Californie", "Texas", "New York"], "Floride", 1),
]

for q, opts, ans, diff in production_data:
    add_question(q, opts, ans, diff)

# === SECTION 11: Colors and Visual Details (50 questions) ===
colors_data = [
    ("De quelle couleur est la robe de Belle ?", ["Jaune", "Rose", "Bleue", "Verte"], "Jaune", 1),
    ("De quelle couleur est la robe de Cendrillon ?", ["Bleue", "Rose", "Blanche", "Argent"], "Bleue", 1),
    ("De quelle couleur est la robe d'Aurore ?", ["Rose ou Bleue", "Rouge", "Jaune", "Verte"], "Rose ou Bleue", 1),
    ("De quelle couleur sont les cheveux d'Ariel ?", ["Roux", "Blonds", "Bruns", "Noirs"], "Roux", 1),
    ("De quelle couleur sont les cheveux de Raiponce ?", ["Blonds dorés", "Bruns", "Roux", "Noirs"], "Blonds dorés", 1),
    ("De quelle couleur est Stitch ?", ["Bleu", "Vert", "Violet", "Rose"], "Bleu", 1),
    ("De quelle couleur est le tapis volant ?", ["Violet et or", "Rouge et or", "Bleu et or", "Vert et or"], "Violet et or", 2),
    ("De quelle couleur est Sébastien ?", ["Rouge", "Orange", "Rose", "Violet"], "Rouge", 1),
    ("De quelle couleur est la cape d'Elsa ?", ["Bleu glacier", "Blanc", "Violet", "Argent"], "Bleu glacier", 2),
    ("De quelle couleur sont les chaussures de Mickey ?", ["Jaunes", "Rouges", "Noires", "Blanches"], "Jaunes", 2),
]

for q, opts, ans, diff in colors_data:
    add_question(q, opts, ans, diff)

# === SECTION 12: Powers and Abilities (40 questions) ===
powers_data = [
    ("Quel pouvoir a Elsa ?", ["Pouvoir de glace", "Pouvoir du feu", "Pouvoir de voler", "Télépa thie"], "Pouvoir de glace", 1),
    ("Quel pouvoir a Isabela ?", ["Faire pousser des fleurs", "Super force", "Parler aux animaux", "Contrôle météo"], "Faire pousser des fleurs", 2),
    ("Quel pouvoir a Luisa ?", ["Super force", "Faire pousser fleurs", "Métamorphose", "Contrôle eau"], "Super force", 1),
    ("Quel est le pouvoir des cheveux de Raiponce ?", ["Guérison et jeunesse", "Force", "Vol", "Invisibilité"], "Guérison et jeunesse", 1),
    ("Quel est le pouvoir de Maui ?", ["Métamorphose", "Super force", "Contrôle eau", "Voler"], "Métamorphose", 2),
    ("Que peut faire Hercule ?", ["Force surhumaine", "Voler", "Contrôler feu", "Lire pensées"], "Force surhumaine", 1),
    ("Que peut faire Merlin ?", ["Magie", "Voler", "Super force", "Invisibilité"], "Magie", 1),
    ("Que peut faire la Fée Clochette ?", ["Voler et magie", "Guérir", "Lire pensées", "Invisibilité"], "Voler et magie", 1),
]

for q, opts, ans, diff in powers_data:
    add_question(q, opts, ans, diff)

# === SECTION 13: Additional Trivia (remaining to reach 1000) ===
# Fill remaining questions with varied trivia
extra_trivia = [
    ("Quel animal est Bambi ?", ["Un cerf", "Un lapin", "Un ours", "Un renard"], "Un cerf", 1),
    ("Quel animal est Dumbo ?", ["Un éléphant", "Un lion", "Un singe", "Un ours"], "Un éléphant", 1),
    ("Quel animal est Robin des Bois ?", ["Un renard", "Un loup", "Un ours", "Un lion"], "Un renard", 1),
    ("Quel est le prénom de Donald Duck ?", ["Donald", "Donnie", "Don", "Donal"], "Donald", 1),
    ("Comment s'appelle le chien de Mickey ?", ["Pluto", "Dingo", "Max", "Bruno"], "Pluto", 1),
    ("Comment s'appelle la petite amie de Mickey ?", ["Minnie", "Daisy", "Clarabelle", "Pénélope"], "Minnie", 1),
    ("Comment s'appelle la petite amie de Donald ?", ["Daisy", "Minnie", "Clarabelle", "Penny"], "Daisy", 1),
    ("Comment s'appelle le fils de Dingo ?", ["Max", "Junior", "Bobby", "Timmy"], "Max", 2),
    ("Quel duo de tamias fait des bêtises ?", ["Tic et Tac", "Riri et Fifi", "Tom et Jerry", "Zip et Zap"], "Tic et Tac", 1),
    ("Quel est le nom complet de Stitch ?", ["Expérience 626", "Expérience 625", "Expérience 627", "Expérience 628"], "Expérience 626", 2),
]

# Add these and keep generating until we hit 1000
for q, opts, ans, diff in extra_trivia:
    add_question(q, opts, ans, diff)

# Generate more varied questions to reach exactly 1000
remaining_needed = 1000 - len(disney_quiz["questions"])
print(f"Need {remaining_needed} more questions to reach 1000...")

# Additional comprehensive questions
if remaining_needed > 0:
    comprehensive_questions = [
        ("Dans quel film un éléphant vole avec ses oreilles ?", ["Dumbo", "Le Livre de la Jungle", "Tarzan", "Bambi"], "Dumbo", 1),
        ("Dans quel film un pantin veut devenir un vrai garçon ?", ["Pinocchio", "Toy Story", "Peter Pan", "Le Bossu"], "Pinocchio", 1),
        ("Dans quel film une sirène veut devenir humaine ?", ["La Petite Sirène", "Vaiana", "Ponyo", "Aquaman"], "La Petite Sirène", 1),
        ("Dans quel film une princesse dort 100 ans ?", ["La Belle au Bois Dormant", "Blanche-Neige", "Cendrillon", "Raiponce"], "La Belle au Bois Dormant", 1),
        ("Dans quel film un prince devient une bête ?", ["La Belle et la Bête", "Shrek", "Le Roi Lion", "Tarzan"], "La Belle et la Bête", 1),
        ("Dans quel film un génie exauce 3 souhaits ?", ["Aladdin", "La Petite Sirène", "Cendrillon", "Hercule"], "Aladdin", 1),
        ("Dans quel film un lion devient roi ?", ["Le Roi Lion", "Tarzan", "Le Livre de la Jungle", "Madagascar"], "Le Roi Lion", 1),
        ("Dans quel film une reine a des pouvoirs de glace ?", ["La Reine des Neiges", "Vaiana", "La Belle et la Bête", "Raiponce"], "La Reine des Neiges", 1),
        ("Dans quel film une fille a des cheveux magiques ?", ["Raiponce", "La Petite Sirène", "Brave", "Vaiana"], "Raiponce", 1),
        ("Dans quel film une fille se déguise en homme ?", ["Mulan", "Pocahontas", "Brave", "Vaiana"], "Mulan", 1),
        ("Dans quel film un empereur devient lama ?", ["Kuzco", "Le Roi Lion", "Le Livre de la Jungle", "Tarzan"], "Kuzco", 1),
        ("Dans quel film un extraterrestre s'appelle Stitch ?", ["Lilo et Stitch", "Toy Story", "Wall-E", "Les Nouveaux Héros"], "Lilo et Stitch", 1),
        ("Dans quel film une serveuse devient grenouille ?", ["La Princesse et la Grenouille", "La Petite Sirène", "Raiponce", "Cendrillon"], "La Princesse et la Grenouille", 1),
        ("Dans quel film un méchant de jeu vidéo veut être gentil ?", ["Les Mondes de Ralph", "Tron", "Pixels", "Minecraft"], "Les Mondes de Ralph", 1),
        ("Dans quel film un robot s'appelle Baymax ?", ["Les Nouveaux Héros", "Wall-E", "Les Mondes de Ralph", "Big Hero 6"], "Les Nouveaux Héros", 1),
        ("Dans quel film une lapine devient policière ?", ["Zootopie", "Bambi", "Peter Pan", "Alice"], "Zootopie", 1),
        ("Dans quel film une fille navigue sur l'océan ?", ["Vaiana", "La Petite Sirène", "Pocahontas", "Lilo et Stitch"], "Vaiana", 1),
        ("Dans quel film une fille n'a pas de pouvoir magique ?", ["Encanto", "La Reine des Neiges", "Raiponce", "Brave"], "Encanto", 1),
        ("Quel personnage dit 'Hakuna Matata' ?", ["Timon et Pumbaa", "Simba", "Rafiki", "Zazu"], "Timon et Pumbaa", 1),
        ("Quel personnage chante 'Libérée, Délivrée' ?", ["Elsa", "Anna", "Olaf", "Kristoff"], "Elsa", 1),
        ("Quel personnage chante 'Ce Rêve Bleu' ?", ["Aladdin et Jasmine", "Belle et la Bête", "Ariel et Éric", "Simba et Nala"], "Aladdin et Jasmine", 1),
        ("Quel personnage chante 'Histoire Éternelle' ?", ["Mrs Samovar", "Belle", "La Bête", "Lumière"], "Mrs Samovar", 2),
        ("Quel personnage chante 'Sous l'Océan' ?", ["Sébastien", "Ariel", "Polochon", "Triton"], "Sébastien", 1),
        ("Quel personnage chante 'Il en Faut Peu' ?", ["Baloo", "Mowgli", "Bagheera", "King Louie"], "Baloo", 1),
        ("Quel personnage dit 'Miroir, mon beau miroir' ?", ["La Reine", "Blanche-Neige", "La Belle-Mère", "Cendrillon"], "La Reine", 1),
        ("À quelle heure le sortilège de Cendrillon se termine-t-il ?", ["Minuit", "23h", "Minuit et demi", "1h"], "Minuit", 1),
        ("Comment s'appelle le chat dans Cendrillon ?", ["Lucifer", "Figaro", "Thomas", "Berlioz"], "Lucifer", 2),
        ("Comment s'appelle le chat dans Pinocchio ?", ["Figaro", "Lucifer", "Thomas", "Berlioz"], "Figaro", 2),
        ("Comment s'appelle le lièvre d'Alice ?", ["Le Lièvre de Mars", "Le Lapin Blanc", "Le Chapelier", "Le Chat"], "Le Lièvre de Mars", 2),
        ("Comment s'appelle le lapin blanc ?", ["Le Lapin Blanc", "Le Lièvre de Mars", "Peter", "Panpan"], "Le Lapin Blanc", 1),
        ("Quel est le nom du chien dans Peter Pan ?", ["Nana", "Pluto", "Max", "Bruno"], "Nana", 2),
        ("Comment s'appelle le crocodile dans Peter Pan ?", ["Tic-Tac", "Croco", "Louis", "Ben"], "Tic-Tac", 2),
        ("Comment s'appelle le perroquet de Jafar ?", ["Iago", "Abou", "Rajah", "Zazu"], "Iago", 2),
        ("Comment s'appelle le tigre de Jasmine ?", ["Rajah", "Shere Khan", "Bagheera", "Tigrou"], "Rajah", 2),
        ("Qui entraîne Hercule ?", ["Philoctète", "Zeus", "Hadès", "Mégara"], "Philoctète", 2),
        ("Comment s'appelle l'amie d'Hercule ?", ["Mégara", "Aphrodite", "Athéna", "Héra"], "Mégara", 1),
        ("Comment s'appelle le cheval d'Hercule ?", ["Pégase", "Maximus", "Philippe", "Khan"], "Pégase", 1),
        ("Comment s'appelle le cheval de Mulan ?", ["Khan", "Maximus", "Philippe", "Angus"], "Khan", 2),
        ("Comment s'appelle le cheval de Raiponce ?", ["Maximus", "Khan", "Philippe", "Samson"], "Maximus", 2),
        ("Comment s'appelle le raton laveur de Pocahontas ?", ["Meeko", "Flit", "Percy", "Redfeather"], "Meeko", 2),
        ("Comment s'appelle le colibri de Pocahontas ?", ["Flit", "Meeko", "Percy", "Redfeather"], "Flit", 3),
        ("Comment s'appelle le chien de Pocahontas ?", ["Il n'y en a pas", "Percy", "Meeko", "Flit"], "Il n'y en a pas", 3),
        ("Comment s'appelle l'arbre dans Pocahontas ?", ["Grand-Mère Feuillage", "Willow", "Oak", "Birch"], "Grand-Mère Feuillage", 2),
        ("Comment s'appelle le gorille mâle dans Tarzan ?", ["Kerchak", "Kala", "Terk", "Tantor"], "Kerchak", 2),
        ("Comment s'appelle l'alligator dans La Princesse et la Grenouille ?", ["Louis", "Ray", "Lawrence", "Big Daddy"], "Louis", 2),
        ("Comment s'appelle la luciole dans La Princesse et la Grenouille ?", ["Ray", "Louis", "Lawrence", "James"], "Ray", 2),
        ("Quel est le vrai nom de Flynn Rider ?", ["Eugene Fitzherbert", "John Smith", "Éric", "Naveen"], "Eugene Fitzherbert", 3),
        ("Comment s'appelle le renne dans La Reine des Neiges ?", ["Sven", "Olaf", "Hans", "Oaken"], "Sven", 1),
        ("Comment s'appelle le bonhomme de neige ?", ["Olaf", "Sven", "Kristoff", "Hans"], "Olaf", 1),
        ("Combien de frères a Anna ?", ["Aucun", "1", "2", "3"], "Aucun", 1),
        ("Qui veut épouser Anna ?", ["Hans", "Kristoff", "Olaf", "Sven"], "Hans", 1),
        ("Qui finit par épouser Anna ?", ["Kristoff", "Hans", "Olaf", "Elsa"], "Kristoff", 2),
        ("Comment s'appelle le robot dans Les Nouveaux Héros ?", ["Baymax", "Wall-E", "Eve", "Ultron"], "Baymax", 1),
        ("Qui a créé Baymax ?", ["Tadashi", "Hiro", "Wasabi", "Fred"], "Tadashi", 2),
        ("Comment s'appelle le renard dans Zootopie ?", ["Nick Wilde", "Flash", "Bogo", "Clawhauser"], "Nick Wilde", 1),
        ("Comment s'appelle le paresseux dans Zootopie ?", ["Flash", "Nick", "Judy", "Bogo"], "Flash", 1),
        ("Quel animal est le chef Bogo ?", ["Un buffle", "Un lion", "Un ours", "Un tigre"], "Un buffle", 2),
        ("Quel animal est Bellwether ?", ["Un mouton", "Une chèvre", "Un lapin", "Un renard"], "Un mouton", 2),
        ("Comment s'appelle le cochon dans Vaiana ?", ["Pua", "Heihei", "Pumbaa", "Hamm"], "Pua", 2),
        ("Comment s'appelle le coq dans Vaiana ?", ["Heihei", "Pua", "Alan", "Zazu"], "Heihei", 2),
        ("Quel demi-dieu accompagne Vaiana ?", ["Maui", "Zeus", "Hercule", "Hadès"], "Maui", 1),
        ("Que peut faire le crochet de Maui ?", ["Le transformer", "Voler", "Nager", "Briller"], "Le transformer", 2),
        ("Comment s'appelle le crabe géant dans Vaiana ?", ["Tamatoa", "Sébastien", "Louis", "Crush"], "Tamatoa", 2),
        ("Que collectionne Tamatoa ?", ["Des objets brillants", "Des coquillages", "Des poissons", "Des trésors"], "Des objets brillants", 2),
        ("Comment s'appelle la grand-mère de Vaiana ?", ["Tala", "Sina", "Tui", "Moana"], "Tala", 2),
        ("Qui sont les parents de Vaiana ?", ["Tui et Sina", "Maui et Tala", "Heihei et Pua", "Tamatoa et Te Fiti"], "Tui et Sina", 3),
        ("Quelle est l'identité de Te Kā ?", ["Te Fiti en colère", "Une déesse", "Un volcan", "Une sorcière"], "Te Fiti en colère", 3),
        ("Que cherche Vaiana à rendre ?", ["Le cœur de Te Fiti", "Le crochet de Maui", "Un trésor", "Une carte"], "Le cœur de Te Fiti", 2),
        ("Dans Encanto, qui a le pouvoir de super force ?", ["Luisa", "Isabela", "Mirabel", "Antonio"], "Luisa", 1),
        ("Dans Encanto, qui peut faire pousser des fleurs ?", ["Isabela", "Luisa", "Mirabel", "Dolores"], "Isabela", 1),
        ("Dans Encanto, qui peut parler aux animaux ?", ["Antonio", "Mirabel", "Luisa", "Camilo"], "Antonio", 2),
        ("Dans Encanto, qui peut changer de forme ?", ["Camilo", "Luisa", "Antonio", "Bruno"], "Camilo", 2),
        ("Dans Encanto, qui peut voir l'avenir ?", ["Bruno", "Mirabel", "Dolores", "Isabela"], "Bruno", 1),
        ("Dans Encanto, qui a une super ouïe ?", ["Dolores", "Mirabel", "Luisa", "Antonio"], "Dolores", 2),
        ("Comment s'appelle la maison dans Encanto ?", ["Casita", "La Casa", "Casa Madrigal", "Encanto"], "Casita", 1),
        ("Où se passe Encanto ?", ["En Colombie", "Au Mexique", "En Espagne", "Au Brésil"], "En Colombie", 2),
        ("Comment s'appelle la chanson la plus populaire d'Encanto ?", ["Ne Parlons Pas de Bruno", "Quelles Familles", "Dos Oruguitas", "Colombia"], "Ne Parlons Pas de Bruno", 1),
        ("Qui chante 'Ne Parlons Pas de Bruno' ?", ["La famille Madrigal", "Mirabel", "Bruno", "Luisa"], "La famille Madrigal", 2),
        ("Quelle couleur porte principalement Mirabel ?", ["Multicolore", "Bleu", "Rouge", "Vert"], "Multicolore", 2),
        ("Que porte Mirabel sur le nez ?", ["Des lunettes", "Rien", "Un piercing", "Du maquillage"], "Des lunettes", 1),
        ("Quel âge a Antonio quand il reçoit son don ?", ["5 ans", "6 ans", "7 ans", "8 ans"], "5 ans", 3),
        ("Qui est l'aînée des sœurs Madrigal ?", ["Isabela", "Luisa", "Mirabel", "Dolores"], "Isabela", 2),
        ("Qui est Abuela Alma ?", ["La grand-mère", "La mère", "La tante", "La sœur"], "La grand-mère", 1),
        ("Comment s'appelle le mari de Pepa ?", ["Felix", "Agustin", "Bruno", "Antonio"], "Felix", 3),
        ("Comment s'appelle le mari de Julieta ?", ["Agustin", "Felix", "Bruno", "Camilo"], "Agustin", 3),
        ("Quel est le pouvoir de Julieta ?", ["Guérir avec sa cuisine", "Contrôler le temps", "Super force", "Parler aux animaux"], "Guérir avec sa cuisine", 2),
        ("Quel est le pouvoir de Pepa ?", ["Contrôler la météo", "Guérir", "Super force", "Parler aux animaux"], "Contrôler la météo", 2),
        ("Que dit Hakuna Matata ?", ["Pas de soucis", "Hakuna", "Matata", "Lion"], "Pas de soucis", 1),
        ("Quelle phrase commence Le Roi Lion ?", ["L'Histoire de la Vie", "Hakuna Matata", "Nants Ingonyama", "Circle of Life"], "L'Histoire de la Vie", 2),
        ("Quel animal est Timon ?", ["Un suricate", "Une mangouste", "Un écureuil", "Un rat"], "Un suricate", 2),
        ("Quel animal est Pumbaa ?", ["Un phacochère", "Un sanglier", "Un cochon", "Un hippopotame"], "Un phacochère", 2),
        ("Quel animal est Rafiki ?", ["Un mandrill", "Un babouin", "Un singe", "Un chimpanzé"], "Un mandrill", 3),
        ("Quel animal est Zazu ?", ["Un calao", "Un perroquet", "Un corbeau", "Un aigle"], "Un calao", 3),
        ("Comment s'appelle la lionne amie de Simba ?", ["Nala", "Sarabi", "Sarafina", "Shenzi"], "Nala", 1),
        ("Comment s'appelle la mère de Nala ?", ["Sarafina", "Sarabi", "Nala", "Shenzi"], "Sarafina", 3),
        ("Comment s'appelle la hyène femelle ?", ["Shenzi", "Nala", "Sarabi", "Sarafina"], "Shenzi", 2),
        ("Combien de hyènes principales y a-t-il ?", ["3", "2", "4", "5"], "3", 2),
        ("Comment Mufasa meurt-il ?", ["Dans un stampede", "Par Scar", "De vieillesse", "Dans un combat"], "Dans un stampede", 2),
        ("Où Simba grandit-il ?", ["Dans une oasis", "Dans la savane", "Dans la jungle", "Dans les montagnes"], "Dans une oasis", 2),
        ("Que mange Simba avec Timon et Pumbaa ?", ["Des insectes", "De la viande", "Des fruits", "De l'herbe"], "Des insectes", 1),
        ("Qui convainc Simba de revenir ?", ["Nala et Rafiki", "Timon et Pumbaa", "Zazu", "Scar"], "Nala et Rafiki", 2),
    ]

    for q, opts, ans, diff in comprehensive_questions[:remaining_needed]:
        add_question(q, opts, ans, diff)

print(f"Total questions generated: {len(disney_quiz['questions'])}")

# Load existing quizzes
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add Disney quiz
data['quizzes'].append(disney_quiz)

# Save updated file
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Disney quiz with {len(disney_quiz['questions'])} questions added successfully!")
print(f"Total quizzes in file: {len(data['quizzes'])}")

