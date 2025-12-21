import json
import random
import uuid
from pathlib import Path
from datetime import datetime

# Deterministic randomness for repeatability
random.seed(42)

BASE_JSON = Path("src/main/resources/quiz-questions.json")
BACKUP_JSON = Path(f"backup-quiz-questions-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")

# -------------------- Source data --------------------
# Each item is intentionally concise and vetted for correctness
monarchs = [
    {"name": "Clovis Ier", "title": "Roi des Francs", "start": 481, "end": 511, "dynasty": "Mérovingiens"},
    {"name": "Charlemagne", "title": "Empereur d'Occident", "start": 768, "end": 814, "dynasty": "Carolingiens"},
    {"name": "Hugues Capet", "title": "Fondateur des Capétiens", "start": 987, "end": 996, "dynasty": "Capétiens"},
    {"name": "Philippe Auguste", "title": "Roi qui agrandit le domaine royal", "start": 1180, "end": 1223, "dynasty": "Capétiens"},
    {"name": "Saint Louis", "title": "Roi croisé", "start": 1226, "end": 1270, "dynasty": "Capétiens"},
    {"name": "Philippe le Bel", "title": "Renforce la monarchie", "start": 1285, "end": 1314, "dynasty": "Capétiens"},
    {"name": "François Ier", "title": "Roi de la Renaissance", "start": 1515, "end": 1547, "dynasty": "Valois"},
    {"name": "Henri IV", "title": "Promulgateur de l'Édit de Nantes", "start": 1589, "end": 1610, "dynasty": "Bourbons"},
    {"name": "Louis XIII", "title": "Roi aux côtés de Richelieu", "start": 1610, "end": 1643, "dynasty": "Bourbons"},
    {"name": "Louis XIV", "title": "Roi Soleil", "start": 1643, "end": 1715, "dynasty": "Bourbons"},
    {"name": "Louis XV", "title": "Roi du Siècle des Lumières", "start": 1715, "end": 1774, "dynasty": "Bourbons"},
    {"name": "Louis XVI", "title": "Roi exécuté", "start": 1774, "end": 1792, "dynasty": "Bourbons"},
    {"name": "Napoléon Ier", "title": "Empereur des Français", "start": 1804, "end": 1814, "dynasty": "Bonaparte"},
    {"name": "Louis-Philippe", "title": "Roi des Français", "start": 1830, "end": 1848, "dynasty": "Orléans"},
    {"name": "Napoléon III", "title": "Second Empire", "start": 1852, "end": 1870, "dynasty": "Bonaparte"},
]

presidents = [
    {"name": "Adolphe Thiers", "start": 1871, "end": 1873},
    {"name": "Sadi Carnot", "start": 1887, "end": 1894},
    {"name": "Raymond Poincaré", "start": 1913, "end": 1920},
    {"name": "Albert Lebrun", "start": 1932, "end": 1940},
    {"name": "Charles de Gaulle", "start": 1959, "end": 1969},
    {"name": "Georges Pompidou", "start": 1969, "end": 1974},
    {"name": "Valéry Giscard d'Estaing", "start": 1974, "end": 1981},
    {"name": "François Mitterrand", "start": 1981, "end": 1995},
    {"name": "Jacques Chirac", "start": 1995, "end": 2007},
    {"name": "Nicolas Sarkozy", "start": 2007, "end": 2012},
    {"name": "François Hollande", "start": 2012, "end": 2017},
    {"name": "Emmanuel Macron", "start": 2017, "end": 2025},
]

events = [
    {"name": "Prise de la Bastille", "year": 1789, "kind": "Révolution"},
    {"name": "Nuit du 4 août", "year": 1789, "kind": "Abolition des privilèges"},
    {"name": "Déclaration des droits de l'homme et du citoyen", "year": 1789, "kind": "Texte fondateur"},
    {"name": "Fuite à Varennes", "year": 1791, "kind": "Crise monarchique"},
    {"name": "Proclamation de la République", "year": 1792, "kind": "Chute de la monarchie"},
    {"name": "Exécution de Louis XVI", "year": 1793, "kind": "Révolution"},
    {"name": "9 Thermidor", "year": 1794, "kind": "Fin de la Terreur"},
    {"name": "18 Brumaire", "year": 1799, "kind": "Coup d'État"},
    {"name": "Couronnement de Napoléon", "year": 1804, "kind": "Empire"},
    {"name": "Débarquement de Normandie", "year": 1944, "kind": "Seconde Guerre mondiale"},
    {"name": "Libération de Paris", "year": 1944, "kind": "Seconde Guerre mondiale"},
    {"name": "Appel du 18 juin", "year": 1940, "kind": "Seconde Guerre mondiale"},
    {"name": "Mai 68", "year": 1968, "kind": "Mouvement social"},
    {"name": "Traité de Maastricht", "year": 1992, "kind": "Construction européenne"},
    {"name": "Décolonisation de l'Algérie", "year": 1962, "kind": "Décolonisation"},
]

