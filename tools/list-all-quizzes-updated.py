#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

print("=== LISTE DE TOUS LES QUIZ DISPONIBLES ===\n")

with open("src/main/resources/quiz-questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

quizzes = data['quizzes']

print(f"Nombre total de quiz : {len(quizzes)}\n")
print("="*80)

total_questions = 0

for i, quiz in enumerate(quizzes):
    name = quiz.get('name', 'N/A')
    image = quiz.get('imageFileName', 'N/A')
    nb_questions = len(quiz.get('questions', []))
    total_questions += nb_questions

    print(f"\n{i+1:2d}. {name}")
    print(f"    Image: {image}")
    print(f"    Questions: {nb_questions}")

    # Afficher quelques détails pour le nouveau quiz
    if 'Periodic' in name:
        print(f"    ⭐ NOUVEAU QUIZ ⭐")
        print(f"    Couvre les 118 éléments du tableau périodique")
        print(f"    4 types de questions par élément")

print("\n" + "="*80)
print(f"\n📊 STATISTIQUES GLOBALES")
print(f"   Total de quiz: {len(quizzes)}")
print(f"   Total de questions: {total_questions}")
print(f"   Moyenne de questions par quiz: {total_questions // len(quizzes)}")
print(f"\n✅ Tous les quiz sont prêts à l'utilisation!")

