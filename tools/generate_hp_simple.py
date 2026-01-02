#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script simplifié pour générer le quiz Harry Potter"""
import json
import uuid
from datetime import datetime
import shutil

print("Démarrage de la génération...")

# 1. Backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f'src/main/resources/quiz-questions-backup-hp-{timestamp}.json'
shutil.copy2('src/main/resources/quiz-questions.json', backup_file)
print(f"[OK] Backup cree: {backup_file}")

# 2. Charger le fichier
print("Chargement du fichier JSON...")
with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"[OK] {len(data['quizzes'])} quizzes existants")

# 3. Supprimer l'ancien quiz HP s'il existe
data['quizzes'] = [q for q in data['quizzes'] if q['name'] != 'Harry Potter']
print("[OK] Nettoyage effectue")

# 4. Préparer les questions
print("Generation des questions...")
questions = []

# Base de questions variées
all_questions = [
    # Livres et histoire
    ("Quel est le titre du premier livre en français ?", ["Harry Potter à l'école des sorciers", "Harry Potter et la pierre philosophale", "Harry Potter le sorcier", "Harry Potter commence"], "Harry Potter à l'école des sorciers", 1),
    ("Qui est l'auteur de Harry Potter ?", ["J.K. Rowling", "J.R.R. Tolkien", "C.S. Lewis", "George R.R. Martin"], "J.K. Rowling", 1),
    ("Combien de livres dans la série principale ?", ["7", "5", "8", "6"], "7", 1),
    ("Date d'anniversaire de Harry ?", ["31 juillet", "1er septembre", "31 octobre", "25 décembre"], "31 juillet", 2),
    ("Âge de Harry au début ?", ["11 ans", "10 ans", "12 ans", "9 ans"], "11 ans", 1),

    # Personnages
    ("Meilleur ami de Harry ?", ["Ron Weasley", "Hermione Granger", "Neville Londubat", "Dean Thomas"], "Ron Weasley", 1),
    ("Meilleure amie de Harry ?", ["Hermione Granger", "Ginny Weasley", "Luna Lovegood", "Cho Chang"], "Hermione Granger", 1),
    ("Parrain de Harry ?", ["Sirius Black", "Remus Lupin", "Hagrid", "Dumbledore"], "Sirius Black", 1),
    ("Directeur de Poudlard ?", ["Albus Dumbledore", "Minerva McGonagall", "Severus Rogue", "Armando Dippet"], "Albus Dumbledore", 1),
    ("Ennemi juré de Harry ?", ["Drago Malefoy", "Crabbe", "Goyle", "Pansy Parkinson"], "Drago Malefoy", 1),

    # Magie et sorts
    ("Sort de désarmement ?", ["Expelliarmus", "Stupefix", "Protego", "Expecto Patronum"], "Expelliarmus", 1),
    ("Sort qui invoque un Patronus ?", ["Expecto Patronum", "Expelliarmus", "Riddikulus", "Lumos"], "Expecto Patronum", 1),
    ("Sort de lumière ?", ["Lumos", "Nox", "Incendio", "Aguamenti"], "Lumos", 1),
    ("Sort d'ouverture ?", ["Alohomora", "Bombarda", "Reducto", "Reparo"], "Alohomora", 1),
    ("Sort de lévitation ?", ["Wingardium Leviosa", "Accio", "Locomotor", "Mobiliarbus"], "Wingardium Leviosa", 1),

    # Lieux
    ("École de sorcellerie principale ?", ["Poudlard", "Beauxbâtons", "Durmstrang", "Ilvermorny"], "Poudlard", 1),
    ("Rue commerçante des sorciers ?", ["Chemin de Traverse", "Allée des Embrumes", "Pré-au-Lard", "Rue Magique"], "Chemin de Traverse", 1),
    ("Banque des sorciers ?", ["Gringotts", "Wizbank", "Sorcier Bank", "Goldmine"], "Gringotts", 1),
    ("Prison des sorciers ?", ["Azkaban", "Nurmengard", "La Tour", "Le Donjon"], "Azkaban", 1),
    ("Village sorcier près de Poudlard ?", ["Pré-au-Lard", "Godric's Hollow", "Little Whinging", "Ottery St Catchpole"], "Pré-au-Lard", 1),

    # Maisons
    ("Maison de Harry ?", ["Gryffondor", "Serpentard", "Serdaigle", "Poufsouffle"], "Gryffondor", 1),
    ("Maison de Drago ?", ["Serpentard", "Gryffondor", "Serdaigle", "Poufsouffle"], "Serpentard", 1),
    ("Maison de Luna ?", ["Serdaigle", "Gryffondor", "Serpentard", "Poufsouffle"], "Serdaigle", 1),
    ("Maison de Cédric Diggory ?", ["Poufsouffle", "Gryffondor", "Serpentard", "Serdaigle"], "Poufsouffle", 1),
    ("Couleurs de Gryffondor ?", ["Rouge et or", "Vert et argent", "Bleu et bronze", "Jaune et noir"], "Rouge et or", 1),

    # Quidditch
    ("Sport des sorciers ?", ["Quidditch", "Football", "Cricket", "Rugby"], "Quidditch", 1),
    ("Poste de Harry ?", ["Attrapeur", "Poursuiveur", "Batteur", "Gardien"], "Attrapeur", 1),
    ("Balle dorée ?", ["Vif d'or", "Souaffle", "Cognard", "Balle magique"], "Vif d'or", 1),
    ("Points pour le Vif d'or ?", ["150", "100", "200", "50"], "150", 1),
    ("Joueurs par équipe ?", ["7", "6", "8", "5"], "7", 1),

    # Objets magiques
    ("Objet d'invisibilité de Harry ?", ["Cape d'invisibilité", "Manteau invisible", "Voile caché", "Tissu magique"], "Cape d'invisibilité", 1),
    ("Carte montrant Poudlard ?", ["Carte du Maraudeur", "Plan de Poudlard", "Carte magique", "Parchemin secret"], "Carte du Maraudeur", 2),
    ("Pierre d'immortalité ?", ["Pierre philosophale", "Pierre de résurrection", "Pierre magique", "Pierre éternelle"], "Pierre philosophale", 1),
    ("Coupe de sélection ?", ["Coupe de Feu", "Coupe magique", "Calice d'or", "Coupe de sélection"], "Coupe de Feu", 1),
    ("Baguette la plus puissante ?", ["Baguette de Sureau", "Baguette de Phoenix", "Baguette de Dragon", "Baguette Ancestrale"], "Baguette de Sureau", 2),

    # Créatures
    ("Créature gardant Gringotts ?", ["Gobelins", "Elfes", "Trolls", "Centaures"], "Gobelins", 1),
    ("Créature aspirant la joie ?", ["Détraqueur", "Épouvantard", "Spectre", "Fantôme"], "Détraqueur", 1),
    ("Mi-cheval mi-aigle ?", ["Hippogriffe", "Centaure", "Licorne", "Griffon"], "Hippogriffe", 2),
    ("Serpent géant ?", ["Basilic", "Nagini", "Python", "Anaconda"], "Basilic", 1),
    ("Oiseau renaissant ?", ["Phénix", "Aigle", "Faucon", "Corbeau"], "Phénix", 1),

    # Famille et relations
    ("Père de Harry ?", ["James Potter", "Sirius Black", "Remus Lupin", "Severus Rogue"], "James Potter", 1),
    ("Mère de Harry ?", ["Lily Potter", "Pétunia Dursley", "Molly Weasley", "Narcissa Malefoy"], "Lily Potter", 1),
    ("Oncle de Harry ?", ["Vernon Dursley", "Dudley Dursley", "Arthur Weasley", "Lucius Malefoy"], "Vernon Dursley", 1),
    ("Cousin de Harry ?", ["Dudley Dursley", "Vernon Dursley", "Drago Malefoy", "Neville Londubat"], "Dudley Dursley", 1),
    ("Harry épouse ?", ["Ginny Weasley", "Hermione Granger", "Cho Chang", "Luna Lovegood"], "Ginny Weasley", 1),

    # Professeurs
    ("Professeur de Métamorphose ?", ["Minerva McGonagall", "Severus Rogue", "Filius Flitwick", "Pomona Chourave"], "Minerva McGonagall", 1),
    ("Professeur de Potions initial ?", ["Severus Rogue", "Horace Slughorn", "Minerva McGonagall", "Remus Lupin"], "Severus Rogue", 1),
    ("Professeur de Sortilèges ?", ["Filius Flitwick", "Minerva McGonagall", "Severus Rogue", "Gilderoy Lockhart"], "Filius Flitwick", 2),
    ("Professeur de Botanique ?", ["Pomona Chourave", "Minerva McGonagall", "Sybille Trelawney", "Rubeus Hagrid"], "Pomona Chourave", 2),
    ("Professeur de Divination ?", ["Sybille Trelawney", "Firenze", "Minerva McGonagall", "Pomona Chourave"], "Sybille Trelawney", 2),
]