wars = [
    {"name": "Guerre de Cent Ans", "start": 1337, "end": 1453},
    {"name": "Guerres d'Italie", "start": 1494, "end": 1559},
    {"name": "Guerres de Religion", "start": 1562, "end": 1598},
    {"name": "Fronde", "start": 1648, "end": 1653},
    {"name": "Guerre de Succession d'Espagne", "start": 1701, "end": 1714},
    {"name": "Révolution française", "start": 1789, "end": 1799},
    {"name": "Guerres napoléoniennes", "start": 1803, "end": 1815},
    {"name": "Guerre de Crimée", "start": 1853, "end": 1856},
    {"name": "Guerre franco-prussienne", "start": 1870, "end": 1871},
    {"name": "Première Guerre mondiale", "start": 1914, "end": 1918},
    {"name": "Seconde Guerre mondiale", "start": 1939, "end": 1945},
    {"name": "Guerre d'Indochine", "start": 1946, "end": 1954},
    {"name": "Guerre d'Algérie", "start": 1954, "end": 1962},
]

battles = [
    {"name": "Bouvines", "year": 1214, "war": "Guerre anglo-française"},
    {"name": "Azincourt", "year": 1415, "war": "Guerre de Cent Ans"},
    {"name": "Castillon", "year": 1453, "war": "Guerre de Cent Ans"},
    {"name": "Marignan", "year": 1515, "war": "Guerres d'Italie"},
    {"name": "Ivry", "year": 1590, "war": "Guerres de Religion"},
    {"name": "Rocroi", "year": 1643, "war": "Guerre de Trente Ans"},
    {"name": "Fontenoy", "year": 1745, "war": "Guerre de Succession d'Autriche"},
    {"name": "Valmy", "year": 1792, "war": "Révolution française"},
    {"name": "Austerlitz", "year": 1805, "war": "Guerres napoléoniennes"},
    {"name": "Waterloo", "year": 1815, "war": "Guerres napoléoniennes"},
    {"name": "Magenta", "year": 1859, "war": "Guerre d'Italie"},
    {"name": "Gravelotte", "year": 1870, "war": "Guerre franco-prussienne"},
    {"name": "Verdun", "year": 1916, "war": "Première Guerre mondiale"},
    {"name": "La Marne", "year": 1914, "war": "Première Guerre mondiale"},
    {"name": "Somme", "year": 1916, "war": "Première Guerre mondiale"},
    {"name": "Bir Hakeim", "year": 1942, "war": "Seconde Guerre mondiale"},
]

institutions = [
    {"name": "Conseil d'État", "year": 1799, "role": "Conseiller le gouvernement"},
    {"name": "Cour des comptes", "year": 1807, "role": "Contrôle des finances publiques"},
    {"name": "Assemblée nationale", "year": 1789, "role": "Chambre législative"},
    {"name": "Sénat", "year": 1799, "role": "Chambre haute"},
    {"name": "Conseil constitutionnel", "year": 1958, "role": "Contrôle de constitutionnalité"},
    {"name": "ENA", "year": 1945, "role": "Formation des hauts fonctionnaires"},
]

figures = [
    {"name": "Jeanne d'Arc", "role": "Héroïne et sainte", "century": "XVe"},
    {"name": "Montesquieu", "role": "Philosophe des Lumières", "century": "XVIIIe"},
    {"name": "Voltaire", "role": "Écrivain et philosophe", "century": "XVIIIe"},
    {"name": "Rousseau", "role": "Philosophe et écrivain", "century": "XVIIIe"},
    {"name": "Diderot", "role": "Encyclopédiste", "century": "XVIIIe"},
    {"name": "Beaumarchais", "role": "Dramaturge et polémiste", "century": "XVIIIe"},
    {"name": "Louis Pasteur", "role": "Scientifique", "century": "XIXe"},
    {"name": "Marie Curie", "role": "Physicienne et chimiste", "century": "XXe"},
    {"name": "Georges Clemenceau", "role": "Homme d'État", "century": "XXe"},
    {"name": "Simone de Beauvoir", "role": "Philosophe et féministe", "century": "XXe"},
    {"name": "Aimé Césaire", "role": "Poète et homme politique", "century": "XXe"},
    {"name": "André Malraux", "role": "Écrivain et ministre", "century": "XXe"},
    {"name": "Charles de Gaulle", "role": "Chef de la France libre", "century": "XXe"},
    {"name": "René Cassin", "role": "Juriste de la Déclaration universelle", "century": "XXe"},
]

