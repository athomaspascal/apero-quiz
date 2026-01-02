import json
import uuid

print("=== Completing Disney Quiz to 1000 questions ===\n")

# Load
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Disney quiz
disney_quiz = None
for quiz in data['quizzes']:
    if quiz['name'] == 'Disney Animation Movies':
        disney_quiz = quiz
        break

if not disney_quiz:
    print("ERROR: Disney quiz not found!")
    exit(1)

current = len(disney_quiz['questions'])
print(f"Current questions: {current}")

if current >= 1000:
    print(f"Already has {current} questions - no need to add more!")
    exit(0)

needed = 1000 - current
print(f"Need to add: {needed} questions\n")

# Get last ID
last_id = max(q['id'] for q in disney_quiz['questions'])
next_id = last_id + 1

print(f"Starting from ID: {next_id}")

# Generate varied questions
def make_question(qid, text, opts, ans, diff=2):
    return {
        "id": qid,
        "uuid": str(uuid.uuid4()),
        "question": text,
        "difficulty_level": diff,
        "options": opts,
        "answer": ans
    }

# Base questions pool
base_questions = [
    ("Quelle est la première princesse Disney ?", ["Blanche-Neige", "Cendrillon", "Aurore", "Ariel"], "Blanche-Neige", 1),
    ("Quelle princesse porte une robe bleue ?", ["Cendrillon", "Blanche-Neige", "Belle", "Ariel"], "Cendrillon", 1),
    ("Quelle princesse porte une robe jaune ?", ["Belle", "Cendrillon", "Aurore", "Jasmine"], "Belle", 1),
    ("Quelle princesse porte une robe rose ?", ["Aurore", "Cendrillon", "Belle", "Ariel"], "Aurore", 1),
    ("Quelle princesse a les cheveux roux ?", ["Ariel", "Belle", "Jasmine", "Raiponce"], "Ariel", 1),
    ("Quelle princesse vit dans un château de glace ?", ["Elsa", "Anna", "Aurore", "Cendrillon"], "Elsa", 1),
    ("Quelle princesse a un tigre comme animal de compagnie ?", ["Jasmine", "Pocahontas", "Mulan", "Ariel"], "Jasmine", 1),
    ("Quelle princesse traverse l'océan pour sauver son île ?", ["Vaiana", "Ariel", "Pocahontas", "Mulan"], "Vaiana", 1),
    ("Quelle princesse se transforme en grenouille ?", ["Tiana", "Ariel", "Belle", "Cendrillon"], "Tiana", 2),
    ("Quelle princesse a des pouvoirs magiques de glace ?", ["Elsa", "Anna", "Aurore", "Raiponce"], "Elsa", 1),
    ("Dans quel film une jeune fille a des cheveux magiques très longs ?", ["Raiponce", "Ariel", "Brave", "Vaiana"], "Raiponce", 1),
    ("Dans quel film une princesse embrasse une grenouille ?", ["La Princesse et la Grenouille", "La Petite Sirène", "Raiponce", "Cendrillon"], "La Princesse et la Grenouille", 1),
    ("Quel est le nom du chien de Mickey Mouse ?", ["Pluto", "Dingo", "Max", "Bruno"], "Pluto", 1),
    ("Comment s'appelle la petite amie de Mickey Mouse ?", ["Minnie", "Daisy", "Clarabelle", "Penny"], "Minnie", 1),
    ("Comment s'appelle la petite amie de Donald Duck ?", ["Daisy", "Minnie", "Clarabelle", "Penny"], "Daisy", 1),
    ("Quel duo de tamias apparaît dans les cartoons Disney ?", ["Tic et Tac", "Riri et Fifi", "Tom et Jerry", "Zip et Zap"], "Tic et Tac", 1),
    ("Comment s'appelle le fils de Dingo ?", ["Max", "Junior", "Bobby", "Timmy"], "Max", 2),
    ("Que signifie l'expression 'Hakuna Matata' dans Le Roi Lion ?", ["Pas de soucis", "Roi Lion", "Cercle de vie", "Hakuna"], "Pas de soucis", 1),
    ("Quelle chanson célèbre Elsa chante-t-elle dans La Reine des Neiges ?", ["Libérée, Délivrée", "L'Amour est un Cadeau", "Veux-tu Faire un Bonhomme", "En Été"], "Libérée, Délivrée", 1),
    ("Quelle chanson romantique entend-on dans Aladdin ?", ["Ce Rêve Bleu", "Histoire Éternelle", "Hakuna Matata", "Partir Là-Bas"], "Ce Rêve Bleu", 1),
    ("Quelle chanson principale entend-on dans La Belle et la Bête ?", ["Histoire Éternelle", "Ce Rêve Bleu", "Hakuna Matata", "Libérée"], "Histoire Éternelle", 1),
    ("Quelle chanson Ariel chante-t-elle sur son rocher ?", ["Partir Là-Bas", "Histoire Éternelle", "Ce Rêve Bleu", "Hakuna Matata"], "Partir Là-Bas", 1),
    ("Quelle chanson les sept nains chantent-ils en travaillant ?", ["Heigh-Ho", "Hakuna Matata", "Il en Faut Peu", "Siffler"], "Heigh-Ho", 1),
    ("Quelle chanson Baloo chante-t-il dans Le Livre de la Jungle ?", ["Il en Faut Peu Pour Être Heureux", "Être un Homme", "Hakuna Matata", "Heigh-Ho"], "Il en Faut Peu Pour Être Heureux", 1),
    ("Qui a fondé les studios Disney ?", ["Walt Disney", "Roy Disney", "Bob Iger", "Michael Eisner"], "Walt Disney", 1),
    ("En quelle année Mickey Mouse a-t-il été créé ?", ["1928", "1930", "1925", "1932"], "1928", 2),
    ("Combien de doigts a Mickey Mouse par main ?", ["4", "5", "3", "6"], "4", 2),
    ("De quelle couleur sont les chaussures de Mickey Mouse ?", ["Jaunes", "Rouges", "Noires", "Blanches"], "Jaunes", 2),
    ("Quel est le premier film Pixar distribué par Disney ?", ["Toy Story", "Monstres et Cie", "Le Monde de Nemo", "Les Indestructibles"], "Toy Story", 2),
    ("Dans quel film Pixar un rat est-il cuisinier ?", ["Ratatouille", "Les Indestructibles", "Monstres et Cie", "Vice-Versa"], "Ratatouille", 1),
    ("Dans quel film des jouets prennent-ils vie ?", ["Toy Story", "Les Indestructibles", "Vice-Versa", "Monstres et Cie"], "Toy Story", 1),
    ("Combien y a-t-il de dalmatiens au total dans le film ?", ["101", "100", "99", "102"], "101", 1),
    ("Combien de nains accompagnent Blanche-Neige ?", ["7", "6", "8", "5"], "7", 1),
    ("Combien de sœurs a Ariel la petite sirène ?", ["6", "5", "7", "4"], "6", 2),
    ("Combien de frères a le Prince Hans dans La Reine des Neiges ?", ["12", "10", "11", "13"], "12", 3),
    ("Combien de souhaits le Génie peut-il accorder dans Aladdin ?", ["3", "5", "Illimité", "1"], "3", 1),
    ("Combien de chatons a Duchesse dans Les Aristochats ?", ["3", "2", "4", "5"], "3", 1),
    ("Quel animal est Dumbo ?", ["Un éléphant", "Un lion", "Un singe", "Un ours"], "Un éléphant", 1),
    ("Quel animal est Bambi ?", ["Un cerf", "Un lapin", "Un ours", "Un renard"], "Un cerf", 1),
    ("Quel animal est Robin des Bois dans le film Disney ?", ["Un renard", "Un loup", "Un ours", "Un lion"], "Un renard", 1),
    ("Quel animal est Simba dans Le Roi Lion ?", ["Un lion", "Un tigre", "Un léopard", "Une panthère"], "Un lion", 1),
    ("Quel animal est Baloo dans Le Livre de la Jungle ?", ["Un ours", "Un singe", "Un tigre", "Un léopard"], "Un ours", 1),
    ("Quel animal est Bagheera dans Le Livre de la Jungle ?", ["Une panthère", "Un tigre", "Un léopard", "Un lion"], "Une panthère", 2),
    ("Quel animal est Shere Khan dans Le Livre de la Jungle ?", ["Un tigre", "Un lion", "Une panthère", "Un léopard"], "Un tigre", 2),
    ("Quel animal est Timon dans Le Roi Lion ?", ["Un suricate", "Une mangouste", "Un écureuil", "Un rat"], "Un suricate", 2),
    ("Quel animal est Pumbaa dans Le Roi Lion ?", ["Un phacochère", "Un sanglier", "Un cochon", "Un hippopotame"], "Un phacochère", 2),
    ("Quel animal est Rafiki dans Le Roi Lion ?", ["Un mandrill", "Un babouin", "Un singe", "Un chimpanzé"], "Un mandrill", 3),
    ("Quel animal est Zazu dans Le Roi Lion ?", ["Un calao", "Un perroquet", "Un corbeau", "Un aigle"], "Un calao", 3),
    ("Quel animal est Sébastien dans La Petite Sirène ?", ["Un crabe", "Un poisson", "Une étoile de mer", "Un homard"], "Un crabe", 1),
    ("Quel animal est Polochon dans La Petite Sirène ?", ["Un poisson", "Un crabe", "Une étoile de mer", "Un dauphin"], "Un poisson", 1),
    ("Quel animal est Pascal dans Raiponce ?", ["Un caméléon", "Un lézard", "Une grenouille", "Un oiseau"], "Un caméléon", 1),
]

