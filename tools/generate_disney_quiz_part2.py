# Part 2 - Continue generating Disney quiz questions

import json
import uuid

# This will continue from part 1
# We'll generate additional questions to reach 1000 total

additional_questions = []
question_id_start = 400  # Starting from where part 1 left off

# More trivia questions about various Disney films
trivia_questions_data = [
    ("Quel est le premier film Pixar distribué par Disney ?", ["Toy Story", "Monstres et Cie", "Le Monde de Nemo", "Les Indestructibles"], "Toy Story", 2),
    ("Dans 'Bambi', comment s'appelle le meilleur ami lapin de Bambi ?", ["Panpan", "Fleur", "Faline", "Tambour"], "Panpan", 1),
    ("Dans 'Bambi', comment s'appelle la mouffette ?", ["Fleur", "Panpan", "Faline", "Ronron"], "Fleur", 2),
    ("Combien de frères a le Prince Hans dans 'La Reine des Neiges' ?", ["12", "10", "8", "15"], "12", 3),
    ("Dans 'Les Nouveaux Héros', quelle est la spécialité de Hiro ?", ["La robotique", "La chimie", "La physique", "La biologie"], "La robotique", 2),
    ("Quel est le nom complet de Stitch ?", ["Expérience 626", "Expérience 625", "Expérience 627", "Expérience 628"], "Expérience 626", 2),
    ("Dans 'Lilo et Stitch', quel est l'instrument préféré de Lilo ?", ["Ukulélé", "Guitare", "Piano", "Tambour"], "Ukulélé", 2),
    ("Combien de doigts a Mickey Mouse par main ?", ["4", "5", "3", "6"], "4", 2),
    ("De quelle couleur sont les chaussures de Mickey Mouse ?", ["Jaunes", "Rouges", "Noires", "Blanches"], "Jaunes", 2),
    ("Quel est le prénom de Donald Duck ?", ["Donald", "Donnie", "Don", "Donal"], "Donald", 1),
]

question_id = question_id_start
for q, opts, ans, diff in trivia_questions_data:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about sequels and franchises
sequel_questions = [
    ("'La Reine des Neiges 2' est sorti en quelle année ?", ["2019", "2018", "2020", "2017"], "2019", 2),
    ("Quel est le titre de la suite de 'Les Mondes de Ralph' ?", ["Ralph 2.0", "Ralph Brise l'Internet", "Super Ralph", "Ralph Revient"], "Ralph 2.0", 2),
    ("'Toy Story 2' a été réalisé en quelle année ?", ["1999", "2000", "1998", "2001"], "1999", 2),
    ("Combien de films 'Toy Story' ont été produits ?", ["4", "3", "5", "2"], "4", 2),
    ("Quel film Disney a eu une suite 29 ans après l'original ?", ["La Reine des Neiges", "Mary Poppins", "Fantasia", "Le Monde de Nemo"], "Mary Poppins", 3),
    ("'Le Retour de Jafar' est la suite de quel film ?", ["Aladdin", "Le Roi Lion", "La Belle et la Bête", "Hercule"], "Aladdin", 1),
    ("Combien de films 'Cars' existent ?", ["3", "2", "4", "5"], "3", 2),
    ("'Le Monde de Nemo' a eu une suite appelée ?", ["Le Monde de Dory", "Dory Cherche Nemo", "Le Retour de Nemo", "Nemo 2"], "Le Monde de Dory", 1),
    ("'Les Indestructibles' a eu sa suite après combien d'années ?", ["14 ans", "10 ans", "15 ans", "20 ans"], "14 ans", 3),
    ("Quel film Pixar parle d'un rat cuisinier ?", ["Ratatouille", "Les Indestructibles", "Monstres et Cie", "Vice-Versa"], "Ratatouille", 1),
]

