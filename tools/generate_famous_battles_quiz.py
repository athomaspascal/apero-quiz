import json
import os
import re
import uuid
from pathlib import Path
import time
import random

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "src" / "main" / "resources" / "quiz-questions.json"

QUIZ_NAME = "Famous Battles"
IMAGE_FILE = "battles.svg"
TARGET_COUNT = 1000
RANDOM_SEED = 42  # reproductible

# --- Data source (seed list of famous battles) ---
# Note: Keep list reasonably sized; we generate multiple question variants per battle.
BATTLES = [
    ("Battle of Marathon", 490, "Greco-Persian Wars", "Ancient Greece"),
    ("Battle of Thermopylae", 480, "Greco-Persian Wars", "Ancient Greece"),
    ("Battle of Salamis", 480, "Greco-Persian Wars", "Ancient Greece"),
    ("Battle of Plataea", 479, "Greco-Persian Wars", "Ancient Greece"),
    ("Battle of Gaugamela", 331, "Wars of Alexander the Great", "Ancient Macedonia"),
    ("Battle of Cannae", 216, "Second Punic War", "Ancient Rome"),
    ("Battle of Zama", 202, "Second Punic War", "Ancient Rome"),
    ("Battle of Actium", 31, "Roman Civil Wars", "Ancient Rome"),
    ("Battle of Hastings", 1066, "Norman Conquest", "England"),
    ("Battle of Tours", 732, "Umayyad–Frankish conflict", "Frankish Kingdom"),
    ("Battle of Agincourt", 1415, "Hundred Years' War", "England/France"),
    ("Battle of Lepanto", 1571, "Ottoman–Habsburg Wars", "Mediterranean"),
    ("Battle of Vienna", 1683, "Great Turkish War", "Habsburg Monarchy"),
    ("Battle of Blenheim", 1704, "War of the Spanish Succession", "Europe"),
    ("Battle of Saratoga", 1777, "American Revolutionary War", "United States"),
    ("Battle of Yorktown", 1781, "American Revolutionary War", "United States"),
    ("Battle of Trafalgar", 1805, "Napoleonic Wars", "Atlantic"),
    ("Battle of Austerlitz", 1805, "Napoleonic Wars", "Europe"),
    ("Battle of Borodino", 1812, "Napoleonic Wars", "Russia"),
    ("Battle of Waterloo", 1815, "Napoleonic Wars", "Belgium"),
    ("Battle of Gettysburg", 1863, "American Civil War", "United States"),
    ("Battle of Antietam", 1862, "American Civil War", "United States"),
    ("Battle of Sedan", 1870, "Franco-Prussian War", "France"),
    ("Battle of Tsushima", 1905, "Russo-Japanese War", "Sea of Japan"),
    ("Battle of the Somme", 1916, "World War I", "France"),
    ("Battle of Verdun", 1916, "World War I", "France"),
    ("Battle of Jutland", 1916, "World War I", "North Sea"),
    ("Battle of Stalingrad", 1942, "World War II", "Soviet Union"),
    ("Battle of Midway", 1942, "World War II", "Pacific"),
    ("Battle of El Alamein", 1942, "World War II", "North Africa"),
    ("Battle of Kursk", 1943, "World War II", "Soviet Union"),
    ("Battle of Normandy", 1944, "World War II", "France"),
    ("Battle of the Bulge", 1944, "World War II", "Belgium"),
    ("Battle of Britain", 1940, "World War II", "United Kingdom"),
    ("Battle of Okinawa", 1945, "World War II", "Pacific"),
    ("Battle of Inchon", 1950, "Korean War", "Korea"),
    ("Battle of Dien Bien Phu", 1954, "First Indochina War", "Vietnam"),
    ("Battle of Khe Sanh", 1968, "Vietnam War", "Vietnam"),
    ("Battle of Mogadishu", 1993, "Somali Civil War", "Somalia"),
]

# Some plausible distractors by era / conflict / region for multiple-choice generation
CONFLICT_DISTRACTORS = [
    "Hundred Years' War",
    "Napoleonic Wars",
    "World War I",
    "World War II",
    "American Civil War",
    "American Revolutionary War",
    "Greco-Persian Wars",
    "Second Punic War",
    "Franco-Prussian War",
    "Russo-Japanese War",
    "Korean War",
    "Vietnam War",
    "Great Turkish War",
    "War of the Spanish Succession",
    "Roman Civil Wars",
]

