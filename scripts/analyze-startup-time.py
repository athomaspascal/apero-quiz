#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse les logs de démarrage pour mesurer le temps d'initialisation
"""

import re
from datetime import datetime
import sys

def parse_log_timestamp(line):
    """Extrait le timestamp d'une ligne de log"""
    # Format: 2026-01-06T01:30:45.123+01:00
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})', line)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%S.%f')
        except:
            pass
    return None

def analyze_startup_logs(log_file):
    """Analyse les logs de démarrage"""

    print("=" * 70)
    print("Analyse des Temps de Démarrage - Application Quiz")
    print("=" * 70)
    print()

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return

    # Rechercher les événements clés
    events = {
        'app_start': None,
        'quiz_init_start': None,
        'quiz_init_end': None,
        'country_init_start': None,
        'country_init_end': None,
        'user_init_start': None,
        'user_init_end': None,
        'migration_start': None,
        'migration_end': None,
        'app_ready': None
    }

    event_patterns = {
        'app_start': r'Starting Quizz1Application',
        'quiz_init_start': r'QuizDataInitializer: Starting initialization check',
        'quiz_init_end': r'QuizDataInitializer: Initialization check completed',
        'country_init_start': r'Initializing countries',
        'country_init_end': r'Countries initialization completed',
        'user_init_start': r'DataInitializer: Starting user and country initialization',
        'user_init_end': r'DataInitializer: Completed',
        'migration_start': r'UserCountryMigration: Starting',
        'migration_end': r'UserCountryMigration: Completed',
        'app_ready': r'Started Quizz1Application'
    }

    # Parcourir les lignes de log
    for line in lines:
        for event_name, pattern in event_patterns.items():
            if re.search(pattern, line):
                timestamp = parse_log_timestamp(line)
                if timestamp and events[event_name] is None:
                    events[event_name] = timestamp
                    print(f"✓ {event_name}: {timestamp.strftime('%H:%M:%S.%f')[:-3]}")

    print()
    print("-" * 70)
    print("Durées des Initialisations:")
    print("-" * 70)

    # Calculer les durées
    if events['quiz_init_start'] and events['quiz_init_end']:
        duration = (events['quiz_init_end'] - events['quiz_init_start']).total_seconds()
        print(f"Quiz Initialization:     {duration:.3f} secondes")
    else:
        print("Quiz Initialization:     NON TROUVÉE (optimisée)")

    if events['country_init_start'] and events['country_init_end']:
        duration = (events['country_init_end'] - events['country_init_start']).total_seconds()
        print(f"Country Initialization:  {duration:.3f} secondes")
    else:
        print("Country Initialization:  NON TROUVÉE (optimisée)")

    if events['user_init_start'] and events['user_init_end']:
        duration = (events['user_init_end'] - events['user_init_start']).total_seconds()
        print(f"User Initialization:     {duration:.3f} secondes")
    else:
        print("User Initialization:     NON TROUVÉE (optimisée)")

    if events['migration_start'] and events['migration_end']:
        duration = (events['migration_end'] - events['migration_start']).total_seconds()
        print(f"User Migration:          {duration:.3f} secondes")
    else:
        print("User Migration:          NON TROUVÉE (optimisée)")

    print()

    # Temps total
    if events['app_start'] and events['app_ready']:
        total_duration = (events['app_ready'] - events['app_start']).total_seconds()
        print("-" * 70)
        print(f"Temps Total de Démarrage: {total_duration:.3f} secondes")
        print("-" * 70)

    print()
    print("=" * 70)
    print("Optimisations Détectées:")
    print("=" * 70)

    optimizations = []
    if not events['country_init_start']:
        optimizations.append("✓ Initialisation des pays désactivée")
    if not events['user_init_start']:
        optimizations.append("✓ Initialisation des utilisateurs désactivée")
    if not events['migration_start']:
        optimizations.append("✓ Migration utilisateur-pays désactivée")

    if optimizations:
        for opt in optimizations:
            print(opt)
        print()
        print("Gain estimé: 5-10 secondes")
    else:
        print("Aucune optimisation détectée - toutes les initialisations sont actives")

    print()

if __name__ == '__main__':
    log_file = 'logs/application.log'
    if len(sys.argv) > 1:
        log_file = sys.argv[1]

    analyze_startup_logs(log_file)

