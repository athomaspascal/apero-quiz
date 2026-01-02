#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génération du quiz Harry Potter avec 1000 questions"""
import json
import uuid
from datetime import datetime
import shutil

def generate_harry_potter_quiz():
    """Génère un quiz Harry Potter complet avec 1000 questions"""

    # Backup du fichier original avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(
        'src/main/resources/quiz-questions.json',
        f'src/main/resources/quiz-questions-backup-{timestamp}.json'
    )
    print(f"✓ Backup créé : quiz-questions-backup-{timestamp}.json")

    # Charger le fichier JSON existant
    with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []
    question_id = 1

    # Catégorie 1: Les livres et l'histoire (200 questions)
    books_questions = [
        ("Quel est le titre complet du premier livre Harry Potter ?", ["Harry Potter à l'école des sorciers", "Harry Potter et la pierre philosophale", "Harry Potter et le sorcier", "Harry Potter commence"], "Harry Potter à l'école des sorciers", 1),
        ("En quelle année le premier livre Harry Potter a-t-il été publié ?", ["1997", "1995", "1999", "2000"], "1997", 1),
        ("Qui est l'auteur de la série Harry Potter ?", ["J.K. Rowling", "J.R.R. Tolkien", "C.S. Lewis", "Suzanne Collins"], "J.K. Rowling", 1),
        ("Combien de livres y a-t-il dans la série Harry Potter ?", ["7", "5", "8", "6"], "7", 1),
        ("Quel est le titre du deuxième livre ?", ["Harry Potter et la Chambre des Secrets", "Harry Potter et le Prisonnier d'Azkaban", "Harry Potter et la Coupe de Feu", "Harry Potter et l'Ordre du Phénix"], "Harry Potter et la Chambre des Secrets", 1),
        ("Quel est le titre du troisième livre ?", ["Harry Potter et le Prisonnier d'Azkaban", "Harry Potter et la Chambre des Secrets", "Harry Potter et la Coupe de Feu", "Harry Potter et l'Ordre du Phénix"], "Harry Potter et le Prisonnier d'Azkaban", 1),
        ("Quel est le titre du quatrième livre ?", ["Harry Potter et la Coupe de Feu", "Harry Potter et l'Ordre du Phénix", "Harry Potter et le Prince de Sang-Mêlé", "Harry Potter et les Reliques de la Mort"], "Harry Potter et la Coupe de Feu", 1),
        ("Quel est le titre du cinquième livre ?", ["Harry Potter et l'Ordre du Phénix", "Harry Potter et la Coupe de Feu", "Harry Potter et le Prince de Sang-Mêlé", "Harry Potter et les Reliques de la Mort"], "Harry Potter et l'Ordre du Phénix", 1),
        ("Quel est le titre du sixième livre ?", ["Harry Potter et le Prince de Sang-Mêlé", "Harry Potter et l'Ordre du Phénix", "Harry Potter et les Reliques de la Mort", "Harry Potter et la Coupe de Feu"], "Harry Potter et le Prince de Sang-Mêlé", 1),
        ("Quel est le titre du septième livre ?", ["Harry Potter et les Reliques de la Mort", "Harry Potter et le Prince de Sang-Mêlé", "Harry Potter et l'Enfant Maudit", "Harry Potter et la fin"], "Harry Potter et les Reliques de la Mort", 1),
        ("Quelle est la date d'anniversaire de Harry Potter ?", ["31 juillet", "1er septembre", "31 octobre", "25 décembre"], "31 juillet", 2),
        ("Quel âge a Harry au début de la série ?", ["11 ans", "10 ans", "12 ans", "13 ans"], "11 ans", 1),
        ("Où vit Harry avant d'aller à Poudlard ?", ["4 Privet Drive", "12 Grimmauld Place", "Le Terrier", "Godric's Hollow"], "4 Privet Drive", 1),
        ("Qui sont les parents adoptifs de Harry ?", ["Les Dursley", "Les Weasley", "Les Granger", "Les Lovegood"], "Les Dursley", 1),
        ("Quel est le prénom de l'oncle de Harry ?", ["Vernon", "Dudley", "Pétunia", "Marge"], "Vernon", 1),
        ("Quel est le prénom de la tante de Harry ?", ["Pétunia", "Marjorie", "Lily", "Rose"], "Pétunia", 1),
        ("Comment s'appelle le cousin de Harry ?", ["Dudley", "Vernon", "Malcolm", "Piers"], "Dudley", 1),
        ("Qui vient chercher Harry pour l'emmener à Poudlard ?", ["Hagrid", "Dumbledore", "McGonagall", "Rogue"], "Hagrid", 1),
        ("Quel est le métier de Hagrid ?", ["Garde-chasse et garde des Clés", "Professeur", "Auror", "Médicomage"], "Garde-chasse et garde des Clés", 1),
        ("Sur quel chemin se trouve la maison des Dursley ?", ["Privet Drive", "Magnolia Crescent", "Wisteria Walk", "King's Cross"], "Privet Drive", 1),
        ("Quel numéro porte la maison des Dursley ?", ["4", "12", "7", "10"], "4", 2),
        ("Comment s'appelle le premier ami que Harry se fait dans le train ?", ["Ron Weasley", "Hermione Granger", "Neville Londubat", "Dean Thomas"], "Ron Weasley", 1),
        ("Quelle est la couleur des yeux de Harry ?", ["Vert", "Bleu", "Marron", "Noisette"], "Vert", 1),
        ("Quelle est la forme de la cicatrice de Harry ?", ["Éclair", "Étoile", "Croix", "Cercle"], "Éclair", 1),
        ("Qui a tué les parents de Harry ?", ["Voldemort", "Bellatrix Lestrange", "Lucius Malefoy", "Peter Pettigrow"], "Voldemort", 1),
        ("Comment s'appelait le père de Harry ?", ["James", "Sirius", "Remus", "Severus"], "James", 1),
        ("Comment s'appelait la mère de Harry ?", ["Lily", "Pétunia", "Rose", "Narcissa"], "Lily", 1),
        ("Dans quelle maison est réparti Harry ?", ["Gryffondor", "Serpentard", "Serdaigle", "Poufsouffle"], "Gryffondor", 1),
        ("Quel objet magique répartit les élèves dans les maisons ?", ["Le Choixpeau magique", "La baguette magique", "Le miroir du Riséd", "La pierre de résurrection"], "Le Choixpeau magique", 1),
        ("Qui est le directeur de Poudlard au début de la série ?", ["Albus Dumbledore", "Minerva McGonagall", "Severus Rogue", "Dolores Ombrage"], "Albus Dumbledore", 1),
        ("Quel est le nom complet du meilleur ami de Harry ?", ["Ronald Bilius Weasley", "Ronald Arthur Weasley", "Ron William Weasley", "Ronald Fred Weasley"], "Ronald Bilius Weasley", 2),
        ("Quel est le nom complet de la meilleure amie de Harry ?", ["Hermione Jean Granger", "Hermione Jane Granger", "Hermione Anne Granger", "Hermione Marie Granger"], "Hermione Jean Granger", 2),
        ("Quel sortilège a raté la mère de Harry pour protéger son fils ?", ["Aucun, elle s'est sacrifiée par amour", "Expecto Patronum", "Protego Maxima", "Finite Incantatem"], "Aucun, elle s'est sacrifiée par amour", 2),
        ("Quel est le surnom de Voldemort ?", ["Celui-Dont-On-Ne-Doit-Pas-Prononcer-Le-Nom", "Le Seigneur Noir", "Tu-Sais-Qui", "Toutes ces réponses"], "Toutes ces réponses", 1),
        ("Quel est le vrai nom de Voldemort ?", ["Tom Elvis Jedusor", "Tom Marvolo Riddle", "Tom Serpentard", "Tom Malefoy"], "Tom Elvis Jedusor", 2),
        ("Combien de frères et sœurs a Ron ?", ["6", "5", "7", "4"], "6", 2),
        ("Quel est le sport des sorciers ?", ["Le Quidditch", "Le football", "Le cricket", "Le balai-ball"], "Le Quidditch", 1),
        ("Quel poste Harry occupe-t-il au Quidditch ?", ["Attrapeur", "Poursuiveur", "Batteur", "Gardien"], "Attrapeur", 1),
        ("Quelle est la créature qui garde la banque Gringotts ?", ["Les gobelins", "Les elfes", "Les trolls", "Les centaures"], "Les gobelins", 1),
        ("Comment s'appelle la rue commerçante des sorciers à Londres ?", ["Le Chemin de Traverse", "La rue des Sorciers", "L'Allée Magique", "Le Passage Secret"], "Le Chemin de Traverse", 1),
        ("Quelle est la monnaie des sorciers ?", ["Gallions, Mornilles et Noises", "Euros", "Livres sterling", "Dollars"], "Gallions, Mornilles et Noises", 1),
        ("Combien de Noises font une Mornille ?", ["29", "17", "25", "30"], "29", 3),
        ("Combien de Mornilles font un Gallion ?", ["17", "29", "25", "30"], "17", 3),
        ("Quel animal de compagnie a Ron ?", ["Un rat nommé Croûtard", "Un hibou nommé Errol", "Un chat nommé Pattenrond", "Une chouette nommée Hedwige"], "Un rat nommé Croûtard", 1),
        ("Quel animal de compagnie a Harry ?", ["Une chouette nommée Hedwige", "Un hibou nommé Errol", "Un rat nommé Croûtard", "Un chat nommé Pattenrond"], "Une chouette nommée Hedwige", 1),
        ("Quel animal de compagnie a Hermione ?", ["Un chat nommé Pattenrond", "Une chouette nommée Hedwige", "Un rat nommé Croûtard", "Un crapaud nommé Trevor"], "Un chat nommé Pattenrond", 1),
        ("Quel est l'animal de compagnie de Neville ?", ["Un crapaud nommé Trevor", "Un rat nommé Croûtard", "Un hibou", "Un chat"], "Un crapaud nommé Trevor", 2),
        ("Quelle est la matière préférée d'Hermione ?", ["Toutes les matières", "Métamorphose", "Potions", "Sortilèges"], "Toutes les matières", 1),
        ("Qui est le professeur de Métamorphose ?", ["Minerva McGonagall", "Filius Flitwick", "Severus Rogue", "Pomona Chourave"], "Minerva McGonagall", 1),
        ("Qui est le professeur de Potions (au début) ?", ["Severus Rogue", "Horace Slughorn", "Minerva McGonagall", "Remus Lupin"], "Severus Rogue", 1),
        ("Qui est le professeur de Sortilèges ?", ["Filius Flitwick", "Minerva McGonagall", "Severus Rogue", "Gilderoy Lockhart"], "Filius Flitwick", 2),
    ]

    for q, opts, ans, diff in books_questions:
        questions.append({
            "id": question_id,
            "uuid": str(uuid.uuid4()),
            "question": q,
            "difficulty_level": diff,
            "options": opts,
            "answer": ans,
            "dateUpdate": "2025-12-31"
        })
        question_id += 1

    # Catégorie 2: Personnages (200 questions)
    characters_questions = [
        ("Qui est le parrain de Harry ?", ["Sirius Black", "Remus Lupin", "Albus Dumbledore", "Hagrid"], "Sirius Black", 1),
        ("Quel est le surnom de Sirius Black ?", ["Patmol", "Lunard", "Queudver", "Cornedrue"], "Patmol", 2),
        ("Quel est le surnom de Remus Lupin ?", ["Lunard", "Patmol", "Queudver", "Cornedrue"], "Lunard", 2),
        ("Quel est le surnom de Peter Pettigrow ?", ["Queudver", "Patmol", "Lunard", "Cornedrue"], "Queudver", 2),
        ("Quel est le surnom de James Potter ?", ["Cornedrue", "Patmol", "Lunard", "Queudver"], "Cornedrue", 2),
        ("Qui est Luna Lovegood ?", ["Une élève de Serdaigle", "Une élève de Gryffondor", "Une élève de Poufsouffle", "Une élève de Serpentard"], "Une élève de Serdaigle", 1),
        ("Qui est Cho Chang ?", ["La première petite amie de Harry", "La meilleure amie d'Hermione", "La sœur de Ron", "La cousine de Drago"], "La première petite amie de Harry", 1),
        ("Qui épouse Harry à la fin ?", ["Ginny Weasley", "Hermione Granger", "Cho Chang", "Luna Lovegood"], "Ginny Weasley", 1),
        ("Qui épouse Ron à la fin ?", ["Hermione Granger", "Lavande Brown", "Parvati Patil", "Fleur Delacour"], "Hermione Granger", 1),
        ("Qui est Drago Malefoy ?", ["Le rival de Harry à Serpentard", "Le meilleur ami de Harry", "Le frère de Harry", "Le professeur"], "Le rival de Harry à Serpentard", 1),
        ("Qui est le père de Drago ?", ["Lucius Malefoy", "Severus Rogue", "Voldemort", "Bellatrix Lestrange"], "Lucius Malefoy", 1),
        ("Qui est la mère de Drago ?", ["Narcissa Malefoy", "Bellatrix Lestrange", "Andromeda Tonks", "Pétunia Dursley"], "Narcissa Malefoy", 2),
        ("Qui est Dobby ?", ["Un elfe de maison", "Un gobelin", "Un fantôme", "Un troll"], "Un elfe de maison", 1),
        ("À qui appartenait Dobby au début ?", ["Aux Malefoy", "Aux Potter", "Aux Weasley", "À Dumbledore"], "Aux Malefoy", 1),
        ("Qui libère Dobby ?", ["Harry Potter", "Ron Weasley", "Hermione Granger", "Lucius Malefoy"], "Harry Potter", 1),
        ("Qui est Neville Londubat ?", ["Un élève de Gryffondor", "Un élève de Poufsouffle", "Un élève de Serdaigle", "Un élève de Serpentard"], "Un élève de Gryffondor", 1),
        ("Qui sont les jumeaux Weasley ?", ["Fred et George", "Bill et Charlie", "Percy et Ron", "Ron et Ginny"], "Fred et George", 1),
        ("Quel est le métier du père de Ron ?", ["Fonctionnaire au Ministère de la Magie", "Professeur à Poudlard", "Auror", "Médicomage"], "Fonctionnaire au Ministère de la Magie", 1),
        ("Comment s'appelle la mère de Ron ?", ["Molly", "Ginny", "Lily", "Pétunia"], "Molly", 1),
        ("Qui est le frère aîné des Weasley ?", ["Bill", "Charlie", "Percy", "Fred"], "Bill", 2),
        ("Quel Weasley travaille avec les dragons ?", ["Charlie", "Bill", "Percy", "Ron"], "Charlie", 2),
        ("Qui est Rubeus Hagrid ?", ["Le garde-chasse de Poudlard", "Le directeur de Poudlard", "Un professeur de potions", "Un auror"], "Le garde-chasse de Poudlard", 1),
        ("Quelle est la particularité de Hagrid ?", ["C'est un demi-géant", "C'est un loup-garou", "C'est un vampire", "C'est un fantôme"], "C'est un demi-géant", 2),
        ("Qui est le professeur de Défense contre les forces du Mal en 3ème année ?", ["Remus Lupin", "Gilderoy Lockhart", "Alastor Maugrey", "Dolores Ombrage"], "Remus Lupin", 2),
        ("Quelle est la particularité de Remus Lupin ?", ["C'est un loup-garou", "C'est un vampire", "C'est un géant", "C'est un fantôme"], "C'est un loup-garou", 1),
        ("Qui est Mad-Eye Moody ?", ["Un auror", "Un professeur de potions", "Un directeur", "Un fantôme"], "Un auror", 2),
        ("Qui se fait passer pour Mad-Eye Moody en 4ème année ?", ["Barty Croupton Jr.", "Peter Pettigrow", "Lucius Malefoy", "Bellatrix Lestrange"], "Barty Croupton Jr.", 3),
        ("Qui est Dolores Ombrage ?", ["Une fonctionnaire du Ministère devenue professeur", "Une directrice de Poudlard", "Une auror", "Une mangemort"], "Une fonctionnaire du Ministère devenue professeur", 2),
        ("Qui est le Prince de Sang-Mêlé ?", ["Severus Rogue", "Tom Jedusor", "Albus Dumbledore", "Drago Malefoy"], "Severus Rogue", 2),
        ("Qui était amoureux de Lily Potter ?", ["Severus Rogue", "James Potter", "Sirius Black", "Les deux premières réponses"], "Les deux premières réponses", 2),
        ("Qui tue Dumbledore ?", ["Severus Rogue", "Voldemort", "Bellatrix Lestrange", "Drago Malefoy"], "Severus Rogue", 1),
        ("Qui tue Voldemort ?", ["Harry Potter", "Neville Londubat", "Ron Weasley", "Hermione Granger"], "Harry Potter", 1),
        ("Qui tue Bellatrix Lestrange ?", ["Molly Weasley", "Harry Potter", "Neville Londubat", "Hermione Granger"], "Molly Weasley", 2),
        ("Qui tue Nagini ?", ["Neville Londubat", "Harry Potter", "Ron Weasley", "Hermione Granger"], "Neville Londubat", 2),
        ("Qui est Nagini ?", ["Le serpent de Voldemort", "Un mangemort", "Un professeur", "Un elfe"], "Le serpent de Voldemort", 1),
        ("Qui est Bellatrix Lestrange ?", ["Une mangemort", "Une auror", "Une professeur", "Une directrice"], "Une mangemort", 1),
        ("Quel lien unit Bellatrix et Sirius ?", ["Ce sont cousins", "Ce sont frère et sœur", "Aucun lien", "Ce sont mari et femme"], "Ce sont cousins", 2),
        ("Qui tue Sirius Black ?", ["Bellatrix Lestrange", "Voldemort", "Peter Pettigrow", "Lucius Malefoy"], "Bellatrix Lestrange", 1),
        ("Qui tue Fred Weasley ?", ["Une explosion durant la bataille", "Voldemort", "Bellatrix Lestrange", "Un mangemort"], "Une explosion durant la bataille", 2),
        ("Qui tue Hedwige ?", ["Un mangemort", "Voldemort", "Un accident", "Personne"], "Un mangemort", 2),
        ("Qui est Tonks ?", ["Une auror et métamorphomage", "Une professeur", "Une mangemort", "Une elfe"], "Une auror et métamorphomage", 2),
        ("Qui épouse Tonks ?", ["Remus Lupin", "Sirius Black", "Bill Weasley", "Charlie Weasley"], "Remus Lupin", 2),
        ("Comment s'appelle le fils de Lupin et Tonks ?", ["Teddy", "James", "Albus", "Sirius"], "Teddy", 2),
        ("Qui est le parrain de Teddy Lupin ?", ["Harry Potter", "Ron Weasley", "Neville Londubat", "Drago Malefoy"], "Harry Potter", 2),
        ("Qui est Fleur Delacour ?", ["Une championne de Beauxbâtons", "Une élève de Poudlard", "Une professeur", "Une auror"], "Une championne de Beauxbâtons", 2),
        ("Qui épouse Fleur Delacour ?", ["Bill Weasley", "Charlie Weasley", "Percy Weasley", "Ron Weasley"], "Bill Weasley", 2),
        ("Qui est Viktor Krum ?", ["Un champion de Durmstrang", "Un élève de Poudlard", "Un professeur", "Un auror"], "Un champion de Durmstrang", 2),
        ("Qui est Cédric Diggory ?", ["Un champion de Poufsouffle", "Un champion de Gryffondor", "Un champion de Serdaigle", "Un champion de Serpentard"], "Un champion de Poufsouffle", 1),
        ("Qui tue Cédric Diggory ?", ["Peter Pettigrow", "Voldemort", "Barty Croupton Jr.", "Lucius Malefoy"], "Peter Pettigrow", 2),
        ("Qui est Gilderoy Lockhart ?", ["Un professeur narcissique et menteur", "Un auror courageux", "Un directeur compétent", "Un mangemort"], "Un professeur narcissique et menteur", 2),
    ]

    for q, opts, ans, diff in characters_questions:
        questions.append({
            "id": question_id,
            "uuid": str(uuid.uuid4()),
            "question": q,
            "difficulty_level": diff,
            "options": opts,
            "answer": ans,
            "dateUpdate": "2025-12-31"
        })
        question_id += 1

    print(f"Génération en cours... {question_id-1} questions créées jusqu'à présent...")

    # Je vais continuer avec plus de catégories dans la suite...
    return questions, question_id

if __name__ == '__main__':
    print("Démarrage de la génération du quiz Harry Potter...")
    questions, next_id = generate_harry_potter_quiz()
    print(f"\n✓ {len(questions)} questions générées")
    print(f"Prochain ID: {next_id}")
    print("\nContinuation nécessaire pour atteindre 1000 questions...")

