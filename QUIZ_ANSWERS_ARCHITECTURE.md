# 📊 Architecture du Système d'Enregistrement des Réponses

## Diagramme de Flux de Données

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FLUX D'ENREGISTREMENT                            │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  Utilisateur │
    │   (User)     │
    └──────┬───────┘
           │ répond à une question
           ▼
    ┌──────────────────┐
    │ QuizQuestionView │  ← Interface utilisateur
    └──────┬───────────┘
           │ appelle
           ▼
    ┌────────────────────┐
    │ QuizAnswerService  │  ← Logique métier
    └──────┬─────────────┘
           │ sauvegarde via
           ▼
    ┌────────────────────────┐
    │ QuizAnswerRepository   │  ← Accès aux données
    └──────┬─────────────────┘
           │ persiste dans
           ▼
    ┌──────────────────┐
    │   DATABASE       │
    │  (quiz_answer)   │
    └──────────────────┘
```

---

## Structure des Entités

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RELATIONS DES TABLES                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│    USER      │
│──────────────│
│ user_id (PK) │
│ name         │
│ email        │
└──────┬───────┘
       │
       │ 1:N
       │
       ▼
┌──────────────────┐         ┌──────────────┐
│ QUIZ_PARTICIPANT │  N:1    │ QUIZ_SESSION │
│──────────────────│◄────────│──────────────│
│ participant_id   │         │ session_id   │
│ user_id (FK)     │         │ quiz_id (FK) │
│ session_id (FK)  │         │ session_code │
│ score            │         └──────┬───────┘
│ completed        │                │
└──────┬───────────┘                │ N:1
       │                            │
       │ 1:N                        ▼
       │                     ┌─────────────┐
       │                     │    QUIZ     │
       │                     │─────────────│
       │                     │ quiz_id (PK)│
       │                     │ name        │
       │                     └──────┬──────┘
       │                            │
       │                            │ 1:N
       │                            │
       │                            ▼
       │                     ┌──────────────────┐
       │                     │ QUIZ_QUESTION    │
       │                     │──────────────────│
       │                     │ question_id (PK) │
       │                     │ quiz_id (FK)     │
       │                     │ question         │
       │                     │ options          │
       │                     │ answer           │
       │                     └──────┬───────────┘
       │                            │
       │                            │
       │                            │
       │                            │ N:1
       │                            │
       ▼                            ▼
┌─────────────────────────────────────────┐
│          QUIZ_ANSWER                    │
│─────────────────────────────────────────│
│ answer_id (PK)                          │
│ participant_id (FK) ─────────┐          │
│ question_id (FK) ────────────┼──────┐   │
│ user_answer                  │      │   │
│ is_correct                   │      │   │
│ answered_at                  │      │   │
│ time_taken_seconds           │      │   │
│                              │      │   │
│ UNIQUE(participant_id,       │      │   │
│        question_id)          │      │   │
└──────────────────────────────┘      │   │
                                      │   │
              ┌───────────────────────┘   │
              │                           │
              │ Clé étrangère vers        │
              │ QUIZ_PARTICIPANT          │
              │                           │
              └───────────────────────────┘
                  Clé étrangère vers
                  QUIZ_QUESTION
```

---

## Flux de Consultation des Statistiques

```
┌─────────────────────────────────────────────────────────────────────┐
│                   CONSULTATION DES STATISTIQUES                      │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │ Organisateur │
    │   / Admin    │
    └──────┬───────┘
           │ demande les stats
           ▼
    ┌──────────────────────┐
    │ ParticipantAnswers   │
    │       View           │
    └──────┬───────────────┘
           │ appelle
           ▼
    ┌────────────────────┐
    │ QuizAnswerService  │
    │ .getParticipant    │
    │     Stats()        │
    └──────┬─────────────┘
           │ récupère depuis
           ▼
    ┌────────────────────────┐
    │ QuizAnswerRepository   │
    │ - findByParticipant()  │
    │ - countCorrect...()    │
    │ - getAverageTime...()  │
    └──────┬─────────────────┘
           │ agrège les données
           ▼
    ┌──────────────────────────┐
    │   DATABASE               │
    │   (quiz_answer table)    │
    │   - toutes les réponses  │
    │   - avec métadonnées     │
    └──────────────────────────┘
           │
           ▼
    ┌──────────────────────────┐
    │ ParticipantAnswerStats   │
    │        (DTO)             │
    │ - score percentage       │
    │ - correct answers        │
    │ - average time           │
    │ - answer details         │
    └──────────────────────────┘
           │
           ▼
    ┌──────────────────────┐
    │  Affichage dans la   │
    │       Grille         │
    └──────────────────────┘
```

---

## Exemple de Données dans la Base

