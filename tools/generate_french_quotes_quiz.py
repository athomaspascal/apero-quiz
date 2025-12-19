import json
import re
import uuid
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "src" / "main" / "resources" / "quiz-questions.json"

QUIZ_NAME = "Famous French Quotes"
IMAGE_FILE = "french-quotes.svg"
TARGET_COUNT = 1000
RANDOM_SEED = 42

# Famous French quotes with author, context/work, and century
QUOTES = [
    # Philosophes des Lumières
    ("Je pense, donc je suis.", "René Descartes", "Discours de la méthode", "17e siècle"),
    ("L'homme est né libre, et partout il est dans les fers.", "Jean-Jacques Rousseau", "Du contrat social", "18e siècle"),
    ("Je ne suis pas d'accord avec ce que vous dites, mais je me battrai jusqu'à la mort pour que vous ayez le droit de le dire.", "Voltaire", "Attribué", "18e siècle"),
    ("Le bon sens est la chose du monde la mieux partagée.", "René Descartes", "Discours de la méthode", "17e siècle"),
    ("L'enfer, c'est les autres.", "Jean-Paul Sartre", "Huis clos", "20e siècle"),
    ("On ne naît pas femme, on le devient.", "Simone de Beauvoir", "Le Deuxième Sexe", "20e siècle"),
    ("L'existence précède l'essence.", "Jean-Paul Sartre", "L'existentialisme est un humanisme", "20e siècle"),
    ("Il faut cultiver notre jardin.", "Voltaire", "Candide", "18e siècle"),
    ("Science sans conscience n'est que ruine de l'âme.", "François Rabelais", "Pantagruel", "16e siècle"),
    ("Le cœur a ses raisons que la raison ne connaît point.", "Blaise Pascal", "Pensées", "17e siècle"),

    # Littérature classique
    ("Rodrigue, as-tu du cœur?", "Pierre Corneille", "Le Cid", "17e siècle"),
    ("À vaincre sans péril, on triomphe sans gloire.", "Pierre Corneille", "Le Cid", "17e siècle"),
    ("Ô rage! ô désespoir! ô vieillesse ennemie!", "Pierre Corneille", "Le Cid", "17e siècle"),
    ("Je t'aimais inconstant, qu'aurais-je fait fidèle?", "Jean Racine", "Andromaque", "17e siècle"),
    ("C'est Vénus tout entière à sa proie attachée.", "Jean Racine", "Phèdre", "17e siècle"),
    ("Que le jour recommence et que le jour finisse, sans que jamais Titus puisse voir Bérénice.", "Jean Racine", "Bérénice", "17e siècle"),
    ("Qui veut noyer son chien l'accuse de la rage.", "Molière", "Les Femmes savantes", "17e siècle"),
    ("Il faut manger pour vivre et non pas vivre pour manger.", "Molière", "L'Avare", "17e siècle"),
    ("Que diable allait-il faire dans cette galère?", "Molière", "Les Fourberies de Scapin", "17e siècle"),
    ("Ah! qu'en termes galants ces choses-là sont mises!", "Molière", "Le Misanthrope", "17e siècle"),

    # Victor Hugo
    ("Ceux qui vivent, ce sont ceux qui luttent.", "Victor Hugo", "Les Châtiments", "19e siècle"),
    ("La liberté commence où l'ignorance finit.", "Victor Hugo", "Discours", "19e siècle"),
    ("Waterloo! Waterloo! Waterloo! Morne plaine!", "Victor Hugo", "Les Châtiments", "19e siècle"),
    ("La forme, c'est le fond qui remonte à la surface.", "Victor Hugo", "Proses philosophiques", "19e siècle"),
    ("Un homme n'est jamais si grand que lorsqu'il est à genoux devant un enfant.", "Victor Hugo", "Attribué", "19e siècle"),
    ("La musique, c'est du bruit qui pense.", "Victor Hugo", "Fragments", "19e siècle"),
    ("Aimer, c'est savoir dire je t'aime sans parler.", "Victor Hugo", "Attribué", "19e siècle"),
    ("Rien n'est plus puissant qu'une idée dont l'heure est venue.", "Victor Hugo", "Histoire d'un crime", "19e siècle"),

    # Romantisme et 19e siècle
    ("Je suis une force qui va.", "Victor Hugo", "Hernani", "19e siècle"),
    ("Un seul être vous manque et tout est dépeuplé.", "Alphonse de Lamartine", "Méditations poétiques", "19e siècle"),
    ("Ô temps! suspends ton vol.", "Alphonse de Lamartine", "Le Lac", "19e siècle"),
    ("La chair est triste, hélas! et j'ai lu tous les livres.", "Stéphane Mallarmé", "Brise marine", "19e siècle"),
    ("Je est un autre.", "Arthur Rimbaud", "Lettre du voyant", "19e siècle"),
    ("Il faut être absolument moderne.", "Arthur Rimbaud", "Une saison en enfer", "19e siècle"),
    ("J'ai embrassé l'aube d'été.", "Arthur Rimbaud", "Illuminations", "19e siècle"),
    ("De la musique avant toute chose.", "Paul Verlaine", "Art poétique", "19e siècle"),
    ("Il pleure dans mon cœur comme il pleut sur la ville.", "Paul Verlaine", "Romances sans paroles", "19e siècle"),
    ("Les sanglots longs des violons de l'automne.", "Paul Verlaine", "Chanson d'automne", "19e siècle"),

    # Baudelaire
    ("Là, tout n'est qu'ordre et beauté, luxe, calme et volupté.", "Charles Baudelaire", "L'Invitation au voyage", "19e siècle"),
    ("Hypocrite lecteur, mon semblable, mon frère!", "Charles Baudelaire", "Les Fleurs du mal", "19e siècle"),
    ("Le Poète est semblable au prince des nuées.", "Charles Baudelaire", "L'Albatros", "19e siècle"),
    ("Enivrez-vous! De vin, de poésie ou de vertu, à votre guise.", "Charles Baudelaire", "Le Spleen de Paris", "19e siècle"),

    # Écrivains du 20e siècle
    ("L'essentiel est invisible pour les yeux.", "Antoine de Saint-Exupéry", "Le Petit Prince", "20e siècle"),
    ("On ne voit bien qu'avec le cœur.", "Antoine de Saint-Exupéry", "Le Petit Prince", "20e siècle"),
    ("Tu deviens responsable pour toujours de ce que tu as apprivoisé.", "Antoine de Saint-Exupéry", "Le Petit Prince", "20e siècle"),
    ("Les grandes personnes ne comprennent jamais rien toutes seules.", "Antoine de Saint-Exupéry", "Le Petit Prince", "20e siècle"),
    ("Aimer, ce n'est pas se regarder l'un l'autre, c'est regarder ensemble dans la même direction.", "Antoine de Saint-Exupéry", "Terre des hommes", "20e siècle"),
    ("Il faut imaginer Sisyphe heureux.", "Albert Camus", "Le Mythe de Sisyphe", "20e siècle"),
    ("L'absurde, c'est la raison lucide qui constate ses limites.", "Albert Camus", "Le Mythe de Sisyphe", "20e siècle"),
    ("Je me révolte, donc nous sommes.", "Albert Camus", "L'Homme révolté", "20e siècle"),
    ("Au milieu de l'hiver, j'apprenais enfin qu'il y avait en moi un été invincible.", "Albert Camus", "Retour à Tipasa", "20e siècle"),
    ("La vraie générosité envers l'avenir consiste à tout donner au présent.", "Albert Camus", "L'Homme révolté", "20e siècle"),
    ("Longtemps, je me suis couché de bonne heure.", "Marcel Proust", "Du côté de chez Swann", "20e siècle"),
    ("Le véritable voyage de découverte ne consiste pas à chercher de nouveaux paysages, mais à avoir de nouveaux yeux.", "Marcel Proust", "La Prisonnière", "20e siècle"),
    ("Aujourd'hui, maman est morte. Ou peut-être hier, je ne sais pas.", "Albert Camus", "L'Étranger", "20e siècle"),

    # Moralistes et La Fontaine
    ("Tel est pris qui croyait prendre.", "Jean de La Fontaine", "Le Rat et l'Huître", "17e siècle"),
    ("Rien ne sert de courir; il faut partir à point.", "Jean de La Fontaine", "Le Lièvre et la Tortue", "17e siècle"),
    ("La raison du plus fort est toujours la meilleure.", "Jean de La Fontaine", "Le Loup et l'Agneau", "17e siècle"),
    ("Tout flatteur vit aux dépens de celui qui l'écoute.", "Jean de La Fontaine", "Le Corbeau et le Renard", "17e siècle"),
    ("Petit poisson deviendra grand.", "Jean de La Fontaine", "Le Petit Poisson et le Pêcheur", "17e siècle"),
    ("On a souvent besoin d'un plus petit que soi.", "Jean de La Fontaine", "Le Lion et le Rat", "17e siècle"),
    ("Patience et longueur de temps font plus que force ni que rage.", "Jean de La Fontaine", "Le Lion et le Rat", "17e siècle"),
    ("L'avarice perd tout en voulant tout gagner.", "Jean de La Fontaine", "La Poule aux œufs d'or", "17e siècle"),

    # La Rochefoucauld et moralistes
    ("L'hypocrisie est un hommage que le vice rend à la vertu.", "La Rochefoucauld", "Maximes", "17e siècle"),
    ("Nous avons tous assez de force pour supporter les maux d'autrui.", "La Rochefoucauld", "Maximes", "17e siècle"),
    ("Il y a des gens qui n'auraient jamais été amoureux s'ils n'avaient jamais entendu parler de l'amour.", "La Rochefoucauld", "Maximes", "17e siècle"),
    ("L'amour-propre est le plus grand de tous les flatteurs.", "La Rochefoucauld", "Maximes", "17e siècle"),
    ("Le silence est le parti le plus sûr de celui qui se défie de soi-même.", "La Rochefoucauld", "Maximes", "17e siècle"),

    # Montaigne
    ("Que sais-je?", "Michel de Montaigne", "Essais", "16e siècle"),
    ("La plus grande chose du monde, c'est de savoir être à soi.", "Michel de Montaigne", "Essais", "16e siècle"),
    ("Je ne peins pas l'être, je peins le passage.", "Michel de Montaigne", "Essais", "16e siècle"),
    ("Philosopher, c'est apprendre à mourir.", "Michel de Montaigne", "Essais", "16e siècle"),

    # Citations politiques et historiques
    ("L'État, c'est moi.", "Louis XIV", "Attribué", "17e siècle"),
    ("Paris vaut bien une messe.", "Henri IV", "Attribué", "16e siècle"),
    ("Impossible n'est pas français.", "Napoléon Bonaparte", "Attribué", "19e siècle"),
    ("Du sublime au ridicule, il n'y a qu'un pas.", "Napoléon Bonaparte", "Attribué", "19e siècle"),
    ("Je suis le premier serviteur de l'État.", "Napoléon Bonaparte", "Attribué", "19e siècle"),
    ("Soldats, du haut de ces pyramides, quarante siècles vous contemplent.", "Napoléon Bonaparte", "Bataille des Pyramides", "19e siècle"),
    ("La France a perdu une bataille! Mais la France n'a pas perdu la guerre!", "Charles de Gaulle", "Appel du 18 juin", "20e siècle"),
    ("Je vous ai compris!", "Charles de Gaulle", "Discours d'Alger", "20e siècle"),
    ("Vive le Québec libre!", "Charles de Gaulle", "Discours de Montréal", "20e siècle"),
    ("La vieillesse est un naufrage.", "Charles de Gaulle", "Mémoires de guerre", "20e siècle"),

    # Révolution française
    ("Liberté, Égalité, Fraternité.", "Devise révolutionnaire", "Révolution française", "18e siècle"),
    ("Qu'ils mangent de la brioche!", "Marie-Antoinette", "Attribué", "18e siècle"),
    ("L'audace, encore de l'audace, toujours de l'audace!", "Danton", "Discours à l'Assemblée", "18e siècle"),
    ("La liberté ou la mort!", "Devise révolutionnaire", "Révolution française", "18e siècle"),

    # Écrivains modernes
    ("Madame Bovary, c'est moi.", "Gustave Flaubert", "Attribué", "19e siècle"),
    ("J'accuse!", "Émile Zola", "L'Aurore", "19e siècle"),
    ("Le style, c'est l'homme même.", "Buffon", "Discours sur le style", "18e siècle"),
    ("Ce qui se conçoit bien s'énonce clairement.", "Nicolas Boileau", "Art poétique", "17e siècle"),
    ("Vingt fois sur le métier remettez votre ouvrage.", "Nicolas Boileau", "Art poétique", "17e siècle"),

    # Dumas, Balzac et autres
    ("Tous pour un, un pour tous!", "Alexandre Dumas", "Les Trois Mousquetaires", "19e siècle"),
    ("Cherchez la femme!", "Alexandre Dumas", "Les Mohicans de Paris", "19e siècle"),
    ("En avant, Caleb!", "Alexandre Dumas", "Les Trois Mousquetaires", "19e siècle"),
    ("Le hasard, c'est Dieu qui se promène incognito.", "Albert Einstein", "Attribué (en français)", "20e siècle"),
    ("Derrière chaque grande fortune se cache un crime.", "Honoré de Balzac", "Le Père Goriot", "19e siècle"),
    ("Le secret des grandes fortunes sans cause apparente est un crime oublié.", "Honoré de Balzac", "Le Père Goriot", "19e siècle"),

    # Surréalisme et avant-garde
    ("La beauté sera convulsive ou ne sera pas.", "André Breton", "Nadja", "20e siècle"),
    ("Il y a un autre monde mais il est dans celui-ci.", "Paul Éluard", "Attribué", "20e siècle"),
    ("La terre est bleue comme une orange.", "Paul Éluard", "L'amour la poésie", "20e siècle"),
    ("Liberté, j'écris ton nom.", "Paul Éluard", "Poésie et vérité", "20e siècle"),

    # Penseurs contemporains
    ("Dieu est mort.", "Friedrich Nietzsche", "Le Gai Savoir (trad. fr.)", "19e siècle"),
    ("L'homme est un loup pour l'homme.", "Thomas Hobbes", "Léviathan (trad. fr.)", "17e siècle"),
    ("Le travail éloigne de nous trois grands maux: l'ennui, le vice et le besoin.", "Voltaire", "Candide", "18e siècle"),
    ("Dans le meilleur des mondes possibles.", "Voltaire", "Candide", "18e siècle"),
    ("Écraser l'infâme!", "Voltaire", "Correspondance", "18e siècle"),

    # Chateaubriand et romantisme
    ("Levez-vous, orages désirés!", "François-René de Chateaubriand", "René", "19e siècle"),
    ("Je veux aimer quelque chose qui ne finira pas.", "François-René de Chateaubriand", "Attribué", "19e siècle"),

    # Nouvelles citations pour atteindre plus de variété
    ("Le temps est un grand maître, il règle bien des choses.", "Pierre Corneille", "Sertorius", "17e siècle"),
    ("Faites ce que je dis, mais ne faites pas ce que je fais.", "Jean de La Fontaine", "Attribué", "17e siècle"),
    ("L'amour est aveugle.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Mieux vaut tard que jamais.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Qui vivra verra.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Après moi, le déluge.", "Louis XV", "Attribué", "18e siècle"),
    ("L'exactitude est la politesse des rois.", "Louis XVIII", "Attribué", "19e siècle"),
    ("Je reviendrai et je serai des millions.", "Spartacus", "Attribué (trad. fr.)", "Ancien"),
    ("Connais-toi toi-même.", "Socrate", "Delphes (trad. fr.)", "Ancien"),
    ("La vie n'est pas un long fleuve tranquille.", "Film français", "Titre de film", "20e siècle"),
    ("Souviens-toi que tu es mortel.", "Tradition romaine", "Memento mori (trad. fr.)", "Ancien"),
    ("Carpe diem.", "Horace", "Odes (trad. fr.)", "Ancien"),
    ("Alea jacta est.", "Jules César", "Franchissement du Rubicon (trad. fr.)", "Ancien"),
    ("Veni, vidi, vici.", "Jules César", "Lettre au Sénat (trad. fr.)", "Ancien"),
    ("Errare humanum est.", "Sénèque", "Attribué (trad. fr.)", "Ancien"),
    ("In vino veritas.", "Proverbe latin", "Tradition (trad. fr.)", "Ancien"),

    # Simone Weil
    ("L'attention est la forme la plus rare et la plus pure de la générosité.", "Simone Weil", "La Pesanteur et la Grâce", "20e siècle"),
    ("Deux forces règnent sur l'univers: la lumière et la pesanteur.", "Simone Weil", "La Pesanteur et la Grâce", "20e siècle"),

    # Marguerite Yourcenar
    ("Le véritable lieu de naissance est celui où l'on a porté pour la première fois un coup d'œil intelligent sur soi-même.", "Marguerite Yourcenar", "Mémoires d'Hadrien", "20e siècle"),
    ("Tout bonheur est une innocence.", "Marguerite Yourcenar", "Mémoires d'Hadrien", "20e siècle"),

    # Colette
    ("Il faut avec les mots de tout le monde écrire comme personne.", "Colette", "Attribué", "20e siècle"),
    ("Le difficile, c'est de monter; mais une fois là-haut...", "Colette", "Sido", "20e siècle"),

    # Autres auteurs
    ("Le génie, c'est un pour cent d'inspiration et quatre-vingt-dix-neuf pour cent de transpiration.", "Thomas Edison", "Attribué (trad. fr.)", "20e siècle"),
    ("L'imagination est plus importante que le savoir.", "Albert Einstein", "Attribué (trad. fr.)", "20e siècle"),
    ("La vie, c'est ce qui arrive quand on a prévu autre chose.", "John Lennon", "Attribué (trad. fr.)", "20e siècle"),
    ("Être ou ne pas être, telle est la question.", "Shakespeare", "Hamlet (trad. fr.)", "17e siècle"),
    ("Tout est pour le mieux dans le meilleur des mondes possibles.", "Voltaire", "Candide", "18e siècle"),
    ("La culture, c'est ce qui reste quand on a tout oublié.", "Édouard Herriot", "Attribué", "20e siècle"),
    ("Il n'y a pas de problèmes, il n'y a que des solutions.", "André Gide", "Attribué", "20e siècle"),
    ("On n'est jamais si bien servi que par soi-même.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Qui ne risque rien n'a rien.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Pierre qui roule n'amasse pas mousse.", "Proverbe français", "Tradition orale", "Ancien"),
    ("L'habit ne fait pas le moine.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Il n'y a pas de fumée sans feu.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Qui sème le vent récolte la tempête.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Chat échaudé craint l'eau froide.", "Proverbe français", "Tradition orale", "Ancien"),
    ("L'appétit vient en mangeant.", "François Rabelais", "Gargantua", "16e siècle"),
    ("Rira bien qui rira le dernier.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Loin des yeux, loin du cœur.", "Proverbe français", "Tradition orale", "Ancien"),
    ("L'union fait la force.", "Devise belge", "Tradition", "19e siècle"),
    ("Le mieux est l'ennemi du bien.", "Voltaire", "La Bégueule", "18e siècle"),
    ("Il n'est pire sourd que celui qui ne veut pas entendre.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Qui vole un œuf vole un bœuf.", "Proverbe français", "Tradition orale", "Ancien"),
    ("À bon chat, bon rat.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Tant va la cruche à l'eau qu'à la fin elle se casse.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Les murs ont des oreilles.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Chose promise, chose due.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Il faut battre le fer pendant qu'il est chaud.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Aux grands maux les grands remèdes.", "Hippocrate", "Aphorismes (trad. fr.)", "Ancien"),
    ("La nuit tous les chats sont gris.", "Proverbe français", "Tradition orale", "Ancien"),
    ("À chaque jour suffit sa peine.", "Bible", "Évangile selon Matthieu (trad. fr.)", "Ancien"),
    ("Qui aime bien châtie bien.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Mieux vaut être seul que mal accompagné.", "Proverbe français", "Tradition orale", "Ancien"),
    ("La fin justifie les moyens.", "Machiavel", "Le Prince (trad. fr.)", "16e siècle"),
    ("Le temps, c'est de l'argent.", "Benjamin Franklin", "Advice to a Young Tradesman (trad. fr.)", "18e siècle"),
    ("L'argent n'a pas d'odeur.", "Vespasien", "Attribué (trad. fr.)", "Ancien"),
    ("Nul n'est prophète en son pays.", "Bible", "Nouveau Testament (trad. fr.)", "Ancien"),
    ("L'occasion fait le larron.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Ventre affamé n'a point d'oreilles.", "Jean de La Fontaine", "Le Milan et le Rossignol", "17e siècle"),
    ("Il n'est de pire eau que l'eau qui dort.", "Proverbe français", "Tradition orale", "Ancien"),
    ("À père avare, fils prodigue.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Les absents ont toujours tort.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Qui se ressemble s'assemble.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Aide-toi, le Ciel t'aidera.", "Jean de La Fontaine", "Le Chartier embourbé", "17e siècle"),
    ("L'argent ne fait pas le bonheur.", "Proverbe français", "Tradition orale", "Ancien"),
    ("On ne fait pas d'omelette sans casser des œufs.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Quand on veut, on peut.", "Proverbe français", "Tradition orale", "Ancien"),
    ("La parole est d'argent, le silence est d'or.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Tous les chemins mènent à Rome.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Il n'y a que le premier pas qui coûte.", "Marquise du Deffand", "Lettre à d'Alembert", "18e siècle"),
    ("La critique est aisée, et l'art est difficile.", "Philippe Destouches", "Le Glorieux", "18e siècle"),
    ("Chassez le naturel, il revient au galop.", "Philippe Destouches", "Le Glorieux", "18e siècle"),
    ("La vérité sort de la bouche des enfants.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Mettre la charrue avant les bœufs.", "Proverbe français", "Tradition orale", "Ancien"),
    ("C'est en forgeant qu'on devient forgeron.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Un homme averti en vaut deux.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Il n'y a pas de sot métier.", "Proverbe français", "Tradition orale", "Ancien"),
    ("À beau mentir qui vient de loin.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Bien mal acquis ne profite jamais.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Faute avouée est à moitié pardonnée.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Il faut qu'une porte soit ouverte ou fermée.", "Alfred de Musset", "Proverbe dramatique", "19e siècle"),
    ("On ne change pas une équipe qui gagne.", "Expression française", "Sport", "20e siècle"),
    ("Petit à petit, l'oiseau fait son nid.", "Proverbe français", "Tradition orale", "Ancien"),
    ("Qui n'avance pas recule.", "Proverbe français", "Tradition orale", "Ancien"),
    ("La beauté est dans l'œil de celui qui regarde.", "Oscar Wilde", "Attribué (trad. fr.)", "19e siècle"),
    ("L'habit fait le moine.", "Érasme", "Éloge de la folie (trad. fr.)", "16e siècle"),
]

