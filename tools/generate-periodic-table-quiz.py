#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil
from datetime import datetime
import uuid

# Données des éléments chimiques (118 éléments)
elements_data = [
    # Hydrogène - Hélium
    {"symbol": "H", "name": "Hydrogen", "name_fr": "Hydrogène", "number": 1, "neutrons": 0, "year": "1766", "discoverer": "Henry Cavendish"},
    {"symbol": "He", "name": "Helium", "name_fr": "Hélium", "number": 2, "neutrons": 2, "year": "1868", "discoverer": "Pierre Janssen & Norman Lockyer"},

    # Période 2
    {"symbol": "Li", "name": "Lithium", "name_fr": "Lithium", "number": 3, "neutrons": 4, "year": "1817", "discoverer": "Johan August Arfwedson"},
    {"symbol": "Be", "name": "Beryllium", "name_fr": "Béryllium", "number": 4, "neutrons": 5, "year": "1798", "discoverer": "Louis-Nicolas Vauquelin"},
    {"symbol": "B", "name": "Boron", "name_fr": "Bore", "number": 5, "neutrons": 6, "year": "1808", "discoverer": "Humphry Davy"},
    {"symbol": "C", "name": "Carbon", "name_fr": "Carbone", "number": 6, "neutrons": 6, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "N", "name": "Nitrogen", "name_fr": "Azote", "number": 7, "neutrons": 7, "year": "1772", "discoverer": "Daniel Rutherford"},
    {"symbol": "O", "name": "Oxygen", "name_fr": "Oxygène", "number": 8, "neutrons": 8, "year": "1774", "discoverer": "Joseph Priestley & Carl Wilhelm Scheele"},
    {"symbol": "F", "name": "Fluorine", "name_fr": "Fluor", "number": 9, "neutrons": 10, "year": "1886", "discoverer": "Henri Moissan"},
    {"symbol": "Ne", "name": "Neon", "name_fr": "Néon", "number": 10, "neutrons": 10, "year": "1898", "discoverer": "William Ramsay & Morris Travers"},

    # Période 3
    {"symbol": "Na", "name": "Sodium", "name_fr": "Sodium", "number": 11, "neutrons": 12, "year": "1807", "discoverer": "Humphry Davy"},
    {"symbol": "Mg", "name": "Magnesium", "name_fr": "Magnésium", "number": 12, "neutrons": 12, "year": "1808", "discoverer": "Humphry Davy"},
    {"symbol": "Al", "name": "Aluminum", "name_fr": "Aluminium", "number": 13, "neutrons": 14, "year": "1825", "discoverer": "Hans Christian Ørsted"},
    {"symbol": "Si", "name": "Silicon", "name_fr": "Silicium", "number": 14, "neutrons": 14, "year": "1824", "discoverer": "Jöns Jacob Berzelius"},
    {"symbol": "P", "name": "Phosphorus", "name_fr": "Phosphore", "number": 15, "neutrons": 16, "year": "1669", "discoverer": "Hennig Brand"},
    {"symbol": "S", "name": "Sulfur", "name_fr": "Soufre", "number": 16, "neutrons": 16, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Cl", "name": "Chlorine", "name_fr": "Chlore", "number": 17, "neutrons": 18, "year": "1774", "discoverer": "Carl Wilhelm Scheele"},
    {"symbol": "Ar", "name": "Argon", "name_fr": "Argon", "number": 18, "neutrons": 22, "year": "1894", "discoverer": "Lord Rayleigh & William Ramsay"},

    # Période 4
    {"symbol": "K", "name": "Potassium", "name_fr": "Potassium", "number": 19, "neutrons": 20, "year": "1807", "discoverer": "Humphry Davy"},
    {"symbol": "Ca", "name": "Calcium", "name_fr": "Calcium", "number": 20, "neutrons": 20, "year": "1808", "discoverer": "Humphry Davy"},
    {"symbol": "Sc", "name": "Scandium", "name_fr": "Scandium", "number": 21, "neutrons": 24, "year": "1879", "discoverer": "Lars Fredrik Nilson"},
    {"symbol": "Ti", "name": "Titanium", "name_fr": "Titane", "number": 22, "neutrons": 26, "year": "1791", "discoverer": "William Gregor"},
    {"symbol": "V", "name": "Vanadium", "name_fr": "Vanadium", "number": 23, "neutrons": 28, "year": "1801", "discoverer": "Andrés Manuel del Río"},
    {"symbol": "Cr", "name": "Chromium", "name_fr": "Chrome", "number": 24, "neutrons": 28, "year": "1797", "discoverer": "Louis-Nicolas Vauquelin"},
    {"symbol": "Mn", "name": "Manganese", "name_fr": "Manganèse", "number": 25, "neutrons": 30, "year": "1774", "discoverer": "Johan Gottlieb Gahn"},
    {"symbol": "Fe", "name": "Iron", "name_fr": "Fer", "number": 26, "neutrons": 30, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Co", "name": "Cobalt", "name_fr": "Cobalt", "number": 27, "neutrons": 32, "year": "1735", "discoverer": "Georg Brandt"},
    {"symbol": "Ni", "name": "Nickel", "name_fr": "Nickel", "number": 28, "neutrons": 31, "year": "1751", "discoverer": "Axel Fredrik Cronstedt"},
    {"symbol": "Cu", "name": "Copper", "name_fr": "Cuivre", "number": 29, "neutrons": 35, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Zn", "name": "Zinc", "name_fr": "Zinc", "number": 30, "neutrons": 35, "year": "1746", "discoverer": "Andreas Marggraf"},
    {"symbol": "Ga", "name": "Gallium", "name_fr": "Gallium", "number": 31, "neutrons": 39, "year": "1875", "discoverer": "Paul-Émile Lecoq de Boisbaudran"},
    {"symbol": "Ge", "name": "Germanium", "name_fr": "Germanium", "number": 32, "neutrons": 41, "year": "1886", "discoverer": "Clemens Winkler"},
    {"symbol": "As", "name": "Arsenic", "name_fr": "Arsenic", "number": 33, "neutrons": 42, "year": "1250", "discoverer": "Albertus Magnus"},
    {"symbol": "Se", "name": "Selenium", "name_fr": "Sélénium", "number": 34, "neutrons": 45, "year": "1817", "discoverer": "Jöns Jacob Berzelius"},
    {"symbol": "Br", "name": "Bromine", "name_fr": "Brome", "number": 35, "neutrons": 45, "year": "1826", "discoverer": "Antoine-Jérôme Balard"},
    {"symbol": "Kr", "name": "Krypton", "name_fr": "Krypton", "number": 36, "neutrons": 48, "year": "1898", "discoverer": "William Ramsay & Morris Travers"},

    # Période 5
    {"symbol": "Rb", "name": "Rubidium", "name_fr": "Rubidium", "number": 37, "neutrons": 48, "year": "1861", "discoverer": "Robert Bunsen & Gustav Kirchhoff"},
    {"symbol": "Sr", "name": "Strontium", "name_fr": "Strontium", "number": 38, "neutrons": 50, "year": "1790", "discoverer": "Adair Crawford"},
    {"symbol": "Y", "name": "Yttrium", "name_fr": "Yttrium", "number": 39, "neutrons": 50, "year": "1794", "discoverer": "Johan Gadolin"},
    {"symbol": "Zr", "name": "Zirconium", "name_fr": "Zirconium", "number": 40, "neutrons": 51, "year": "1789", "discoverer": "Martin Heinrich Klaproth"},
    {"symbol": "Nb", "name": "Niobium", "name_fr": "Niobium", "number": 41, "neutrons": 52, "year": "1801", "discoverer": "Charles Hatchett"},
    {"symbol": "Mo", "name": "Molybdenum", "name_fr": "Molybdène", "number": 42, "neutrons": 54, "year": "1778", "discoverer": "Carl Wilhelm Scheele"},
    {"symbol": "Tc", "name": "Technetium", "name_fr": "Technétium", "number": 43, "neutrons": 55, "year": "1937", "discoverer": "Carlo Perrier & Emilio Segrè"},
    {"symbol": "Ru", "name": "Ruthenium", "name_fr": "Ruthénium", "number": 44, "neutrons": 57, "year": "1844", "discoverer": "Karl Ernst Claus"},
    {"symbol": "Rh", "name": "Rhodium", "name_fr": "Rhodium", "number": 45, "neutrons": 58, "year": "1803", "discoverer": "William Hyde Wollaston"},
    {"symbol": "Pd", "name": "Palladium", "name_fr": "Palladium", "number": 46, "neutrons": 60, "year": "1803", "discoverer": "William Hyde Wollaston"},
    {"symbol": "Ag", "name": "Silver", "name_fr": "Argent", "number": 47, "neutrons": 61, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Cd", "name": "Cadmium", "name_fr": "Cadmium", "number": 48, "neutrons": 64, "year": "1817", "discoverer": "Friedrich Stromeyer"},
    {"symbol": "In", "name": "Indium", "name_fr": "Indium", "number": 49, "neutrons": 66, "year": "1863", "discoverer": "Ferdinand Reich & Hieronymous Richter"},
    {"symbol": "Sn", "name": "Tin", "name_fr": "Étain", "number": 50, "neutrons": 69, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Sb", "name": "Antimony", "name_fr": "Antimoine", "number": 51, "neutrons": 71, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Te", "name": "Tellurium", "name_fr": "Tellure", "number": 52, "neutrons": 76, "year": "1782", "discoverer": "Franz-Joseph Müller von Reichenstein"},
    {"symbol": "I", "name": "Iodine", "name_fr": "Iode", "number": 53, "neutrons": 74, "year": "1811", "discoverer": "Bernard Courtois"},
    {"symbol": "Xe", "name": "Xenon", "name_fr": "Xénon", "number": 54, "neutrons": 77, "year": "1898", "discoverer": "William Ramsay & Morris Travers"},

    # Période 6
    {"symbol": "Cs", "name": "Cesium", "name_fr": "Césium", "number": 55, "neutrons": 78, "year": "1860", "discoverer": "Robert Bunsen & Gustav Kirchhoff"},
    {"symbol": "Ba", "name": "Barium", "name_fr": "Baryum", "number": 56, "neutrons": 81, "year": "1808", "discoverer": "Humphry Davy"},
    {"symbol": "La", "name": "Lanthanum", "name_fr": "Lanthane", "number": 57, "neutrons": 82, "year": "1839", "discoverer": "Carl Gustaf Mosander"},
    {"symbol": "Ce", "name": "Cerium", "name_fr": "Cérium", "number": 58, "neutrons": 82, "year": "1803", "discoverer": "Martin Heinrich Klaproth"},
    {"symbol": "Pr", "name": "Praseodymium", "name_fr": "Praséodyme", "number": 59, "neutrons": 82, "year": "1885", "discoverer": "Carl Auer von Welsbach"},
    {"symbol": "Nd", "name": "Neodymium", "name_fr": "Néodyme", "number": 60, "neutrons": 84, "year": "1885", "discoverer": "Carl Auer von Welsbach"},
    {"symbol": "Pm", "name": "Promethium", "name_fr": "Prométhium", "number": 61, "neutrons": 84, "year": "1945", "discoverer": "Jacob A. Marinsky"},
    {"symbol": "Sm", "name": "Samarium", "name_fr": "Samarium", "number": 62, "neutrons": 88, "year": "1879", "discoverer": "Paul-Émile Lecoq de Boisbaudran"},
    {"symbol": "Eu", "name": "Europium", "name_fr": "Europium", "number": 63, "neutrons": 89, "year": "1901", "discoverer": "Eugène-Anatole Demarçay"},
    {"symbol": "Gd", "name": "Gadolinium", "name_fr": "Gadolinium", "number": 64, "neutrons": 93, "year": "1880", "discoverer": "Jean Charles Galissard de Marignac"},
    {"symbol": "Tb", "name": "Terbium", "name_fr": "Terbium", "number": 65, "neutrons": 94, "year": "1843", "discoverer": "Carl Gustaf Mosander"},
    {"symbol": "Dy", "name": "Dysprosium", "name_fr": "Dysprosium", "number": 66, "neutrons": 97, "year": "1886", "discoverer": "Paul-Émile Lecoq de Boisbaudran"},
    {"symbol": "Ho", "name": "Holmium", "name_fr": "Holmium", "number": 67, "neutrons": 98, "year": "1878", "discoverer": "Marc Delafontaine & Jacques-Louis Soret"},
    {"symbol": "Er", "name": "Erbium", "name_fr": "Erbium", "number": 68, "neutrons": 99, "year": "1843", "discoverer": "Carl Gustaf Mosander"},
    {"symbol": "Tm", "name": "Thulium", "name_fr": "Thulium", "number": 69, "neutrons": 100, "year": "1879", "discoverer": "Per Teodor Cleve"},
    {"symbol": "Yb", "name": "Ytterbium", "name_fr": "Ytterbium", "number": 70, "neutrons": 103, "year": "1878", "discoverer": "Jean Charles Galissard de Marignac"},
    {"symbol": "Lu", "name": "Lutetium", "name_fr": "Lutécium", "number": 71, "neutrons": 104, "year": "1907", "discoverer": "Georges Urbain"},
    {"symbol": "Hf", "name": "Hafnium", "name_fr": "Hafnium", "number": 72, "neutrons": 106, "year": "1923", "discoverer": "Dirk Coster & George de Hevesy"},
    {"symbol": "Ta", "name": "Tantalum", "name_fr": "Tantale", "number": 73, "neutrons": 108, "year": "1802", "discoverer": "Anders Gustaf Ekeberg"},
    {"symbol": "W", "name": "Tungsten", "name_fr": "Tungstène", "number": 74, "neutrons": 110, "year": "1783", "discoverer": "Juan José Elhuyar & Fausto Elhuyar"},
    {"symbol": "Re", "name": "Rhenium", "name_fr": "Rhénium", "number": 75, "neutrons": 111, "year": "1925", "discoverer": "Walter Noddack & Ida Tacke"},
    {"symbol": "Os", "name": "Osmium", "name_fr": "Osmium", "number": 76, "neutrons": 114, "year": "1803", "discoverer": "Smithson Tennant"},
    {"symbol": "Ir", "name": "Iridium", "name_fr": "Iridium", "number": 77, "neutrons": 115, "year": "1803", "discoverer": "Smithson Tennant"},
    {"symbol": "Pt", "name": "Platinum", "name_fr": "Platine", "number": 78, "neutrons": 117, "year": "1735", "discoverer": "Antonio de Ulloa"},
    {"symbol": "Au", "name": "Gold", "name_fr": "Or", "number": 79, "neutrons": 118, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Hg", "name": "Mercury", "name_fr": "Mercure", "number": 80, "neutrons": 121, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Tl", "name": "Thallium", "name_fr": "Thallium", "number": 81, "neutrons": 123, "year": "1861", "discoverer": "William Crookes"},
    {"symbol": "Pb", "name": "Lead", "name_fr": "Plomb", "number": 82, "neutrons": 125, "year": "Antiquity", "discoverer": "Known since ancient times"},
    {"symbol": "Bi", "name": "Bismuth", "name_fr": "Bismuth", "number": 83, "neutrons": 126, "year": "1753", "discoverer": "Claude François Geoffroy"},
    {"symbol": "Po", "name": "Polonium", "name_fr": "Polonium", "number": 84, "neutrons": 125, "year": "1898", "discoverer": "Marie Curie & Pierre Curie"},
    {"symbol": "At", "name": "Astatine", "name_fr": "Astate", "number": 85, "neutrons": 125, "year": "1940", "discoverer": "Dale R. Corson"},
    {"symbol": "Rn", "name": "Radon", "name_fr": "Radon", "number": 86, "neutrons": 136, "year": "1900", "discoverer": "Friedrich Ernst Dorn"},

    # Période 7
    {"symbol": "Fr", "name": "Francium", "name_fr": "Francium", "number": 87, "neutrons": 136, "year": "1939", "discoverer": "Marguerite Perey"},
    {"symbol": "Ra", "name": "Radium", "name_fr": "Radium", "number": 88, "neutrons": 138, "year": "1898", "discoverer": "Marie Curie & Pierre Curie"},
    {"symbol": "Ac", "name": "Actinium", "name_fr": "Actinium", "number": 89, "neutrons": 138, "year": "1899", "discoverer": "André-Louis Debierne"},
    {"symbol": "Th", "name": "Thorium", "name_fr": "Thorium", "number": 90, "neutrons": 142, "year": "1828", "discoverer": "Jöns Jacob Berzelius"},
    {"symbol": "Pa", "name": "Protactinium", "name_fr": "Protactinium", "number": 91, "neutrons": 140, "year": "1913", "discoverer": "Kasimir Fajans & Otto Göhring"},
    {"symbol": "U", "name": "Uranium", "name_fr": "Uranium", "number": 92, "neutrons": 146, "year": "1789", "discoverer": "Martin Heinrich Klaproth"},
    {"symbol": "Np", "name": "Neptunium", "name_fr": "Neptunium", "number": 93, "neutrons": 144, "year": "1940", "discoverer": "Edwin McMillan & Philip Abelson"},
    {"symbol": "Pu", "name": "Plutonium", "name_fr": "Plutonium", "number": 94, "neutrons": 150, "year": "1940", "discoverer": "Glenn T. Seaborg"},
    {"symbol": "Am", "name": "Americium", "name_fr": "Américium", "number": 95, "neutrons": 148, "year": "1944", "discoverer": "Glenn T. Seaborg"},
    {"symbol": "Cm", "name": "Curium", "name_fr": "Curium", "number": 96, "neutrons": 151, "year": "1944", "discoverer": "Glenn T. Seaborg"},
    {"symbol": "Bk", "name": "Berkelium", "name_fr": "Berkélium", "number": 97, "neutrons": 150, "year": "1949", "discoverer": "Glenn T. Seaborg"},
    {"symbol": "Cf", "name": "Californium", "name_fr": "Californium", "number": 98, "neutrons": 153, "year": "1950", "discoverer": "Glenn T. Seaborg"},
    {"symbol": "Es", "name": "Einsteinium", "name_fr": "Einsteinium", "number": 99, "neutrons": 153, "year": "1952", "discoverer": "Albert Ghiorso"},
    {"symbol": "Fm", "name": "Fermium", "name_fr": "Fermium", "number": 100, "neutrons": 157, "year": "1952", "discoverer": "Albert Ghiorso"},
    {"symbol": "Md", "name": "Mendelevium", "name_fr": "Mendélévium", "number": 101, "neutrons": 157, "year": "1955", "discoverer": "Albert Ghiorso"},
    {"symbol": "No", "name": "Nobelium", "name_fr": "Nobélium", "number": 102, "neutrons": 157, "year": "1958", "discoverer": "Albert Ghiorso"},
    {"symbol": "Lr", "name": "Lawrencium", "name_fr": "Lawrencium", "number": 103, "neutrons": 159, "year": "1961", "discoverer": "Albert Ghiorso"},
    {"symbol": "Rf", "name": "Rutherfordium", "name_fr": "Rutherfordium", "number": 104, "neutrons": 157, "year": "1964", "discoverer": "Albert Ghiorso"},
    {"symbol": "Db", "name": "Dubnium", "name_fr": "Dubnium", "number": 105, "neutrons": 157, "year": "1967", "discoverer": "Albert Ghiorso"},
    {"symbol": "Sg", "name": "Seaborgium", "name_fr": "Seaborgium", "number": 106, "neutrons": 160, "year": "1974", "discoverer": "Albert Ghiorso"},
    {"symbol": "Bh", "name": "Bohrium", "name_fr": "Bohrium", "number": 107, "neutrons": 155, "year": "1981", "discoverer": "Peter Armbruster"},
    {"symbol": "Hs", "name": "Hassium", "name_fr": "Hassium", "number": 108, "neutrons": 161, "year": "1984", "discoverer": "Peter Armbruster"},
    {"symbol": "Mt", "name": "Meitnerium", "name_fr": "Meitnérium", "number": 109, "neutrons": 159, "year": "1982", "discoverer": "Peter Armbruster"},
    {"symbol": "Ds", "name": "Darmstadtium", "name_fr": "Darmstadtium", "number": 110, "neutrons": 161, "year": "1994", "discoverer": "Sigurd Hofmann"},
    {"symbol": "Rg", "name": "Roentgenium", "name_fr": "Roentgenium", "number": 111, "neutrons": 161, "year": "1994", "discoverer": "Sigurd Hofmann"},
    {"symbol": "Cn", "name": "Copernicium", "name_fr": "Copernicium", "number": 112, "neutrons": 165, "year": "1996", "discoverer": "Sigurd Hofmann"},
    {"symbol": "Nh", "name": "Nihonium", "name_fr": "Nihonium", "number": 113, "neutrons": 171, "year": "2003", "discoverer": "RIKEN team"},
    {"symbol": "Fl", "name": "Flerovium", "name_fr": "Flérovium", "number": 114, "neutrons": 175, "year": "1998", "discoverer": "Yuri Oganessian"},
    {"symbol": "Mc", "name": "Moscovium", "name_fr": "Moscovium", "number": 115, "neutrons": 174, "year": "2003", "discoverer": "Yuri Oganessian"},
    {"symbol": "Lv", "name": "Livermorium", "name_fr": "Livermorium", "number": 116, "neutrons": 177, "year": "2000", "discoverer": "Yuri Oganessian"},
    {"symbol": "Ts", "name": "Tennessine", "name_fr": "Tennessine", "number": 117, "neutrons": 177, "year": "2010", "discoverer": "Yuri Oganessian"},
    {"symbol": "Og", "name": "Oganesson", "name_fr": "Oganesson", "number": 118, "neutrons": 176, "year": "2002", "discoverer": "Yuri Oganessian"},
]

print("Génération du quiz sur les éléments chimiques...")
print(f"Nombre d'éléments: {len(elements_data)}\n")

# Créer les questions
questions = []
question_id = 1

# Pour chaque élément, créer 4 questions
for elem in elements_data:
    # Question 1: Numéro atomique
    q1 = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Quel est le numéro atomique du {elem['name_fr']} ({elem['symbol']})?",
        "options": [
            str(elem['number']),
            str(elem['number'] + 1),
            str(elem['number'] - 1) if elem['number'] > 1 else str(elem['number'] + 2),
            str(elem['number'] + 5)
        ],
        "answer": str(elem['number'])
    }
    questions.append(q1)
    question_id += 1

    # Question 2: Nombre de neutrons
    q2 = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Combien de neutrons l'isotope le plus stable du {elem['name_fr']} ({elem['symbol']}) possède-t-il généralement?",
        "options": [
            str(elem['neutrons']),
            str(elem['neutrons'] + 2),
            str(elem['neutrons'] - 2) if elem['neutrons'] > 2 else str(elem['neutrons'] + 3),
            str(elem['neutrons'] + 4)
        ],
        "answer": str(elem['neutrons'])
    }
    questions.append(q2)
    question_id += 1

    # Question 3: Date de découverte
    q3 = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"En quelle année le {elem['name_fr']} ({elem['symbol']}) a-t-il été découvert?",
        "options": [
            elem['year'],
            str(int(elem['year']) + 10) if elem['year'].isdigit() else "1800",
            str(int(elem['year']) - 10) if elem['year'].isdigit() and int(elem['year']) > 10 else "1850",
            str(int(elem['year']) + 20) if elem['year'].isdigit() else "1900"
        ] if elem['year'] != "Antiquity" else [
            "Antiquity",
            "1500",
            "1000 BC",
            "500 BC"
        ],
        "answer": elem['year']
    }
    questions.append(q3)
    question_id += 1

    # Question 4: Découvreur
    discoverer_parts = elem['discoverer'].split('&')
    discoverer_main = discoverer_parts[0].strip()

    q4 = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": f"Qui a découvert le {elem['name_fr']} ({elem['symbol']})?",
        "options": [
            elem['discoverer'],
            "Antoine Lavoisier",
            "Dmitri Mendeleev",
            "Marie Curie"
        ],
        "answer": elem['discoverer']
    }
    questions.append(q4)
    question_id += 1

print(f"Nombre total de questions générées: {len(questions)}")

# Créer le quiz
periodic_table_quiz = {
    "name": "Periodic Table of Elements - Complete",
    "imageFileName": "periodic-table.svg",
    "questions": questions
}

print(f"\n✓ Quiz créé avec {len(questions)} questions")
print(f"✓ Prêt pour l'ajout au fichier quiz-questions.json")

# Sauvegarder dans un fichier temporaire
with open("periodic-table-quiz-temp.json", "w", encoding="utf-8") as f:
    json.dump(periodic_table_quiz, f, ensure_ascii=False, indent=2)

print(f"✓ Quiz sauvegardé dans periodic-table-quiz-temp.json")