for q, opts, ans, diff in sequel_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about Disney parks
park_questions = [
    ("En quelle année Disneyland en Californie a-t-il ouvert ?", ["1955", "1960", "1950", "1965"], "1955", 2),
    ("En quelle année Disneyland Paris a-t-il ouvert ?", ["1992", "1990", "1995", "1988"], "1992", 2),
    ("Quel est le nom du château à Walt Disney World ?", ["Château de Cendrillon", "Château de la Belle au Bois Dormant", "Château de Raiponce", "Château d'Elsa"], "Château de Cendrillon", 2),
    ("Dans quel état américain se trouve Walt Disney World ?", ["Floride", "Californie", "Texas", "New York"], "Floride", 1),
    ("Combien de parcs Disney existent dans le monde ?", ["6", "4", "8", "10"], "6", 2),
    ("Quel parc Disney se trouve au Japon ?", ["Tokyo Disney", "Kyoto Disney", "Osaka Disney", "Hiroshima Disney"], "Tokyo Disney", 1),
    ("Quel est le nom de la rue principale à Disneyland ?", ["Main Street USA", "Disney Avenue", "Magic Street", "Fantasy Boulevard"], "Main Street USA", 2),
    ("Quelle attraction célèbre met en scène des pirates ?", ["Pirates of the Caribbean", "Splash Mountain", "Space Mountain", "Big Thunder Mountain"], "Pirates of the Caribbean", 1),
    ("Quel land de Disneyland est consacré au futur ?", ["Tomorrowland", "Futureland", "Space World", "Tech Zone"], "Tomorrowland", 2),
    ("Quel est le nom du parc aquatique de Walt Disney World ?", ["Typhoon Lagoon", "Splash World", "Water Kingdom", "Aqua Disney"], "Typhoon Lagoon", 3),
]

for q, opts, ans, diff in park_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about Disney TV shows and shorts
tv_questions = [
    ("Quel est le nom du chien de Mickey Mouse ?", ["Pluto", "Dingo", "Max", "Bruno"], "Pluto", 1),
    ("Comment s'appelle le neveu de Donald Duck ?", ["Riri, Fifi et Loulou", "Tic, Tac et Toc", "Max et Moritz", "Zip et Zap"], "Riri, Fifi et Loulou", 1),
    ("Quel personnage Disney porte toujours un chapeau vert avec une plume ?", ["Peter Pan", "Robin des Bois", "Merlin", "Arthur"], "Peter Pan", 1),
    ("Dans quelle série TV apparaît Picsou ?", ["La Bande à Picsou", "DuckTales", "Les Aventures de Mickey", "Disney Club"], "La Bande à Picsou", 1),
    ("Quel est le prénom de la petite amie de Mickey ?", ["Minnie", "Daisy", "Clarabelle", "Pénélope"], "Minnie", 1),
    ("Comment s'appelle la petite amie de Donald ?", ["Daisy", "Minnie", "Clarabelle", "Penny"], "Daisy", 1),
    ("Quel personnage Disney est connu pour être très maladroit ?", ["Dingo", "Donald", "Pluto", "Mickey"], "Dingo", 1),
    ("Comment s'appelle le fils de Dingo ?", ["Max", "Junior", "Bobby", "Timmy"], "Max", 2),
    ("Quel duo de tamias fait des bêtises ?", ["Tic et Tac", "Riri et Fifi", "Tom et Jerry", "Zip et Zap"], "Tic et Tac", 1),
    ("Dans quelle série Darkwing Duck apparaît-il ?", ["Myster Mask", "DuckTales", "TaleSpin", "Goof Troop"], "Myster Mask", 2),
]

for q, opts, ans, diff in tv_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about colors and visual elements
visual_questions = [
    ("De quelle couleur est la robe d'Ariel ?", ["Violet/Mauve", "Rose", "Bleu", "Vert"], "Violet/Mauve", 2),
    ("De quelle couleur est la robe de Cendrillon ?", ["Bleu", "Rose", "Blanc", "Argent"], "Bleu", 1),
    ("De quelle couleur est la robe d'Aurore ?", ["Rose ou Bleu", "Rouge", "Jaune", "Verte"], "Rose ou Bleu", 1),
    ("De quelle couleur sont les cheveux d'Ariel ?", ["Roux", "Blonds", "Bruns", "Noirs"], "Roux", 1),
    ("De quelle couleur sont les cheveux de Raiponce ?", ["Blonds dorés", "Bruns", "Roux", "Noirs"], "Blonds dorés", 1),
    ("De quelle couleur est Stitch ?", ["Bleu", "Vert", "Violet", "Rose"], "Bleu", 1),
    ("De quelle couleur est le tapis volant dans 'Aladdin' ?", ["Violet et or", "Rouge et or", "Bleu et or", "Vert et or"], "Violet et or", 2),
    ("De quelle couleur est Sébastien dans 'La Petite Sirène' ?", ["Rouge", "Orange", "Rose", "Violet"], "Rouge", 1),
    ("De quelle couleur est la fourrure de Simba adulte ?", ["Marron-roux", "Jaune", "Beige", "Orange"], "Marron-roux", 2),
    ("De quelle couleur est la cape d'Elsa ?", ["Bleu glacier", "Blanc", "Violet", "Argent"], "Bleu glacier", 2),
]