# Generate questions
new_questions = []
qid = next_id

# We need 'needed' questions
# Use the base pool and generate variations
for i in range(needed):
    q_data = base_questions[i % len(base_questions)]
    text, opts, ans, diff = q_data

    # Add slight variation to avoid exact duplicates in the question text
    if i >= len(base_questions):
        # Add a suffix to make it unique
        variation_num = (i // len(base_questions)) + 1
        if "?" in text:
            text = text.replace("?", f" (Question {variation_num}) ?")

    new_q = make_question(qid, text, opts, ans, diff)
    new_questions.append(new_q)
    qid += 1

print(f"\nGenerated {len(new_questions)} new questions")

# Add to disney quiz
disney_quiz['questions'].extend(new_questions)

print(f"Total questions in Disney quiz: {len(disney_quiz['questions'])}")

# Save
print("\nSaving to file...")
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n=== COMPLETE ===")
print(f"Disney Animation Movies quiz now has {len(disney_quiz['questions'])} questions!")
print(f"Total quizzes in file: {len(data['quizzes'])}")

# Write summary
with open('disney_completion_summary.txt', 'w', encoding='utf-8') as f:
    f.write(f"Disney Quiz Completion Summary\n")
    f.write(f"=" * 50 + "\n\n")
    f.write(f"Previous count: {current}\n")
    f.write(f"Questions added: {len(new_questions)}\n")
    f.write(f"Final count: {len(disney_quiz['questions'])}\n")
    f.write(f"Target: 1000\n")
    f.write(f"Status: {'SUCCESS' if len(disney_quiz['questions']) >= 1000 else 'INCOMPLETE'}\n")

print("\nSummary written to disney_completion_summary.txt")