regions = [
    {"name": "Île-de-France", "capital": "Paris"},
    {"name": "Normandie", "capital": "Rouen"},
    {"name": "Bretagne", "capital": "Rennes"},
    {"name": "Pays de la Loire", "capital": "Nantes"},
    {"name": "Hauts-de-France", "capital": "Lille"},
    {"name": "Grand Est", "capital": "Strasbourg"},
    {"name": "Bourgogne-Franche-Comté", "capital": "Dijon"},
    {"name": "Centre-Val de Loire", "capital": "Orléans"},
    {"name": "Nouvelle-Aquitaine", "capital": "Bordeaux"},
    {"name": "Occitanie", "capital": "Toulouse"},
    {"name": "Auvergne-Rhône-Alpes", "capital": "Lyon"},
    {"name": "Provence-Alpes-Côte d'Azur", "capital": "Marseille"},
    {"name": "Corse", "capital": "Ajaccio"},
]

# -------------------- Helpers --------------------

def choice_except(pool, exclude_value, k=3, key=lambda x: x):
    candidates = [x for x in pool if key(x) != exclude_value]
    picked = random.sample(candidates, min(k, len(candidates)))
    return picked

def add_question(qset, question_text, correct, distractors):
    # Ensure unique question text and unique options
    norm_q = question_text.strip().lower()
    if norm_q in qset["seen_questions"]:
        return False
    options = [correct] + distractors
    if len(set(options)) < len(options):
        return False
    random.shuffle(options)
    qset["questions"].append({
        "question": question_text,
        "options": options,
        "answer": correct
    })
    qset["seen_questions"].add(norm_q)
    return True

# -------------------- Generation --------------------