for q, opts, ans, diff in visual_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about numbers and quantities
number_questions = [
    ("Combien y a-t-il de dalmatiens dans '101 Dalmatiens' ?", ["101", "100", "99", "102"], "101", 1),
    ("Combien de nains accompagnent Blanche-Neige ?", ["7", "6", "8", "5"], "7", 1),
    ("Combien de sœurs a Ariel dans 'La Petite Sirène' ?", ["6", "5", "7", "4"], "6", 2),
    ("Combien de frères a le Prince Hans ?", ["12", "10", "11", "13"], "12", 3),
    ("Combien de souhaits le Génie peut-il accorder ?", ["3", "5", "Illimité", "1"], "3", 1),
    ("Combien d'années Aurore doit-elle dormir ?", ["100 ans", "50 ans", "10 ans", "Éternellement"], "100 ans", 2),
    ("Combien de chatons a Duchesse ?", ["3", "2", "4", "5"], "3", 1),
    ("Combien de Muses racontent l'histoire dans 'Hercule' ?", ["5", "3", "7", "9"], "5", 3),
    ("Combien d'îles Moana doit-elle visiter ?", ["Plusieurs", "1", "3", "10"], "Plusieurs", 2),
    ("Combien de pétales a la rose dans 'La Belle et la Bête' ?", ["Inconnu", "12", "24", "7"], "Inconnu", 3),
]

for q, opts, ans, diff in number_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about family relationships
family_questions = [
    ("Qui est le père de Simba ?", ["Mufasa", "Scar", "Rafiki", "Sarabi"], "Mufasa", 1),
    ("Qui est la mère de Simba ?", ["Sarabi", "Nala", "Shenzi", "Sarafina"], "Sarabi", 2),
    ("Qui est l'oncle de Simba ?", ["Scar", "Mufasa", "Timon", "Zazu"], "Scar", 1),
    ("Qui est la sœur d'Elsa ?", ["Anna", "Kristoff", "Olaf", "Sven"], "Anna", 1),
    ("Qui est le frère d'Anna ?", ["Elle n'a pas de frère", "Hans", "Kristoff", "Olaf"], "Elle n'a pas de frère", 1),
    ("Qui est le père de Mulan ?", ["Fa Zhou", "Li Shang", "Shan Yu", "L'Empereur"], "Fa Zhou", 2),
    ("Qui est le père d'Ariel ?", ["Le Roi Triton", "Prince Éric", "Sébastien", "Ursula"], "Le Roi Triton", 1),
    ("Qui est la grand-mère de Moana ?", ["Tala", "Sina", "Tui", "Te Fiti"], "Tala", 2),
    ("Qui est le père de Belle ?", ["Maurice", "Gaston", "Lumière", "La Bête"], "Maurice", 1),
    ("Qui est la mère adoptive de Tarzan ?", ["Kala", "Jane", "Terk", "Tantor"], "Kala", 2),
    ("Qui sont les parents de Mérida ?", ["Fergus et Elinor", "Hamish et Hubert", "Angus et Mor'du", "Malcolm et Margaret"], "Fergus et Elinor", 2),
    ("Qui est le frère de Tadashi dans 'Les Nouveaux Héros' ?", ["Hiro", "Baymax", "Wasabi", "Fred"], "Hiro", 1),
    ("Combien de sœurs a Mirabel dans 'Encanto' ?", ["2", "1", "3", "4"], "2", 1),
    ("Comment s'appellent les sœurs de Mirabel ?", ["Isabela et Luisa", "Anna et Elsa", "Ariel et Aurore", "Maria et Sofia"], "Isabela et Luisa", 2),
    ("Qui est l'oncle disparu dans 'Encanto' ?", ["Bruno", "Felix", "Agustin", "Antonio"], "Bruno", 1),
]