```
TABLE: quiz_answer
┌───────────┬─────────────────┬──────────────┬─────────────┬────────────┬─────────────────────┬────────────────────┐
│ answer_id │ participant_id  │ question_id  │ user_answer │ is_correct │ answered_at         │ time_taken_seconds │
├───────────┼─────────────────┼──────────────┼─────────────┼────────────┼─────────────────────┼────────────────────┤
│    1001   │       23        │      145     │   "Paris"   │    true    │ 2025-12-07 18:45:12 │        15          │
│    1002   │       23        │      146     │   "Mars"    │    true    │ 2025-12-07 18:45:35 │        23          │
│    1003   │       23        │      147     │   "Venus"   │    false   │ 2025-12-07 18:46:02 │        27          │
│    1004   │       24        │      145     │   "London"  │    false   │ 2025-12-07 18:45:20 │        20          │
│    1005   │       24        │      146     │   "Mars"    │    true    │ 2025-12-07 18:45:45 │        25          │
└───────────┴─────────────────┴──────────────┴─────────────┴────────────┴─────────────────────┴────────────────────┘

STATISTIQUES CALCULÉES:
┌─────────────────┬───────────────┬─────────────────┬───────────────────┬───────────────────┐
│ participant_id  │ total_answers │ correct_answers │ score_percentage  │ avg_time_seconds  │
├─────────────────┼───────────────┼─────────────────┼───────────────────┼───────────────────┤
│       23        │       3       │        2        │      66.67%       │       21.67       │
│       24        │       2       │        1        │      50.00%       │       22.50       │
└─────────────────┴───────────────┴─────────────────┴───────────────────┴───────────────────┘
```

---

## API des Méthodes Principales

```
┌─────────────────────────────────────────────────────────────────────┐
│                     QUIZANSWERSERVICE API                            │
└─────────────────────────────────────────────────────────────────────┘

┌─ ENREGISTREMENT ────────────────────────────────────────────────────┐
│                                                                      │
│  recordAnswer(participant, question, userAnswer)                    │
│  ➜ Enregistre une réponse sans le temps                            │
│                                                                      │
│  recordAnswer(participant, question, userAnswer, timeTakenSeconds)  │
│  ➜ Enregistre une réponse avec le temps pris                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─ CONSULTATION ──────────────────────────────────────────────────────┐
│                                                                      │
│  getParticipantAnswers(participant)                                 │
│  ➜ Liste de toutes les réponses d'un participant                   │
│                                                                      │
│  getQuestionAnswers(question)                                       │
│  ➜ Liste de toutes les réponses pour une question                  │
│                                                                      │
│  getAnswer(participant, question)                                   │
│  ➜ Réponse spécifique                                              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─ STATISTIQUES ──────────────────────────────────────────────────────┐
│                                                                      │
│  countCorrectAnswers(participant)                                   │
│  ➜ Nombre de bonnes réponses                                       │
│                                                                      │
│  countTotalAnswers(participant)                                     │
│  ➜ Nombre total de réponses                                        │
│                                                                      │
│  calculateScorePercentage(participant)                              │
│  ➜ Pourcentage de réussite                                         │
│                                                                      │
│  getAverageTimeTaken(participant)                                   │
│  ➜ Temps moyen par question                                        │
│                                                                      │
│  getParticipantStats(participant)                                   │
│  ➜ Objet complet ParticipantAnswerStats                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─ GESTION ───────────────────────────────────────────────────────────┐
│                                                                      │
│  deleteParticipantAnswers(participant)                              │
│  ➜ Supprime toutes les réponses (pour recommencer)                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Cycle de Vie d'une Réponse

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CYCLE DE VIE D'UNE RÉPONSE                     │
└─────────────────────────────────────────────────────────────────────┘

1. CRÉATION
   ┌────────────────────────────────────────────┐
   │ QuizAnswer créé avec :                     │
   │ - participant                              │
   │ - question                                 │
   │ - userAnswer                               │
   │ - correct (calculé automatiquement)        │
   │ - answeredAt (maintenant)                  │
   │ - timeTakenSeconds (optionnel)             │
   └────────────────────────────────────────────┘
                    ▼
2. VALIDATION
   ┌────────────────────────────────────────────┐
   │ Vérification contrainte d'unicité          │
   │ ➜ Un participant peut répondre une seule   │
   │   fois à chaque question                   │
   └────────────────────────────────────────────┘
                    ▼
3. PERSISTANCE
   ┌────────────────────────────────────────────┐
   │ Enregistrement en base de données          │
   │ ➜ Données immédiatement disponibles        │
   │   pour consultation                        │
   └────────────────────────────────────────────┘
                    ▼
4. UTILISATION
   ┌────────────────────────────────────────────┐
   │ - Calcul du score                          │
   │ - Statistiques                             │
   │ - Leaderboard                              │
   │ - Révision                                 │
   │ - Analyse                                  │
   └────────────────────────────────────────────┘
```

---

**Date** : 7 décembre 2025  
**Version** : 1.0  
**Statut** : Production Ready