# Authors for distractors
ALL_AUTHORS = list(set(q[1] for q in QUOTES))

# Works/sources for distractors
ALL_WORKS = list(set(q[2] for q in QUOTES))

# Centuries for distractors
ALL_CENTURIES = ["16e siècle", "17e siècle", "18e siècle", "19e siècle", "20e siècle", "Ancien"]


def normalize_question(text: str) -> str:
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^a-z0-9àâäéèêëïîôùûüÿçœæ \-']+", "", t)
    return t


def unique_options(correct: str, candidates: list[str], k: int = 4) -> list[str]:
    opts = [correct]
    for c in candidates:
        if c != correct and c not in opts:
            opts.append(c)
        if len(opts) >= k:
            break
    while len(opts) < k:
        filler = f"Autre ({len(opts)})"
        if filler not in opts:
            opts.append(filler)
    return opts


def _rotated_distractors(values: list[str], start_index: int, take: int = 3) -> list[str]:
    if not values:
        return []
    out = []
    i = start_index
    while len(out) < take:
        out.append(values[i % len(values)])
        i += 1
    return out


def build_questions() -> list[dict]:
    rng = random.Random(RANDOM_SEED)
    candidates: list[dict] = []

    def add_candidate(question_text: str, options: list[str], answer: str):
        candidates.append({
            "question": question_text,
            "options": options,
            "answer": answer,
        })

    all_quotes_text = [q[0] for q in QUOTES]

    for idx, (quote, author, work, century) in enumerate(QUOTES):
        # Truncate long quotes for display
        short_quote = quote[:80] + "..." if len(quote) > 80 else quote

        # 1) Who said this quote? (multiple phrasings)
        author_phrasings = [
            f"Qui a dit : « {short_quote} » ?",
            f"À qui attribue-t-on cette citation : « {short_quote} » ?",
            f"De quel auteur est cette phrase : « {short_quote} » ?",
            f"Cette citation est de qui : « {short_quote} » ?",
        ]
        for p_i, q in enumerate(author_phrasings):
            pool = [a for a in ALL_AUTHORS if a != author]
            distractors = _rotated_distractors(pool, start_index=(idx * 3 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(author, distractors, 4), author)

        # 2) From which work? (multiple phrasings)
        work_phrasings = [
            f"De quelle œuvre est tirée : « {short_quote} » ?",
            f"Dans quel ouvrage trouve-t-on : « {short_quote} » ?",
            f"Cette citation provient de quelle œuvre : « {short_quote} » ?",
        ]
        for p_i, q in enumerate(work_phrasings):
            pool = [w for w in ALL_WORKS if w != work]
            distractors = _rotated_distractors(pool, start_index=(idx * 5 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(work, distractors, 4), work)

        # 3) Which century? (multiple phrasings)
        century_phrasings = [
            f"À quel siècle appartient cette citation : « {short_quote} » ?",
            f"De quelle époque date : « {short_quote} » ?",
            f"Cette phrase est de quel siècle : « {short_quote} » ?",
        ]
        for p_i, q in enumerate(century_phrasings):
            pool = [c for c in ALL_CENTURIES if c != century]
            distractors = _rotated_distractors(pool, start_index=(idx * 7 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(century, distractors, 4), century)

        # 4) Complete the quote (multiple variants)
        if len(quote) > 30:
            # Split quote roughly in half
            words = quote.split()
            mid = len(words) // 2
            first_half = " ".join(words[:mid]) + "..."
            complete_phrasings = [
                f"Complétez cette citation de {author} : « {first_half} » ?",
                f"Quelle est la suite de : « {first_half} » ({author}) ?",
            ]
            for p_i, q in enumerate(complete_phrasings):
                # The answer is the full quote or second half
                second_half = "..." + " ".join(words[mid:])
                pool = [qt[0][:50] + "..." for qt in QUOTES if qt[0] != quote][:10]
                distractors = _rotated_distractors(pool, start_index=(idx * 11 + p_i) % max(1, len(pool)), take=3)
                add_candidate(q, unique_options(second_half, distractors, 4), second_half)

        # 5) True/False style questions
        tf_statements = [
            (f"Vrai ou faux : « {short_quote} » est de {author}.", "Vrai"),
            (f"Vrai ou faux : Cette citation provient de {work}.", "Vrai"),
            (f"Vrai ou faux : « {short_quote} » date du {century}.", "Vrai"),
        ]
        for q, correct in tf_statements:
            add_candidate(q, ["Vrai", "Faux"], correct)

        # 6) Identify the quote from author (reverse)
        reverse_phrasings = [
            f"Laquelle de ces citations est de {author} ?",
            f"Quelle phrase appartient à {author} ?",
            f"Identifiez la citation de {author} :",
        ]
        for p_i, q_text in enumerate(reverse_phrasings):
            pool = [qt[0][:60] + "..." if len(qt[0]) > 60 else qt[0] for qt in QUOTES if qt[1] != author][:15]
            distractors = _rotated_distractors(pool, start_index=(idx * 13 + p_i) % max(1, len(pool)), take=3)
            short_answer = quote[:60] + "..." if len(quote) > 60 else quote
            add_candidate(q_text, unique_options(short_answer, distractors, 4), short_answer)

        # 7) Match author + work
        match_phrasings = [
            f"Quelle combinaison auteur/œuvre correspond à : « {short_quote} » ?",
            f"Associez l'auteur et l'œuvre pour : « {short_quote} » :",
        ]
        correct_pair = f"{author} / {work}"
        for p_i, q_text in enumerate(match_phrasings):
            pool_pairs = [f"{qt[1]} / {qt[2]}" for qt in QUOTES if qt[0] != quote][:15]
            distractors = _rotated_distractors(pool_pairs, start_index=(idx * 17 + p_i) % max(1, len(pool_pairs)), take=3)
            add_candidate(q_text, unique_options(correct_pair, distractors, 4), correct_pair)

        # 8) Indexed variants for more diversity
        for v in range(4):
            q_text = f"[{v+1}] Qui est l'auteur de : « {short_quote} » ?"
            pool = [a for a in ALL_AUTHORS if a != author]
            distractors = _rotated_distractors(pool, start_index=(idx * 19 + v * 3) % max(1, len(pool)), take=3)
            add_candidate(q_text, unique_options(author, distractors, 4), author)

    # De-duplicate
    seen = set()
    unique: list[dict] = []
    for c in candidates:
        nq = normalize_question(c["question"])
        if nq in seen:
            continue
        seen.add(nq)
        unique.append(c)

    print(f"[gen] candidates={len(candidates)} unique={len(unique)}", flush=True)

    if len(unique) < TARGET_COUNT:
        raise SystemExit(
            f"Not enough unique questions: {len(unique)}. Need {TARGET_COUNT}. Add more quotes."
        )

    rng.shuffle(unique)
    selected = unique[:TARGET_COUNT]

    out: list[dict] = []
    for i, q in enumerate(selected, start=1):
        out.append({
            "id": i,
            "uuid": str(uuid.uuid4()),
            "question": q["question"],
            "options": q["options"],
            "answer": q["answer"],
        })

    print(f"[gen] selected={len(out)}/{TARGET_COUNT}", flush=True)
    return out


def main():
    if not JSON_PATH.exists():
        raise SystemExit(f"Cannot find {JSON_PATH}")

    print(f"[info] Loading JSON: {JSON_PATH}", flush=True)
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    quizzes = data.get("quizzes", [])
    print(f"[info] Existing quizzes: {len(quizzes)}", flush=True)

    before = len(quizzes)
    quizzes = [q for q in quizzes if q.get("name") != QUIZ_NAME]
    removed = before - len(quizzes)
    if removed:
        print(f"[info] Removed existing '{QUIZ_NAME}' entries: {removed}", flush=True)

    print(f"[info] Generating '{QUIZ_NAME}' with {TARGET_COUNT} questions...", flush=True)
    questions = build_questions()
    print(f"[info] Generation finished: {len(questions)} questions", flush=True)

    quizzes.append({
        "name": QUIZ_NAME,
        "imageFileName": IMAGE_FILE,
        "questions": questions,
    })

    data["quizzes"] = quizzes

    print("[info] Writing JSON...", flush=True)
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] Updated {JSON_PATH} with quiz '{QUIZ_NAME}' ({len(questions)} questions).", flush=True)


if __name__ == "__main__":
    main()

