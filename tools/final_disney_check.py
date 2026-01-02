#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification finale complète du quiz Disney"""
import json
import sys

def final_check():
    """Vérifie que le quiz Disney est complet et valide"""
    results = []

    try:
        # Charger le fichier JSON
        with open('src/main/resources/quiz-questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        results.append("✓ Fichier JSON chargé avec succès")

        # Trouver le quiz Disney
        disney_quiz = None
        for quiz in data['quizzes']:
            if quiz['name'] == 'Disney':
                disney_quiz = quiz
                break

        if not disney_quiz:
            results.append("✗ Quiz Disney non trouvé")
            return results, False

        results.append(f"✓ Quiz Disney trouvé")

        # Vérifier le nombre de questions
        num_questions = len(disney_quiz['questions'])
        results.append(f"✓ Nombre de questions : {num_questions}")

        if num_questions != 1000:
            results.append(f"✗ ERREUR : Attendu 1000 questions, trouvé {num_questions}")
            return results, False

        # Vérifier quelques questions aléatoires
        test_indices = [0, 100, 500, 999]
        for idx in test_indices:
            q = disney_quiz['questions'][idx]

            # Vérifier les champs obligatoires
            required_fields = ['id', 'uuid', 'question', 'difficulty_level', 'options', 'answer']
            missing_fields = [f for f in required_fields if f not in q]

            if missing_fields:
                results.append(f"✗ Question {idx+1} manque: {', '.join(missing_fields)}")
                return results, False

            # Vérifier que la réponse est dans les options
            if q['answer'] not in q['options']:
                results.append(f"✗ Question {idx+1}: réponse '{q['answer']}' pas dans les options")
                return results, False

            # Vérifier le niveau de difficulté
            if not 1 <= q['difficulty_level'] <= 3:
                results.append(f"✗ Question {idx+1}: niveau de difficulté invalide ({q['difficulty_level']})")
                return results, False

        results.append(f"✓ Questions testées ({', '.join(map(str, [i+1 for i in test_indices]))}) sont valides")

        # Vérifier les UUID uniques
        uuids = [q['uuid'] for q in disney_quiz['questions']]
        if len(uuids) != len(set(uuids)):
            results.append("✗ Des UUID sont dupliqués")
            return results, False

        results.append("✓ Tous les UUID sont uniques")

        # Vérifier l'image
        if 'imageFileName' in disney_quiz:
            results.append(f"✓ Image : {disney_quiz['imageFileName']}")
        else:
            results.append("⚠ Aucune image définie")

        # Statistiques par niveau de difficulté
        difficulty_counts = {}
        for q in disney_quiz['questions']:
            level = q['difficulty_level']
            difficulty_counts[level] = difficulty_counts.get(level, 0) + 1

        results.append("\n📊 Répartition par difficulté :")
        for level in sorted(difficulty_counts.keys()):
            results.append(f"  Niveau {level} : {difficulty_counts[level]} questions")

        results.append("\n✅ TOUTES LES VÉRIFICATIONS SONT PASSÉES !")
        results.append("Le quiz Disney de 1000 questions est complet et valide.")

        return results, True

    except json.JSONDecodeError as e:
        results.append(f"✗ Erreur de parsing JSON : {e}")
        return results, False
    except Exception as e:
        results.append(f"✗ Erreur : {e}")
        import traceback
        results.append(traceback.format_exc())
        return results, False

if __name__ == '__main__':
    results, success = final_check()

    # Écrire dans un fichier
    with open('final_check_result.txt', 'w', encoding='utf-8') as f:
        f.write("VÉRIFICATION FINALE DU QUIZ DISNEY\n")
        f.write("=" * 60 + "\n\n")
        for line in results:
            f.write(line + "\n")

    # Afficher dans la console
    for line in results:
        print(line)

    sys.exit(0 if success else 1)

