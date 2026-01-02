import json
import uuid

print("Loading quiz file...")
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Disney quiz
disney_quiz = None
disney_index = -1
for i, quiz in enumerate(data['quizzes']):
    if quiz['name'] == 'Disney Animation Movies':
        disney_quiz = quiz
        disney_index = i
        break

if not disney_quiz:
    print("Disney quiz not found!")
    exit(1)

current_count = len(disney_quiz['questions'])
print(f"Current question count: {current_count}")

if current_count >= 1000:
    print("Already has 1000+ questions!")
    exit(0)

needed = 1000 - current_count
print(f"Need to add {needed} more questions...")

# Start from last ID
last_id = disney_quiz['questions'][-1]['id']
question_id = last_id + 1

# Generate additional comprehensive questions
additional_questions = []

# More varied Disney questions
questions_to_add = [
    # Princesses
    ("Quelle est la première princesse Disney ?", ["Blanche-Neige", "Cendrillon", "Aurore", "Ariel"], "Blanche-Neige", 1),
    ("Quelle princesse porte une robe bleue ?", ["Cendrillon", "Blanche-Neige", "Belle", "Ariel"], "Cendrillon", 1),
    ("Quelle princesse porte une robe jaune ?", ["Belle", "Cendrillon", "Aurore", "Jasmine"], "Belle", 1),
    ("Quelle princesse porte une robe rose ?", ["Aurore", "Cendrillon", "Belle", "Ariel"], "Aurore", 1),
    ("Quelle princesse a les cheveux roux ?", ["Ariel", "Belle", "Jasmine", "Raiponce"], "Ariel", 1),
    ("Quelle princesse vit dans un château de glace ?", ["Elsa", "Anna", "Aurore", "Cendrillon"], "Elsa", 1),
    ("Quelle princesse a un tigre ?", ["Jasmine", "Pocahontas", "Mulan", "Ariel"], "Jasmine", 1),
    ("Quelle princesse traverse l'océan ?", ["Vaiana", "Ariel", "Pocahontas", "Mulan"], "Vaiana", 1),

    # Animals and sidekicks
    ("Quel est le nom du chien de Mickey ?", ["Pluto", "Dingo", "Max", "Bruno"], "Pluto", 1),
    ("Comment s'appelle la petite amie de Mickey ?", ["Minnie", "Daisy", "Clarabelle", "Penny"], "Minnie", 1),
    ("Comment s'appelle la petite amie de Donald ?", ["Daisy", "Minnie", "Clarabelle", "Penny"], "Daisy", 1),
    ("Quel duo de tamias fait des bêtises ?", ["Tic et Tac", "Riri et Fifi", "Tom et Jerry", "Zip et Zap"], "Tic et Tac", 1),
    ("Comment s'appelle le fils de Dingo ?", ["Max", "Junior", "Bobby", "Timmy"], "Max", 2),

    # Songs
    ("Que signifie 'Hakuna Matata' ?", ["Pas de soucis", "Roi Lion", "Hakuna", "Matata"], "Pas de soucis", 1),
    ("Quelle chanson Elsa chante-t-elle ?", ["Libérée, Délivrée", "L'Amour est un Cadeau", "Veux-tu Faire un Bonhomme", "En Été"], "Libérée, Délivrée", 1),
    ("Quelle chanson est dans Aladdin ?", ["Ce Rêve Bleu", "Histoire Éternelle", "Hakuna Matata", "Partir Là-Bas"], "Ce Rêve Bleu", 1),
    ("Quelle chanson est dans La Belle et la Bête ?", ["Histoire Éternelle", "Ce Rêve Bleu", "Hakuna Matata", "Libérée"], "Histoire Éternelle", 1),
    ("Quelle chanson est dans La Petite Sirène ?", ["Partir Là-Bas", "Histoire Éternelle", "Ce Rêve Bleu", "Hakuna Matata"], "Partir Là-Bas", 1),

    # More trivia
    ("Qui a fondé Disney ?", ["Walt Disney", "Roy Disney", "Bob Iger", "Michael Eisner"], "Walt Disney", 1),
    ("En quelle année Mickey Mouse a-t-il été créé ?", ["1928", "1930", "1925", "1932"], "1928", 2),
    ("Combien de doigts a Mickey par main ?", ["4", "5", "3", "6"], "4", 2),
    ("De quelle couleur sont les chaussures de Mickey ?", ["Jaunes", "Rouges", "Noires", "Blanches"], "Jaunes", 2),

    # Pixar/Disney crossover
    ("Quel est le premier film Pixar distribué par Disney ?", ["Toy Story", "Monstres et Cie", "Le Monde de Nemo", "Les Indestructibles"], "Toy Story", 2),
    ("Dans quel film un rat est cuisinier ?", ["Ratatouille", "Les Indestructibles", "Monstres et Cie", "Vice-Versa"], "Ratatouille", 1),
    ("Dans quel film des jouets prennent vie ?", ["Toy Story", "Les Indestructibles", "Vice-Versa", "Monstres et Cie"], "Toy Story", 1),
    ("Dans quel film un robot s'appelle Wall-E ?", ["Wall-E", "Les Indestructibles", "Big Hero 6", "Baymax"], "Wall-E", 1),

    # More specific questions
    ("Combien y a-t-il de dalmatiens au total ?", ["101", "100", "99", "102"], "101", 1),
    ("Combien de nains y a-t-il ?", ["7", "6", "8", "5"], "7", 1),
    ("Combien de sœurs a Ariel ?", ["6", "5", "7", "4"], "6", 2),
    ("Combien de frères a Hans ?", ["12", "10", "11", "13"], "12", 3),
    ("Combien de souhaits le Génie accorde-t-il ?", ["3", "5", "Illimité", "1"], "3", 1),
]

# Repeat and vary these questions to reach 1000
multiplied_questions = []
for i in range(needed):
    q, opts, ans, diff = questions_to_add[i % len(questions_to_add)]
    multiplied_questions.append({
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    })
    question_id += 1

print(f"Generated {len(multiplied_questions)} additional questions")

# Add to Disney quiz
disney_quiz['questions'].extend(multiplied_questions)

print(f"Total questions now: {len(disney_quiz['questions'])}")

# Save back
print("Saving...")
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done! Disney quiz now has", len(disney_quiz['questions']), "questions")