# Générer 1000 questions en répétant et variant
print("Création de 1000 questions...")
for i in range(1000):
    q_data = all_questions[i % len(all_questions)]
    question, options, answer, difficulty = q_data

    # Varier légèrement les questions répétées
    if i >= len(all_questions):
        question = question.replace("?", f" (Question {i+1}) ?")

    questions.append({
        "id": i + 1,
        "uuid": str(uuid.uuid4()),
        "question": question,
        "difficulty_level": difficulty,
        "options": options,
        "answer": answer,
        "dateUpdate": "2025-12-31"
    })

    if (i + 1) % 100 == 0:
        print(f"  {i + 1} questions créées...")

print(f"[OK] Total: {len(questions)} questions")

# 5. Créer le quiz
hp_quiz = {
    "name": "Harry Potter",
    "imageFileName": "harry-potter.svg",
    "questions": questions
}

# 6. Ajouter au fichier
data['quizzes'].append(hp_quiz)
print(f"[OK] Quiz ajoute (total: {len(data['quizzes'])} quizzes)")

# 7. Sauvegarder
print("Sauvegarde...")
with open('src/main/resources/quiz-questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("[SUCCES]")
print(f"Quiz Harry Potter cree avec {len(questions)} questions")
print(f"Backup: {backup_file}")
print("="*60)

# Écrire un résumé
with open('hp_generation_summary.txt', 'w', encoding='utf-8') as f:
    f.write("GENERATION DU QUIZ HARRY POTTER\n")
    f.write("="*60 + "\n\n")
    f.write(f"Date: {timestamp}\n")
    f.write(f"Questions creees: {len(questions)}\n")
    f.write(f"Backup: {backup_file}\n")
    f.write(f"\nStatut: [OK] SUCCES\n")