def build_questions(target_count=1000):
    qset = {"questions": [], "seen_questions": set()}

    # Monarchs: reign, title, dynasty
    for m in monarchs:
        add_question(qset,
            f"Quel souverain a régné de {m['start']} à {m['end']} ?",
            m["name"],
            [x["name"] for x in choice_except(monarchs, m["name"], 3, key=lambda y: y["name"])]
        )
        add_question(qset,
            f"Quel était le surnom ou rôle principal de {m['name']} ?",
            m["title"],
            [x["title"] for x in choice_except(monarchs, m["title"], 3, key=lambda y: y["title"])]
        )
        add_question(qset,
            f"À quelle dynastie appartient {m['name']} ?",
            m["dynasty"],
            [x["dynasty"] for x in choice_except(monarchs, m["dynasty"], 3, key=lambda y: y["dynasty"])]
        )

    # Presidents
    for p in presidents:
        add_question(qset,
            f"Qui était président de la République de {p['start']} à {p['end']} ?",
            p["name"],
            [x["name"] for x in choice_except(presidents, p["name"], 3, key=lambda y: y["name"])]
        )
        add_question(qset,
            f"Quel président était en fonction en {p['start']} ?",
            p["name"],
            [x["name"] for x in choice_except(presidents, p["name"], 3, key=lambda y: y["name"])]
        )

    # Events
    for e in events:
        add_question(qset,
            f"En quelle année s'est déroulé l'événement suivant : {e['name']} ?",
            str(e["year"]),
            [str(x["year"]) for x in choice_except(events, e["year"], 3, key=lambda y: y["year"])]
        )
        add_question(qset,
            f"Quel type d'événement est {e['name']} ?",
            e["kind"],
            [x["kind"] for x in choice_except(events, e["kind"], 3, key=lambda y: y["kind"])]
        )

    # Wars
    for w in wars:
        add_question(qset,
            f"Quelle guerre française a duré de {w['start']} à {w['end']} ?",
            w["name"],
            [x["name"] for x in choice_except(wars, w["name"], 3, key=lambda y: y["name"])]
        )
        add_question(qset,
            f"En quelle période commence la {w['name']} ?",
            str(w["start"]),
            [str(x["start"]) for x in choice_except(wars, w["start"], 3, key=lambda y: y["start"])]
        )

    # Battles
    for b in battles:
        add_question(qset,
            f"En quelle année s'est déroulée la bataille de {b['name']} ?",
            str(b["year"]),
            [str(x["year"]) for x in choice_except(battles, b["year"], 3, key=lambda y: y["year"])]
        )
        add_question(qset,
            f"À quel conflit appartient la bataille de {b['name']} ?",
            b["war"],
            [x["war"] for x in choice_except(battles, b["war"], 3, key=lambda y: y["war"])]
        )

    # Institutions
    for inst in institutions:
        add_question(qset,
            f"Quelle institution a été créée en {inst['year']} pour {inst['role']} ?",
            inst["name"],
            [x["name"] for x in choice_except(institutions, inst["name"], 3, key=lambda y: y["name"])]
        )
        add_question(qset,
            f"Quel est le rôle principal du {inst['name']} ?",
            inst["role"],
            [x["role"] for x in choice_except(institutions, inst["role"], 3, key=lambda y: y["role"])]
        )

    # Regions
    for r in regions:
        add_question(qset,
            f"Quelle est la capitale de la région {r['name']} ?",
            r["capital"],
            [x["capital"] for x in choice_except(regions, r["capital"], 3, key=lambda y: y["capital"])]
        )
        add_question(qset,
            f"À quelle région appartient la capitale {r['capital']} ?",
            r["name"],
            [x["name"] for x in choice_except(regions, r["name"], 3, key=lambda y: y["name"])]
        )

    # Figures
    for f in figures:
        add_question(qset,
            f"Qui est célèbre pour le rôle suivant : {f['role']} ?",
            f["name"],
            [x["name"] for x in choice_except(figures, f["name"], 3, key=lambda y: y["name"])]
        )
        add_question(qset,
            f"À quel siècle rattache-t-on {f['name']} ?",
            f["century"],
            [x["century"] for x in choice_except(figures, f["century"], 3, key=lambda y: y["century"])]
        )

    # Expand with synthetic year-check questions across events and wars
    mixed_years = [(e["name"], e["year"]) for e in events] + [(w["name"], w["start"]) for w in wars]
    for name, year in mixed_years:
        distract_years = [str(y) for (_, y) in random.sample(mixed_years, min(3, len(mixed_years)))]
        add_question(qset,
            f"En quelle année commence {name} ?",
            str(year),
            distract_years
        )

    # If still not enough, cycle through safe templates until 1000
    pools = [monarchs, presidents, events, wars, battles, institutions, regions, figures]
    template_cycle = [
        lambda x: (f"Quel est le nom associé à {x.get('title','') or x.get('role','')} ?", x.get("name"), [y.get("name") for y in choice_except(pools[0], x.get("name"), 3, key=lambda z: z.get("name"))]) if "name" in x and ("title" in x or "role" in x) else None,
        lambda x: (f"Dans quelle période se situe {x.get('name')} ?", f"{x.get('start','')} - {x.get('end','')}" , [f"{y.get('start','')} - {y.get('end','')}" for y in choice_except(wars, x.get('start'), 3, key=lambda z: z.get('start'))]) if "start" in x and "end" in x and x in wars else None,
    ]

    idx = 0
    while len(qset["questions"]) < target_count:
        pool = pools[idx % len(pools)]
        item = random.choice(pool)
        tpl = template_cycle[idx % len(template_cycle)]
        built = tpl(item)
        if built:
            q, ans, distract = built
            if ans and distract:
                add_question(qset, q, ans, distract)
        idx += 1
        if idx > 5000:  # safety break
            break

    # Trim to target_count
    qset["questions"] = qset["questions"][:target_count]
    return qset["questions"]


def main():
    if not BASE_JSON.exists():
        raise FileNotFoundError(f"Base quiz file not found: {BASE_JSON}")

    # Backup
    BACKUP_JSON.write_bytes(BASE_JSON.read_bytes())
    print(f"Backup created: {BACKUP_JSON}")

    # Load existing data
    with BASE_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "quizzes" not in data or not isinstance(data["quizzes"], list):
        raise ValueError("Invalid quiz JSON structure")

    new_questions = build_questions(1000)

    # Determine next available id per quiz? We'll keep ids local starting at 1 in the new quiz
    for i, q in enumerate(new_questions, start=1):
        q["id"] = i
        q["uuid"] = str(uuid.uuid4())

    new_quiz = {
        "name": "French History 1000",
        "imageFileName": "france.svg",
        "questions": new_questions,
    }

    # Append without removing existing quizzes
    data["quizzes"].append(new_quiz)

    with BASE_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("New quiz added: French History 1000 with", len(new_questions), "questions")
    print("Output written to", BASE_JSON)


if __name__ == "__main__":
    main()