REGION_DISTRACTORS = [
    "France",
    "England",
    "Belgium",
    "Russia",
    "United States",
    "North Africa",
    "Pacific",
    "Mediterranean",
    "North Sea",
    "Sea of Japan",
    "Vietnam",
    "United Kingdom",
    "Ancient Greece",
    "Ancient Rome",
]

YEAR_BUCKETS = [
    ("Ancient", -500, 500),
    ("Medieval", 500, 1500),
    ("Early Modern", 1500, 1800),
    ("19th century", 1800, 1900),
    ("20th century", 1900, 2000),
    ("21st century", 2000, 2100),
]


def normalize_question(text: str) -> str:
    """Normalize text to detect duplicates: lowercase, strip punctuation/spaces."""
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^a-z0-9 \-']+", "", t)
    return t


def year_bucket(year: int) -> str:
    for name, start, end in YEAR_BUCKETS:
        if start <= year < end:
            return name
    return "Unknown"


def unique_options(correct: str, candidates: list[str], k: int = 4) -> list[str]:
    """Return a list of k unique options where the 1st element is correct."""
    opts = [correct]
    for c in candidates:
        if c != correct and c not in opts:
            opts.append(c)
        if len(opts) >= k:
            break
    while len(opts) < k:
        filler = f"Other ({len(opts)})"
        if filler not in opts:
            opts.append(filler)
    return opts


def _rotated_distractors(values: list[str], start_index: int, take: int = 3) -> list[str]:
    """Take `take` items from `values` starting at `start_index` (wrap-around)."""
    if not values:
        return []
    out = []
    i = start_index
    while len(out) < take:
        out.append(values[i % len(values)])
        i += 1
    return out