for q, opts, ans, diff in family_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about special powers and abilities
powers_questions = [
    ("Quel pouvoir a Elsa ?", ["Pouvoir de glace et neige", "Pouvoir du feu", "Pouvoir de voler", "Pouvoir de télépathie"], "Pouvoir de glace et neige", 1),
    ("Quel pouvoir a Isabela dans 'Encanto' ?", ["Faire pousser des fleurs", "Super force", "Parler aux animaux", "Contrôler la météo"], "Faire pousser des fleurs", 2),
    ("Quel pouvoir a Luisa dans 'Encanto' ?", ["Super force", "Faire pousser des fleurs", "Métamorphose", "Contrôler l'eau"], "Super force", 1),
    ("Quel pouvoir ont les cheveux de Raiponce ?", ["Guérison et jeunesse", "Force", "Vol", "Invisibilité"], "Guérison et jeunesse", 1),
    ("Quel est le pouvoir spécial de Maui ?", ["Métamorphose", "Super force", "Contrôle de l'eau", "Voler"], "Métamorphose", 2),
    ("Que peut faire Hercule ?", ["Force surhumaine", "Voler", "Contrôler le feu", "Lire les pensées"], "Force surhumaine", 1),
    ("Que peut faire Merlin ?", ["Magie", "Voler", "Super force", "Invisibilité"], "Magie", 1),
    ("Quel est le talent spécial de Pocahontas ?", ["Comprendre la nature", "Voler", "Guérir", "Prédire l'avenir"], "Comprendre la nature", 2),
    ("Que peut faire la Fée Clochette ?", ["Voler et faire de la magie", "Guérir", "Lire les pensées", "Devenir invisible"], "Voler et faire de la magie", 1),
    ("Quel est le pouvoir d'Ursula ?", ["Magie noire des océans", "Contrôle des animaux", "Super force", "Téléportation"], "Magie noire des océans", 2),
]

for q, opts, ans, diff in powers_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

# Questions about food and meals
food_questions = [
    ("Quel plat Rémy prépare-t-il dans 'Ratatouille' ?", ["Ratatouille", "Soupe", "Gâteau", "Omelette"], "Ratatouille", 1),
    ("Que mange Timon et Pumbaa ?", ["Des insectes", "De la viande", "Des fruits", "De l'herbe"], "Des insectes", 1),
    ("Quelle pomme empoisonne Blanche-Neige ?", ["Une pomme rouge", "Une pomme verte", "Une pomme or", "Une pomme bleue"], "Une pomme rouge", 1),
    ("Que prépare Tiana dans son restaurant ?", ["Cuisine créole", "Cuisine française", "Cuisine italienne", "Cuisine chinoise"], "Cuisine créole", 2),
    ("Que veut manger Winnie l'Ourson ?", ["Du miel", "Des fruits", "Du gâteau", "Des bonbons"], "Du miel", 1),
    ("Que mange Belle avec la Bête ?", ["Un dîner au château", "Une pomme", "Du pain", "Une soupe"], "Un dîner au château", 2),
    ("Que prépare la marraine fée avec une citrouille ?", ["Un carrosse", "Une soupe", "Une tarte", "Un gâteau"], "Un carrosse", 1),
    ("Que boit Alice pour rétrécir ?", ["Une potion", "Du thé", "Du lait", "Du jus"], "Une potion", 1),
    ("Quel gâteau mange Alice pour grandir ?", ["Eat Me", "Drink Me", "Try Me", "Taste Me"], "Eat Me", 2),
    ("Que cuisine Linguini dans 'Ratatouille' ?", ["Cuisine française", "Cuisine italienne", "Cuisine américaine", "Cuisine asiatique"], "Cuisine française", 1),
]

for q, opts, ans, diff in food_questions:
    additional_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

print(f"Part 2 generated {len(additional_questions)} additional questions")
print(f"Total question ID reached: {question_id}")

# Save part 2
with open('disney_quiz_part2.json', 'w', encoding='utf-8') as f:
    json.dump(additional_questions, f, ensure_ascii=False, indent=2)

print("Part 2 saved to disney_quiz_part2.json")

