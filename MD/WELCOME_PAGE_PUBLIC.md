# Page d'Accueil Publique - Welcome View

## Date de création : 2026-01-11

## Description

Une page d'accueil publique a été créée pour permettre aux visiteurs de voir l'application sans se connecter. Cette page affiche :

- Un titre amusant "🎯 Quizz Time! 🧠" avec un dégradé de couleurs
- Une image SVG inspirante avec des cartes de quiz, un cerveau et des étoiles
- Une description engageante de l'application
- Les fonctionnalités principales (compétition, amis, duel, thèmes)
- Des boutons pour se connecter ou créer un compte

## Fichiers créés/modifiés

### Nouveaux fichiers
- `src/main/java/com/quizz/core/ui/WelcomeView.java` - Vue d'accueil publique
- `src/main/resources/META-INF/resources/images/quiz-welcome.svg` - Image décorative

### Fichiers modifiés
- `src/main/java/com/quizz/core/security/SecurityService.java` - Redirection vers WelcomeView
- `src/main/resources/messages.properties` - Traductions par défaut
- `src/main/resources/messages_en.properties` - Traductions anglaises
- `src/main/resources/messages_fr.properties` - Traductions françaises
- `src/main/resources/messages_it.properties` - Traductions italiennes

## Clés de traduction ajoutées

| Clé | EN | FR | IT |
|-----|----|----|-----|
| welcome.subtitle | Test your knowledge and have fun! | Testez vos connaissances et amusez-vous ! | Metti alla prova le tue conoscenze e divertiti! |
| welcome.description | Join thousands of players... | Rejoignez des milliers de joueurs... | Unisciti a migliaia di giocatori... |
| welcome.feature.compete | Compete for the top | Montez sur le podium | Scala la classifica |
| welcome.feature.friends | Play with friends | Jouez entre amis | Gioca con gli amici |
| welcome.feature.duel | Duel mode | Mode duel | Modalità duello |
| welcome.feature.topics | 100+ topics | 100+ thèmes | 100+ argomenti |
| welcome.login | Sign In | Se connecter | Accedi |
| welcome.register | Create Account | Créer un compte | Crea Account |
| welcome.footer | Ready to become a quiz champion? | Prêt à devenir un champion du quiz ? | Pronto a diventare un campione di quiz? |

## Accès

- **URL** : `/welcome`
- **Annotation** : `@AnonymousAllowed` (accessible sans authentification)
- **Redirection automatique** : Les utilisateurs non authentifiés sont automatiquement redirigés vers cette page

## Design

- Background avec dégradé violet (#667eea → #764ba2)
- Conteneur blanc avec coins arrondis et ombre
- Boutons stylisés avec dégradé
- Responsive design adapté aux écrans mobiles