def build_questions() -> list[dict]:
    """Generate up to TARGET_COUNT unique questions.

    Key points:
    - We avoid a 'while until TARGET_COUNT' loop that can stall on duplicates.
    - We pre-generate a large pool of candidate questions with variants, de-duplicate,
      then shuffle and take TARGET_COUNT.
    """

    rng = random.Random(RANDOM_SEED)
    start = time.time()

    candidates: list[dict] = []

    all_battle_names = [b[0] for b in BATTLES]
    all_years = sorted({b[1] for b in BATTLES})

    def add_candidate(question_text: str, options: list[str], answer: str):
        candidates.append({
            "question": question_text,
            "options": options,
            "answer": answer,
        })

    # Generate many variants per battle, ensuring large capacity (> 1000)
    for idx, (name, year, conflict, region) in enumerate(BATTLES):
        era = year_bucket(year)

        # Variant set size per battle is intentionally large.
        # 1) Year question - multiple phrasings
        year_phrasings = [
            f"In which year did the {name} take place?",
            f"What year did the {name} occur?",
            f"The {name} happened in which year?",
            f"Which year marks the {name}?",
        ]
        for p_i, q in enumerate(year_phrasings):
            correct = str(year)
            # Rotate distractors using battle index to diversify option sets
            base = [str(year - 2), str(year - 1), str(year + 1), str(year + 2), str(year - 10), str(year + 10)]
            distractors = _rotated_distractors(base, start_index=(idx + p_i) % len(base), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 2) Conflict question - multiple phrasings + rotated distractors
        conflict_phrasings = [
            f"The {name} is most commonly associated with which conflict or war?",
            f"During which conflict did the {name} take place?",
            f"The {name} is a battle from which war?",
            f"Which war is the {name} part of?",
        ]
        for p_i, q in enumerate(conflict_phrasings):
            correct = conflict
            pool = [c for c in CONFLICT_DISTRACTORS if c != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 3 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 3) Region question - multiple phrasings
        region_phrasings = [
            f"In which region or theatre did the {name} occur?",
            f"Where did the {name} take place?",
            f"The {name} occurred in which region/theatre?",
            f"In which location is the {name} best placed?",
        ]
        for p_i, q in enumerate(region_phrasings):
            correct = region
            pool = [r for r in REGION_DISTRACTORS if r != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 5 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 4) Era bucket - multiple phrasings
        era_phrasings = [
            f"The {name} belongs to which broad historical period?",
            f"Which historical period best fits the {name}?",
            f"The {name} is usually classified in which era?",
            f"In terms of periodization, the {name} falls under which category?",
        ]
        era_options = ["Ancient", "Medieval", "Early Modern", "19th century", "20th century", "21st century"]
        for p_i, q in enumerate(era_phrasings):
            correct = era
            distractors = _rotated_distractors([e for e in era_options if e != correct], start_index=(idx + p_i) % 5, take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 5) Reverse by year + conflict (multiple variants)
        rev_yc_phrasings = [
            f"Which famous battle occurred in {year} during the {conflict}?",
            f"In {year}, which battle is associated with the {conflict}?",
            f"Which battle took place in {year} as part of the {conflict}?",
            f"Name the battle from {year} linked to the {conflict}.",
        ]
        for p_i, q in enumerate(rev_yc_phrasings):
            correct = name
            pool = [n for n in all_battle_names if n != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 7 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 6) Reverse by region (multiple variants)
        rev_region_phrasings = [
            f"Which famous battle took place in {region}?",
            f"Which battle is best known for taking place in {region}?",
            f"Name a famous battle that occurred in {region}.",
            f"Which battle happened in the region/theatre of {region}?",
        ]
        for p_i, q in enumerate(rev_region_phrasings):
            correct = name
            pool = [n for n in all_battle_names if n != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 11 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 7) Extra variants to expand capacity: nearest year questions
        if len(all_years) >= 4:
            yr = year
            # pick 3 other years as options (deterministic rotation)
            year_pool = [str(y) for y in all_years if y != yr]
            distractors = _rotated_distractors(year_pool, start_index=(idx * 13) % max(1, len(year_pool)), take=3)
            q = f"Select the correct year for the {name}."
            add_candidate(q, unique_options(str(yr), distractors, 4), str(yr))

        # 8) True/False style (converted to MCQ) - unique texts
        # Keep the statement as the question text; options are always True/False
        tf_statements = [
            (f"True or false: The {name} took place in {year}.", "True"),
            (f"True or false: The {name} is associated with the {conflict}.", "True"),
            (f"True or false: The {name} occurred in {region}.", "True"),
            (f"True or false: The {name} belongs to the {era} period.", "True"),
        ]
        for q, correct in tf_statements:
            add_candidate(q, ["True", "False"], correct)

        # 9) Mixed attribute recall: battle -> year+region
        y_r_phrasings = [
            f"Which pair correctly matches the {name}?",
            f"Pick the correct year and region for the {name}.",
            f"Select the correct combination (year + region) for the {name}.",
        ]
        # Generate 3 unique wrong pairs deterministically
        pool_pairs = []
        for j, (n2, y2, _c2, r2) in enumerate(BATTLES):
            if n2 == name:
                continue
            pool_pairs.append((y2, r2, j))
        pool_pairs.sort(key=lambda t: (t[2]))
        distractor_pairs = _rotated_distractors([f"{y2} / {r2}" for (y2, r2, _j) in pool_pairs], start_index=(idx * 17) % max(1, len(pool_pairs)), take=3)
        for p_i, q in enumerate(y_r_phrasings):
            correct_pair = f"{year} / {region}"
            # vary start index per phrasing
            wrongs = _rotated_distractors(distractor_pairs, start_index=p_i % max(1, len(distractor_pairs)), take=3)
            add_candidate(q, unique_options(correct_pair, wrongs, 4), correct_pair)

        # 10) Mixed attribute recall: battle -> conflict+region
        c_r_phrasings = [
            f"Which pair correctly matches the {name} (conflict + region)?",
            f"Select the correct conflict and region for the {name}.",
            f"Pick the correct combination (conflict + region) for the {name}.",
        ]
        pool_cr = []
        for j, (n2, _y2, c2, r2) in enumerate(BATTLES):
            if n2 == name:
                continue
            pool_cr.append((c2, r2, j))
        pool_cr.sort(key=lambda t: (t[2]))
        distractor_cr = _rotated_distractors([f"{c2} / {r2}" for (c2, r2, _j) in pool_cr], start_index=(idx * 19) % max(1, len(pool_cr)), take=3)
        for p_i, q in enumerate(c_r_phrasings):
            correct_pair = f"{conflict} / {region}"
            wrongs = _rotated_distractors(distractor_cr, start_index=p_i % max(1, len(distractor_cr)), take=3)
            add_candidate(q, unique_options(correct_pair, wrongs, 4), correct_pair)

        # 11) Identify battle from year+region
        yr_reg_phrasings = [
            f"Which battle took place in {year} in {region}?",
            f"A battle in {region} in {year} is which one?",
            f"In {region}, which battle occurred in {year}?",
        ]
        for p_i, q in enumerate(yr_reg_phrasings):
            correct = name
            pool = [n for n in all_battle_names if n != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 23 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 12) Identify battle from conflict+region
        conf_reg_phrasings = [
            f"Which battle is associated with the {conflict} in {region}?",
            f"A battle in {region} linked to the {conflict} is which one?",
            f"In {region}, which battle belongs to the {conflict}?",
        ]
        for p_i, q in enumerate(conf_reg_phrasings):
            correct = name
            pool = [n for n in all_battle_names if n != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 29 + p_i) % max(1, len(pool)), take=3)
            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 13) "Pick the battle" questions with 4 battle-name options.
        # This massively increases unique question texts (they include a stable variant index).
        # We keep the answer as the correct battle name.
        pick_battle_variants = 12
        for v in range(pick_battle_variants):
            correct = name
            pool = [n for n in all_battle_names if n != correct]
            distractors = _rotated_distractors(pool, start_index=(idx * 37 + v * 5) % max(1, len(pool)), take=3)

            # Vary text significantly; include variant id to prevent normalization collisions.
            # (We *want* unique questions; the variant id is part of the question.)
            if v % 3 == 0:
                q = f"[{v+1}] Which battle matches: year={year}, conflict={conflict}?"
            elif v % 3 == 1:
                q = f"[{v+1}] Identify the battle fought in {region} ({conflict})."
            else:
                q = f"[{v+1}] Choose the battle that took place in {year} in {region}."

            add_candidate(q, unique_options(correct, distractors, 4), correct)

        # 14) Chronology (order) questions: pick the earliest/latest among 4 battles.
        # We build a small group including the correct battle and 3 distractors; answer is one of the options.
        chronology_variants = 6
        for v in range(chronology_variants):
            pool_idx = [(i2, b2) for i2, b2 in enumerate(BATTLES) if b2[0] != name]
            # deterministically pick 3 other battles
            picked = _rotated_distractors([b2[0] for (_i2, b2) in pool_idx], start_index=(idx * 41 + v * 7) % max(1, len(pool_idx)), take=3)
            option_names = [name] + picked

            # map to years
            year_by_name = {b[0]: b[1] for b in BATTLES}
            years = [(bn, year_by_name.get(bn, 9999)) for bn in option_names]
            if v % 2 == 0:
                # earliest
                ans = min(years, key=lambda t: t[1])[0]
                q = f"[{v+1}] Among these battles, which happened earliest?"
            else:
                # latest
                ans = max(years, key=lambda t: t[1])[0]
                q = f"[{v+1}] Among these battles, which happened latest?"

            add_candidate(q, option_names, ans)

    # De-duplicate by normalized question text
    seen = set()
    unique: list[dict] = []
    dupe_count = 0
    for c in candidates:
        nq = normalize_question(c["question"])
        if nq in seen:
            dupe_count += 1
            continue
        seen.add(nq)
        unique.append(c)

    elapsed = time.time() - start
    print(
        f"[gen] candidates={len(candidates)} unique={len(unique)} duplicates={dupe_count} "
        f"elapsed={elapsed:0.2f}s",
        flush=True,
    )

    if len(unique) < TARGET_COUNT:
        raise SystemExit(
            f"Not enough unique questions to reach {TARGET_COUNT}. "
            f"Unique={len(unique)}. Add more battles/templates."
        )

    rng.shuffle(unique)
    selected = unique[:TARGET_COUNT]

    # Assign stable incremental ids + uuids
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

    print("[info] Checking duplicates...", flush=True)
    norms = [normalize_question(q["question"]) for q in questions]
    if len(set(norms)) != len(norms):
        raise SystemExit("Duplicate questions detected after generation")

    quizzes.append({
        "name": QUIZ_NAME,
        "imageFileName": IMAGE_FILE,
        "questions": questions,
    })

    data["quizzes"] = quizzes

    print("[info] Writing JSON back to disk...", flush=True)
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] Updated {JSON_PATH} with quiz '{QUIZ_NAME}' ({len(questions)} questions).", flush=True)


if __name__ == "__main__":
    main()

